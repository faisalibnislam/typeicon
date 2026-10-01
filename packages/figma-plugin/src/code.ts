// Main-thread (sandbox) code. Has access to the `figma` API but no DOM and
// no network access of its own here: all catalog requests happen in the UI
// iframe, which is restricted by manifest.networkAccess.

import type { MainToUi } from './messages';
import {
  applyColor,
  iconNodeName,
  rescaleSteps,
  validateApiBase,
  validateInsertMessage,
} from './shared';

// Injected by build.mjs: http://localhost:3107 for --dev, https://typeicon.net otherwise.
declare const __DEFAULT_API_BASE__: string;

const STORAGE_KEY_API_BASE = 'apiBase';
const PLUGIN_DATA_KEY = 'typeicon';
const GAP = 16;

figma.showUI(__html__, { width: 360, height: 560, themeColors: true, title: 'TypeIcon' });

function post(msg: MainToUi): void {
  figma.ui.postMessage(msg);
}

async function readApiBase(): Promise<string> {
  try {
    const stored: unknown = await figma.clientStorage.getAsync(STORAGE_KEY_API_BASE);
    const checked = validateApiBase(stored);
    if (checked.ok) return checked.value;
  } catch {
    // Fall through to the default; clientStorage may be unavailable.
  }
  return __DEFAULT_API_BASE__;
}

function placementFor(node: SceneNode): { x: number; y: number } {
  const selection = figma.currentPage.selection;
  const boxes = selection
    .map((n) => n.absoluteBoundingBox)
    .filter((b): b is Rect => b !== null);
  if (boxes.length > 0) {
    const right = Math.max(...boxes.map((b) => b.x + b.width));
    const top = Math.min(...boxes.map((b) => b.y));
    return { x: Math.round(right + GAP), y: Math.round(top) };
  }
  const c = figma.viewport.center;
  return { x: Math.round(c.x - node.width / 2), y: Math.round(c.y - node.height / 2) };
}

function insertIcon(raw: unknown): void {
  const checked = validateInsertMessage(raw);
  if (!checked.ok) {
    figma.notify(`TypeIcon: ${checked.error}`, { error: true });
    post({ type: 'insert-error', error: checked.error });
    return;
  }
  const req = checked.value;

  let frame: FrameNode;
  try {
    frame = figma.createNodeFromSvg(applyColor(req.svg, req.color));
  } catch (err) {
    const error = `Figma could not import this SVG (${err instanceof Error ? err.message : String(err)}).`;
    figma.notify(`TypeIcon: ${error}`, { error: true });
    post({ type: 'insert-error', error });
    return;
  }

  frame.name = iconNodeName(req.style, req.name);
  // Scale uniformly so the longest side is 24px (strokes scale too).
  for (const step of rescaleSteps(frame.width, frame.height)) frame.rescale(step);
  try {
    frame.lockAspectRatio();
  } catch {
    // Older Figma builds may lack lockAspectRatio(); the icon is still usable.
  }

  const pos = placementFor(frame);
  figma.currentPage.appendChild(frame);
  frame.x = pos.x;
  frame.y = pos.y;

  const meta = {
    name: req.name,
    style: req.style,
    source: req.source,
    license: req.license,
    iconId: req.id,
    variantId: `${req.id}:${req.style}`,
    color: req.color ?? '#000000',
  };
  frame.setPluginData(PLUGIN_DATA_KEY, JSON.stringify(meta));
  frame.setPluginData('name', req.name);
  frame.setPluginData('style', req.style);
  frame.setPluginData('source', req.source);
  frame.setPluginData('license', req.license);
  frame.setPluginData('variantId', meta.variantId);

  figma.currentPage.selection = [frame];
  figma.notify(`Inserted ${req.name} (${req.style}) · ${req.license}`);
  post({ type: 'inserted', name: req.name });
}

figma.ui.onmessage = async (msg: unknown) => {
  if (!msg || typeof msg !== 'object') return;
  const type = (msg as { type?: unknown }).type;
  switch (type) {
    case 'get-settings': {
      post({ type: 'settings', apiBase: await readApiBase(), defaultApiBase: __DEFAULT_API_BASE__ });
      return;
    }
    case 'set-settings': {
      const checked = validateApiBase((msg as { apiBase?: unknown }).apiBase);
      if (!checked.ok) {
        post({ type: 'settings-error', error: checked.error });
        return;
      }
      try {
        await figma.clientStorage.setAsync(STORAGE_KEY_API_BASE, checked.value);
      } catch {
        post({ type: 'settings-error', error: 'Could not save settings.' });
        return;
      }
      post({ type: 'settings', apiBase: checked.value, defaultApiBase: __DEFAULT_API_BASE__ });
      return;
    }
    case 'insert':
      insertIcon(msg);
      return;
    case 'close':
      figma.closePlugin();
      return;
    default:
      return;
  }
};
