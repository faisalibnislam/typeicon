"""Writes plan.json: the TypeIcon Core base-concept plan (categories, concepts, variant sets).

Edit the lists below, then run: .venv/bin/python tools/core-authoring/make_plan.py
Names are lowercase kebab-case. Existing icons are skipped by the authoring agents.
"""
import json
import re
from pathlib import Path

C = {}

def cat(slug, title, mods, names):
    C[slug] = {"title": title, "modifiers": mods, "concepts": [n.strip() for n in names.split() if n.strip()]}

cat("arrows", "Arrows & navigation", "none", """
arrow-up-right arrow-up-left arrow-down-right arrow-down-left arrows-left-right arrows-up-down arrow-big-up arrow-big-down
arrow-big-left arrow-big-right arrow-bar-up arrow-bar-down arrow-bar-left arrow-bar-right arrow-circle-up arrow-circle-down
arrow-circle-left arrow-square-up arrow-square-down arrow-square-left arrow-square-right chevron-up chevron-left chevrons-up
chevrons-down chevrons-left chevrons-right chevron-up-down chevron-left-right corner-up-left corner-up-right corner-down-left
corner-down-right corner-left-up corner-right-up move move-diagonal expand collapse maximize minimize fullscreen
fullscreen-exit undo redo rotate-cw rotate-ccw refresh-ccw repeat repeat-once shuffle swap-horizontal swap-vertical
sort-ascending sort-descending trending-up trending-down login logout enter exit reply reply-all forward-mail redirect
merge split fork route direction navigation compass-arrow crosshair target focus zoom-in zoom-out drag-horizontal
drag-vertical pointer-hand cursor-text grab arrow-curve-left arrow-curve-right arrow-loop arrow-zigzag arrow-return
arrow-narrow-up arrow-narrow-down arrow-narrow-left arrow-narrow-right caret-up caret-left arrows-maximize arrows-minimize
arrows-shuffle arrows-cross arrows-diagonal arrow-autofit-width arrow-autofit-height u-turn-left u-turn-right step-into step-out
""")
cat("interface", "Interface & layout", "full", """
dashboard sidebar sidebar-right layout-columns layout-rows layout-grid layout-sidebar layout-bottombar layout-navbar
layout-cards layout-list layout-masonry table kanban window app-window browser tabs toggle-on toggle-off slider-horizontal
checkbox checkbox-checked radio-button radio-selected dropdown button input-field form search-field list-checks list-ordered
list-tree list-details more-horizontal more-vertical grip-vertical grip-horizontal drag-handle adjustments sliders-horizontal
sliders-vertical command keyboard-shortcut spinner loader progress-bar notification-dot pin unpin picture-in-picture split-view
component components frame-corners section divider spacing padding margin z-index layers-ui modal popover tooltip toast
accordion carousel pagination breadcrumb stepper menu-2 menu-dots app-grid launcher home-screen widget cursor-click
cursor-pointer select-area lasso marquee resize crop-ui aspect grid-dots ruler-ui
""")
cat("text", "Text & editor", "common", """
bold italic underline strikethrough heading heading-1 heading-2 heading-3 paragraph quote code-inline code-block link-2
unlink align-left align-center align-right align-justify align-top align-middle align-bottom indent outdent list-bullet
list-number text-size font-family typography letter-case uppercase lowercase subscript superscript highlighter eraser
pilcrow spell-check translate text-cursor clear-formatting text-color text-wrap line-height letter-spacing text-direction-ltr
text-direction-rtl columns-text blockquote horizontal-rule table-insert image-insert emoji-insert mention hashtag at-sign
markdown word-count text-recognition signature-pen ink-pen fountain-pen marker quill
""")
cat("files", "Files & documents", "full", """
file-text file-image file-video file-audio file-code file-zip file-pdf file-spreadsheet file-presentation file-document
file-font file-vector file-3d file-database file-json file-csv file-shield file-certificate file-invoice file-report
file-stack folder-open folders folder-tree folder-zip folder-shared clipboard clipboard-list clipboard-text notebook book
book-open books archive archive-box inbox outbox paperclip document-signed contract receipt invoice report certificate
id-card passport ticket sticky-note note notes journal scroll newspaper magazine catalog library dossier envelope-document
page-blank pages cover-page table-of-contents manuscript blueprint
""")
cat("communication", "Communication", "full", """
message-circle message-square messages chat-dots chat-bubbles comment-dots send paper-plane mail-open mailbox mail-stack
phone-call phone-incoming phone-outgoing phone-missed phone-ringing voicemail video-call contact address-book megaphone
broadcast rss podcast antenna satellite-dish walkie-talkie fax pager speech-bubble thought-bubble quote-bubble
conversation announcement inbox-full newsletter email-at letter postcard stamp-postage telegram-message signal-bars
chat-typing mail-flag intercom speakerphone headset-support
""")
cat("media", "Audio & video", "full", """
music music-note music-notes headphones speaker volume-low volume-high volume-mute volume-off radio record stop-circle
play-circle pause-circle skip-forward skip-back fast-forward rewind repeat-song playlist album vinyl cassette film
clapperboard video video-camera webcam tv projector screen-share cast subtitles closed-captions equalizer waveform
metronome microphone-stand microphone-vintage guitar electric-guitar piano drum trumpet violin saxophone flute harp
tambourine xylophone accordion-instrument bell-music mixer turntable boombox mp3-player movie-reel popcorn-movie ticket-movie
""")
cat("design", "Photo & design", "full", """
images gallery crop rotate-image flip-horizontal flip-vertical aspect-ratio palette brush paintbrush pen-tool ruler compass-drawing
eyedropper color-swatch layers stack shapes vector bezier grid-lines frame focus-frame aperture lens shutter camera-flash magic-wand
sparkles stamp scissors sticker spray-can bucket-fill gradient contrast brightness exposure blur sharpen photo-album polaroid
film-strip selection-tool artboard mockup typography-design color-wheel paint-roller easel sculpture mosaic origami
""")
cat("devices", "Devices & hardware", "full", """
laptop desktop monitor tablet watch smartwatch keyboard mouse printer scanner server database hard-drive ssd usb cpu memory-chip
router modem plug socket cable battery-charging bluetooth nfc gamepad joystick vr-headset drone robot calculator security-camera
smart-speaker remote-control lightbulb lamp flashlight power power-button fan thermometer sd-card sim-card headset earbuds
tv-retro radio-retro phone-retro floppy-disk cd dvd projector-device e-reader game-console handheld-console charger
power-bank ethernet-port hdmi wifi-router server-rack desktop-tower all-in-one
""")
cat("development", "Development & code", "full", """
code terminal command-line bug git-branch git-commit git-merge git-pull-request git-compare git-fork api webhook brackets braces
function variable binary regex database-table schema sitemap cloud-code server-stack container cube package puzzle plug-connected
api-key token cookie shield-code branch-tree deploy pipeline test-tube-code debug breakpoint console log-file source-code
repository tag-version release diff merge-conflict hotfix algorithm data-structure queue stack-data graph-nodes network-topology
""")
cat("security", "Security & privacy", "full", """
shield-check shield-lock shield-x fingerprint face-id key-round keyhole password safe vault eye-off incognito spy alarm siren cctv
id-badge verified security-certificate firewall virus lock-keyhole padlock-open two-factor otp captcha scan-face access-card
door-lock guard privacy mask-privacy detective-glass warning-shield bomb-disposal biometric retina-scan
""")
cat("people", "People & roles", "common", """
users user-group team person-standing person-walking person-running baby child elderly family man woman gender-neutral
hand-raised handshake crowd profile user-circle user-square contact-card student teacher worker chef doctor nurse police
firefighter astronaut detective judge pilot farmer builder scientist artist musician photographer mechanic waiter cashier
programmer designer lifeguard soldier king queen prince princess wizard ninja pirate superhero bride groom couple
""")
cat("body", "Body & anatomy", "minimal", """
head face ear nose mouth lips tooth teeth tongue hand hand-open fist finger-point arm bicep leg foot footprints heart-organ brain
lungs stomach liver kidneys intestines bone skull spine ribs skeleton knee hip pelvis hair beard mustache eyebrow eyelashes palm
fingernail blood-drop dna cell neuron eye-closed eye-open ear-hearing pregnant baby-feet shoulder elbow wrist ankle toe thumb
neck chest back-body belly-button muscle-fiber vein kidney thyroid bladder womb tooth-molar jaw eyeball iris
""")
cat("health", "Health & medical", "common", """
hospital ambulance first-aid medical-cross stethoscope syringe pill pills capsule bandage medical-thermometer heart-pulse
heartbeat ecg blood-pressure microscope test-tube flask bacteria vaccine face-mask wheelchair crutch walker x-ray body-scan
dental eye-chart glasses hearing-aid prescription medical-clipboard dropper iv-bag hospital-bed scalpel band-aid dna-helix
inhaler pill-bottle ointment splint cast-arm defibrillator oxygen-tank blood-bag transfusion allergy fever cough sneeze
virus-shield quarantine mental-health meditation sleep calories weight-scale nutrition
""")
cat("clothing", "Clothing & fashion", "common", """
t-shirt shirt polo dress skirt pants jeans shorts jacket coat hoodie sweater vest suit tie bow-tie scarf hat cap beanie sock
shoe sneaker boot high-heel sandal slipper glove mitten belt handbag backpack wallet purse wristwatch ring necklace earring
bracelet sunglasses swimsuit bikini underwear bra pajamas uniform apron hanger sewing-machine needle-thread sewing-button
tank-top blouse cardigan kimono sari raincoat overalls leggings cowboy-hat top-hat helmet crown tiara lipstick perfume
nail-polish comb hairbrush razor zipper safety-pin clothes-iron laundry-basket fabric
""")
cat("food", "Food & drink", "minimal", """
apple banana cherry grapes lemon orange pear strawberry watermelon pineapple avocado carrot broccoli corn chili-pepper tomato
eggplant potato onion mushroom bread croissant cheese egg meat drumstick fish-food shrimp burger pizza hot-dog taco sandwich
fries noodles rice-bowl sushi soup salad cake cupcake cookie donut ice-cream candy lollipop chocolate popcorn coffee tea cup mug
water-glass wine-glass beer cocktail bottle milk juice soda teapot kettle fork-knife spoon chef-hat cutting-board frying-pan
cooking-pot oven microwave toaster blender grill peach coconut kiwi lime mango blueberries garlic cucumber lettuce pumpkin
peanut bacon steak pancakes waffle pie pretzel honey jam salt pepper-shaker ketchup bento dumpling kebab
""")
cat("home", "Home & furniture", "common", """
sofa armchair chair dining-table desk bed crib wardrobe drawers shelf bookshelf floor-lamp desk-lamp ceiling-light chandelier
door door-open window-house stairs fireplace bathtub shower toilet sink faucet mirror towel washing-machine dryer fridge
dishwasher air-conditioner heater radiator vacuum broom mop bucket recycle-bin plant-pot picture-frame wall-clock rug curtains
house-key doorbell letterbox garage fence cabinet nightstand bench stool hammock bunk-bed coat-rack umbrella-stand smoke-detector
light-switch power-outlet thermostat-home ceiling-fan candle-holder vase cushion blanket pillow
""")
cat("buildings", "Buildings & places", "common", """
building office apartment skyscraper factory warehouse store bank school university hospital-building church mosque temple
synagogue castle tent cabin hotel restaurant cafe museum library-building stadium theater cinema lighthouse bridge tower
windmill barn igloo pyramid monument fountain park playground gas-station parking police-station fire-station post-office
courthouse airport train-station bus-stop harbor capitol pagoda arena mall supermarket pharmacy gym-building spa garage-building
""")
cat("travel", "Maps & travel", "common", """
map map-folded pin-drop globe-earth compass signpost milestone luggage suitcase-rolling passport-travel plane-ticket boarding-pass
binoculars travel-backpack camping-tent campfire mountain beach-umbrella island palm-tree sunrise sunset key-card road highway
traffic-light crosswalk parking-meter toll-booth world-map route-pins location-arrow gps satellite street-sign tour-bus cruise
souvenir postcard-travel visa currency-exchange-travel hostel resort camper
""")
cat("transport", "Transport & vehicles", "common", """
car car-side taxi bus truck van fire-truck police-car motorcycle scooter bicycle e-bike skateboard train tram subway plane
plane-takeoff plane-landing helicopter rocket ship boat sailboat ferry submarine anchor steering-wheel fuel ev-charger tire engine
gear-shift seatbelt speedometer traffic-cone road-sign tractor forklift crane excavator cable-car hot-air-balloon parachute
horse-carriage kick-scooter wheelchair-transport tow-truck garbage-truck delivery-van race-car convertible pickup-truck
minivan jet-ski canoe kayak yacht container-ship freight-train monorail
""")
cat("nature", "Nature & weather", "minimal", """
cloud-rain cloud-snow cloud-lightning cloud-sun cloud-moon fog wind tornado hurricane snowflake raindrop umbrella rainbow
thermometer-hot thermometer-cold star-night comet planet earth volcano wave water-drop fire leaf tree pine-tree flower rose tulip
sunflower cactus seedling sprout clover feather seashell stone crystal snowman iceberg desert forest meteor moon-crescent
moon-full sun-cloud hail sleet drizzle heatwave waterfall river lake cave canyon coral bamboo maple-leaf acorn pinecone
""")
cat("animals", "Animals", "minimal", """
cat dog bird fish horse cow pig sheep goat chicken duck rabbit mouse-animal hamster bear panda lion tiger elephant giraffe
zebra monkey fox wolf deer owl eagle penguin parrot dove butterfly bee ant spider ladybug snail turtle frog snake lizard
crocodile dinosaur whale dolphin shark octopus crab jellyfish squid bat squirrel hedgehog koala kangaroo camel llama paw
dog-bone bird-cage fish-bowl pet-bowl rhino hippo flamingo swan peacock rooster unicorn dragon seal otter beaver raccoon
""")
cat("sports", "Sports & fitness", "common", """
soccer-ball basketball baseball tennis-ball volleyball golf hockey cricket rugby american-football bowling boxing-glove dumbbell
kettlebell barbell yoga running swimming cycling skiing snowboard ice-skating surfing climbing trophy medal podium stopwatch
whistle dartboard bow-arrow ping-pong badminton jersey finish-flag scoreboard goal-net baseball-bat golf-club hockey-stick
tennis-racket skates helmet-sports treadmill jump-rope weightlifting karate archery fishing-rod
""")
cat("games", "Games & entertainment", "common", """
dice chess-king chess-queen chess-rook chess-bishop chess-knight chess-pawn playing-cards poker-chip arcade ghost alien sword
shield-game potion treasure-chest heart-game coin gem crown-game balloon party-popper confetti gift ticket theater-masks circus
ferris-wheel roller-coaster carousel puzzle-piece joystick-arcade game-cartridge controller-retro boss-skull health-bar
level-up map-treasure castle-game dragon-game magic-book crystal-ball tarot slot-machine
""")
cat("commerce", "Shopping & commerce", "full", """
basket shopping-bag price-tag barcode qr-code credit-card cash coins banknote piggy-bank gift-card coupon discount sale
package-box delivery-truck shipping return-box cash-register pos-terminal shop-scale storefront product inventory warehouse-shelf
order checkout invoice-shop receipt-long shopping-list wishlist loyalty-card trolley bag-check store-open store-closed
""")
cat("finance", "Finance & business", "full", """
dollar euro pound yen rupee crypto-coin currency-exchange chart-line chart-pie chart-area chart-candlestick budget tax loan
stock-up stock-down portfolio briefcase contract-sign gold-bar diamond presentation whiteboard flip-chart meeting agenda stapler
pushpin folder-stack filing-cabinet org-chart hierarchy workflow goal lightbulb-idea rocket-launch award signature seal-stamp
bank-card atm cheque savings investment calculator-money ledger audit
""")
cat("education", "Education & science", "common", """
graduation-cap school-backpack pencil pen eraser-school crayon chalkboard abacus desk-globe atom molecule beaker telescope magnet
protractor math-compass exercise-book school-bell formula periodic-table lab-coat test-paper grade-a certificate-education
diploma lecture online-course bookmark-book reading glasses-reading dictionary encyclopedia quiz homework
""")
cat("math", "Math & symbols", "none", """
pi sigma infinity integral square-root plus-minus divide multiply equals not-equal approximately less-than greater-than
less-equal greater-equal percentage per-mille degree function-fx theta alpha beta gamma delta lambda mu omega phi epsilon
factorial parentheses brackets-square fraction exponent logarithm angle triangle-math circle-math sum-symbol product-symbol
empty-set union intersection subset element-of for-all exists therefore because number-sign ampersand asterisk section-sign
paragraph-mark copyright registered trademark-symbol vector-arrow matrix radian axis graph-function coordinates
""")
cat("shapes", "Shapes", "none", """
circle square triangle diamond-shape hexagon octagon pentagon oval rectangle rhombus parallelogram trapezoid crescent ring cross
plus-shape spiral wave-shape zigzag squiggle blob polygon cube-shape sphere cylinder cone pyramid-shape torus prism star-4
star-6 heart-outline-shape shield-shape badge-shape
""")
cat("time", "Time & calendar", "common", """
alarm-clock stopwatch timer hourglass calendar-days calendar-week calendar-range sundial history schedule time-zone countdown
snooze calendar-event calendar-today clock-analog clock-digital date-picker weekend deadline recurring
""")
cat("emotions", "Emoji & emotions", "none", """
smile laugh wink sad cry angry surprised neutral confused heart-eyes sick sleepy cool thinking kiss tongue-out zipper-mouth
party-face star-struck grimace worried relieved nerd skull-emoji poop-emoji
""")
cat("gestures", "Hands & gestures", "none", """
hand-wave hand-stop hand-point-up hand-point-down hand-point-left hand-point-right hand-peace hand-ok hand-rock hand-heart
clap pray fist-bump hand-grab hand-pinch hand-swipe hand-tap hand-click thumbs-up thumbs-down hand-call-me hand-crossed-fingers
hand-write hand-shake-deal hand-coins
""")
cat("social", "Social", "common", """
like dislike repost follow unfollow notification-bell poll vote survey feedback rating review trending hashtag-social share-alt
comment-heart live-stream story reel followers verified-badge influencer community-group
""")
cat("tools", "Tools & construction", "common", """
hammer wrench screwdriver saw drill pliers toolbox tape-measure spirit-level paint-bucket trowel shovel pickaxe axe hard-hat
ladder brick-wall bulldozer nut-bolt screw nail cogs chain rope hook anvil welding sandpaper clamp utility-knife blueprint-roll
""")
cat("garden", "Garden & farming", "minimal", """
watering-can garden-rake wheelbarrow seed-bag potted-plant harvest wheat crop-corn farm-fence scarecrow beehive greenhouse
lawn-mower garden-hose hedge-trimmer compost sprinkler plant-sprout fruit-tree vegetable-basket
""")
cat("energy", "Energy & environment", "common", """
solar-panel wind-turbine battery-full battery-low battery-empty energy-plug leaf-eco recycle hydro-power nuclear oil-drop
gas-flame power-plant charging-station thermostat carbon-footprint earth-eco water-saving electricity-meter power-grid
""")
cat("charts", "Charts & data", "full", """
chart-bar-horizontal chart-donut chart-scatter chart-bubble chart-radar chart-funnel chart-histogram gauge speed-gauge
table-data analytics kpi report-chart chart-dots chart-arrows chart-waterfall chart-treemap chart-sankey chart-gantt
""")
cat("celebration", "Holidays & celebrations", "minimal", """
birthday-cake fireworks christmas-tree pumpkin-halloween candle menorah lantern easter-egg valentine wedding-ring champagne
party-hat gift-box ribbon bell-christmas snowglobe wreath
""")
cat("culture", "Culture & belief", "none", """
yin-yang peace-sign hamsa cross-christian star-of-david crescent-star om dharma-wheel khanda torii prayer-beads
""")
cat("accessibility", "Accessibility", "minimal", """
accessibility-person sign-language braille audio-description hearing-loop blind-cane service-dog low-vision cognitive
mobility-aid easy-read
""")
cat("status", "Alerts & status", "common", """
alert-circle alert-octagon ban stop-sign loader-circle bell-ring badge-status flag-status circle-check-dashed circle-dashed
circle-dot circle-half status-online status-offline status-busy status-away progress-check shield-status
""")
cat("space", "Space & astronomy", "minimal", """
satellite-orbit planet-ring ufo shooting-star galaxy moon-phases solar-eclipse black-hole space-station astronaut-helmet
constellation observatory lunar-rover
""")
cat("letters", "Letters & numbers", "none",
    " ".join([f"letter-{c}" for c in "abcdefghijklmnopqrstuvwxyz"] + [f"number-{n}" for n in range(10)]
             + [f"square-letter-{c}" for c in "abcdefghijklmnopqrstuvwxyz"] + [f"circle-number-{n}" for n in range(10)]))

# Existing v0.1 categories -> variant sets
EXISTING = {"navigation": "none", "arrows": "none", "actions": "common", "status": "common", "people": "common", "social": "common",
            "communication": "full", "security": "full", "time": "common", "objects": "common", "files": "full", "media": "full",
            "commerce": "full", "places": "common", "weather": "minimal", "devices": "full", "layout": "full", "data": "full"}

NAME_RE = re.compile(r"^(?=.{2,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$")
seen = {}
for slug, c in C.items():
    uniq = []
    for n in c["concepts"]:
        assert NAME_RE.match(n), n
        if n in seen:
            continue
        seen[n] = slug
        uniq.append(n)
    c["concepts"] = uniq

out = {"$comment": "Generated by make_plan.py. Base concepts to draw; variants are generated from modifier sets.",
       "categories": C, "existingCategoryModifiers": EXISTING}
Path(__file__).with_name("plan.json").write_text(json.dumps(out, indent=1) + "\n")
print(len(C), "categories,", sum(len(c["concepts"]) for c in C.values()), "planned base concepts")
for s, c in C.items():
    print(f"  {s:14} {len(c['concepts']):4}  {c['modifiers']}")
