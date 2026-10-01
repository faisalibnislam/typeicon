"""SVG sanitation: security properties and honest routing (never silently change artwork)."""
import pytest

from typeicon_fonts.svg_sanitize import MAX_BYTES, SvgRejected, sanitize_svg

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{}</svg>'


def test_rejects_doctype_and_entities():
    xxe = '<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h1v1z"/></svg>'
    with pytest.raises(SvgRejected, match="DOCTYPE"):
        sanitize_svg(xxe)


def test_rejects_billion_laughs():
    bomb = '<!DOCTYPE lolz [<!ENTITY lol "lol"><!ENTITY lol2 "&lol;&lol;&lol;">]><svg xmlns="http://www.w3.org/2000/svg">&lol2;</svg>'
    with pytest.raises(SvgRejected):
        sanitize_svg(bomb)


def test_removes_scripts_handlers_links_foreign_object():
    evil = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24" onload="alert(1)">'
            '<script>alert(2)</script><style>*{fill:url(https://x)}</style>'
            '<a href="https://evil.example"><path d="M1 1h2v2z"/></a>'
            '<foreignObject><div xmlns="http://www.w3.org/1999/xhtml">x</div></foreignObject>'
            '<path d="M4 4h16v16H4z" onclick="steal()" style="fill:url(https://evil.example/x.svg#g)"/></svg>')
    r = sanitize_svg(evil)
    low = r.svg.lower()
    for bad in ("script", "onload", "onclick", "foreignobject", "href", "evil.example", "<style", "<a "):
        assert bad not in low, bad
    assert "M4 4h16v16H4z" in r.svg


def test_external_use_reference_removed_and_routed_svg_only():
    r = sanitize_svg(SVG.format('<use href="https://evil.example/sprite.svg#x"/>'))
    assert "evil.example" not in r.svg
    assert r.route == "svg-only"


@pytest.mark.parametrize("body,reason", [
    ('<defs><linearGradient id="g"><stop offset="0"/></linearGradient></defs><path d="M0 0h9v9z" fill="url(#g)"/>', "gradient"),
    ('<image href="data:image/png;base64,AAAA" width="10" height="10"/>', "raster image"),
    ('<text x="1" y="10">Hi</text>', "text"),
    ('<filter id="f"/><path d="M0 0h9v9z"/>', "filter"),
    ('<mask id="m"/><path d="M0 0h9v9z"/>', "mask"),
    ('<path d="M0 0h9v9z" opacity="0.2"/><path d="M9 9h9v9z"/>', "partial opacity (multi-tone artwork)"),
    ('<path d="M0 0h9v9z" fill="#f00"/><path d="M9 9h9v9z" fill="#00f"/>', "multicolour artwork"),
])
def test_unsupported_artwork_routed_to_svg_only(body, reason):
    r = sanitize_svg(SVG.format(body))
    assert r.route == "svg-only"
    assert reason in r.reasons


def test_single_colour_unified_to_current_color_and_viewbox_kept():
    r = sanitize_svg('<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M0 -960h960v960H0z" fill="#000"/></svg>')
    assert r.route == "font"
    assert 'viewBox="0 -960 960 960"' in r.svg
    assert "currentColor" in r.svg and "#000" not in r.svg
    assert 'width=' not in r.svg


@pytest.mark.parametrize("data", [
    b"not xml at all",
    b'<html><body/></html>',
    b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 10"/>',
])
def test_rejects_invalid_documents(data):
    with pytest.raises(SvgRejected):
        sanitize_svg(data)


def test_size_and_depth_limits():
    with pytest.raises(SvgRejected, match="larger"):
        sanitize_svg(b"<svg>" + b" " * (MAX_BYTES + 1) + b"</svg>")
    deep = SVG.format("<g>" * 40 + '<path d="M0 0h1v1z"/>' + "</g>" * 40)
    with pytest.raises(SvgRejected, match="deep"):
        sanitize_svg(deep)
