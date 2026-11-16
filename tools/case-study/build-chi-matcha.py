"""Builds chi-matcha.html (the Chi Matcha case study) from the colour and frame tokens in index.html.
Run: python tools/case-study/build-chi-matcha.py  (after changing tokens or the copy below)."""
import re
import os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
idx = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
a = idx.index('    :root {'); b = idx.index('    /*gen:farmcss*/')
TOKENS = idx[a:b].rstrip() + '\n'
ICON = re.search(r'<link rel="icon"[^>]*>', idx).group(0)

CSS = r'''
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 72px; }
    body { font-family: var(--f-body); font-size: 17px; line-height: 28px; color: var(--text); background: var(--page); -webkit-font-smoothing: antialiased; overflow-x: hidden; }
    a { color: var(--ink); text-decoration: underline; text-decoration-color: var(--wheat); text-decoration-thickness: 3px; text-underline-offset: 4px; }
    a:hover { background: var(--wheat); color: #2e2419; }
    :focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
    img { display: block; max-width: 100%; height: auto; }
    .skip-link { position: absolute; left: var(--s2); top: -100px; z-index: 1000; padding: var(--s2) var(--s3); background: var(--ink); color: #fff; font: 20px/24px var(--f-px); text-decoration: none; }
    .skip-link:focus { top: var(--s2); }
    .container { width: min(1040px, calc(100% - 64px)); margin: 0 auto; }
    h1, h2, h3 { font-family: var(--f-px); font-weight: 400; color: var(--ink); }
    h1 { font-size: 96px; line-height: 88px; }
    h2 { font-size: 40px; line-height: 40px; margin-bottom: var(--s4); }
    h3 { font-size: 28px; line-height: 32px; }
    section { padding-top: var(--s8); }
    p + p { margin-top: var(--s3); }

    .btn-game { font: 20px/24px var(--f-px); color: var(--ink); text-decoration: none; cursor: pointer; display: inline-flex; align-items: center; gap: var(--s2); padding: 6px 10px; position: relative; border: 6px solid transparent; background: none; border-image: var(--fr-btn2) 6 fill / 6px / 0 stretch; filter: drop-shadow(0 4px 0 var(--btn2-drop)); margin-bottom: 4px; }
    .btn-game:hover { background: none; color: #2e2419; border-image-source: var(--fr-btn); }
    .btn-game:active { transform: translateY(4px); filter: none; }
    .btn-primary-g { border-image-source: var(--fr-btn); color: var(--on-wheat); filter: drop-shadow(0 4px 0 var(--btn-drop)); }
    .btn-primary-g:hover { border-image-source: var(--fr-btn-hi); }
    .px { width: 24px; height: 24px; flex: none; fill: currentColor; shape-rendering: crispEdges; }

    .cs-bar { position: sticky; top: 0; z-index: 50; background: var(--sky-1); border-bottom: 4px solid var(--page); }
    .cs-bar .container { display: flex; align-items: center; justify-content: space-between; gap: var(--s3); min-height: 60px; flex-wrap: wrap; padding: var(--s1) 0; }
    .cs-bar a.back { font: 22px/28px var(--f-px); text-decoration: none; padding: var(--s1) var(--s2); margin-left: calc(-1 * var(--s2)); }
    .cs-bar a.back:hover { background: var(--wheat); }
    .cs-bar .cs-title { font: 20px/24px var(--f-px); color: var(--dim); }
    .cs-bar-tools { display: flex; align-items: center; gap: var(--s2); }
    .cs-bar-tools .btn-game { padding-top: 4px; padding-bottom: 4px; margin-bottom: 0; }

    .cs-hero { padding-top: var(--s7); }
    .cs-kicker { font: 24px/28px var(--f-px); color: var(--wheat-ink); margin-bottom: var(--s2); }
    .cs-lede { font-size: 22px; line-height: 34px; max-width: 34em; margin-top: var(--s4); }
    .chips { display: flex; flex-wrap: wrap; gap: var(--s2); margin-top: var(--s4); list-style: none; }
    .chip { font-size: 14px; line-height: 20px; padding: 2px 10px; background: var(--tint); color: var(--ink); clip-path: var(--notch); }
    .cs-actions { display: flex; flex-wrap: wrap; gap: var(--s3); margin-top: var(--s5); }
    .shot { border: 6px solid transparent; border-image: var(--fr-soft) 6 / 6px / 0 stretch; }
    .cs-hero .shot { margin-top: var(--s6); width: 100%; }

    .glance { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--s4) var(--s5); border: 6px solid transparent; border-image: var(--fr-panel) 6 fill / 6px / 0 stretch; padding: var(--s4); }
    .glance dt { font: 20px/24px var(--f-px); color: var(--dim); }
    .glance dd { margin-top: var(--s1); }

    .lead-quote { font: 34px/38px var(--f-px); color: var(--ink); max-width: 20em; }
    .lead-quote + p { margin-top: var(--s4); max-width: 38em; }

    .steps { list-style: none; counter-reset: s; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--s4); }
    .steps li { counter-increment: s; position: relative; padding: var(--s4) var(--s3) var(--s3); border: 6px solid transparent; border-image: var(--fr-soft) 6 fill / 6px / 0 stretch; }
    .steps li::before { content: counter(s); position: absolute; top: -18px; left: var(--s3); font: 28px/32px var(--f-px); color: #2e2419; background: var(--wheat); padding: 0 var(--s2); clip-path: var(--notch); }
    .note { margin-top: var(--s4); color: var(--dim); font-size: 16px; line-height: 24px; max-width: 44em; }

    .screens { list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--s6) var(--s5); }
    .screens figure { margin: 0; }
    .screens .shot { width: 100%; max-width: 330px; }
    .screens figcaption { margin-top: var(--s3); font-size: 16px; line-height: 24px; color: var(--dim); max-width: 330px; }
    .screens figcaption b { display: block; font: 24px/28px var(--f-px); color: var(--ink); font-weight: 400; }

    .swatches { list-style: none; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: var(--s3); margin: var(--s4) 0 var(--s5); }
    .swatch { border: 6px solid transparent; border-image: var(--fr-soft) 6 fill / 6px / 0 stretch; padding: var(--s2); font-size: 14px; line-height: 20px; }
    .swatch i { display: block; height: 56px; margin-bottom: var(--s2); border: 2px solid var(--ink); }
    .swatch b { display: block; font: 20px/24px var(--f-px); color: var(--ink); font-weight: 400; }
    .type-demo { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--s4); margin-bottom: var(--s5); }
    /* these two boxes show the app's own light colours, so they must not take the theme's frame colour */
    .type-card { border: 2px solid var(--ink); border-image: none; padding: var(--s3) var(--s4); background: #ddede2; color: #000; }
    .type-card p { margin: 0; }
    .type-card .big { font-size: 32px; line-height: 40px; }
    .type-card .meta { font: 14px/20px 'DM Sans', var(--f-body); color: #4d4d4d; margin-top: var(--s2); }
    .serif { font-family: 'Playfair Display', Georgia, serif; font-weight: 700; }
    .sans { font-family: 'DM Sans', var(--f-body); }
    .components .shot { width: 100%; }
    .components figcaption { margin-top: var(--s3); font-size: 16px; line-height: 24px; color: var(--dim); max-width: 46em; }

    .decision { max-width: 44em; margin-top: var(--s5); }
    .decision:first-of-type { margin-top: var(--s4); }
    .decision h3 { font-size: 24px; line-height: 28px; }
    .decision p { margin-top: var(--s1); }
    .ticks { list-style: none; display: grid; gap: var(--s3); max-width: 46em; }
    .ticks li { position: relative; padding-left: var(--s5); }
    .ticks li::before { content: ''; position: absolute; left: 4px; top: 11px; width: 10px; height: 10px; background: var(--leaf-dot); }
    .ticks.issues li::before { background: var(--wheat); outline: 2px solid var(--ink); }

    .sec-tag { font: 20px/22px var(--f-px); color: var(--wheat-ink); margin-bottom: var(--s1); }
    .slots-h { margin-top: var(--s5); margin-bottom: var(--s3); }
    .slots { list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--s3); }
    .slot { border: 6px solid transparent; border-image: var(--fr-soft) 6 fill / 6px / 0 stretch; padding: var(--s2); min-height: 96px; text-align: center; font-size: 14px; line-height: 20px; color: var(--dim); }
    .slot b { display: block; font: 24px/28px var(--f-px); font-weight: 400; color: var(--ink); }
    .slot.empty { opacity: .45; }
    @media (pointer: coarse) { .cs-bar a.back, footer a { display: inline-block; padding: 10px 4px; } .cs-bar a.back { margin-left: -4px; } }
    footer { margin-top: var(--s8); padding: var(--s6) 0; background: var(--sky-2); }
    footer .container { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: var(--s3); }
    footer .container > p { margin: 0; }

    @media (max-width: 960px) {
      h1 { font-size: 80px; line-height: 72px; }
      .steps, .screens { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .slots { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .slot.empty { display: none; }
      .swatches { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    }
    @media (max-width: 640px) {
      .screens .shot { max-width: 260px; }
      .cs-lede { font-size: 19px; line-height: 30px; margin-top: var(--s3); }
      .container { width: calc(100% - 32px); }
      .cs-bar .cs-title { display: none; }
      .cs-bar .container { flex-wrap: nowrap; }
      h1 { font-size: 64px; line-height: 60px; }
      h2 { font-size: 34px; line-height: 36px; }
      section { padding-top: var(--s7); }
      .glance, .type-demo { grid-template-columns: 1fr; }
      .steps, .screens { grid-template-columns: 1fr; }
      .swatches { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .lead-quote { font-size: 28px; line-height: 32px; }
      .btn-game { flex: 1 1 auto; justify-content: center; }
    }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } * { animation: none !important; transition: none !important; } }
'''

IMG = 'assets/case-study/chi-matcha/'
def fig(n, file, title, text, alt):
    return f'''        <li><figure>
          <img class="shot" src="{IMG}{file}.webp" width="412" height="917" loading="lazy" alt="{alt}">
          <figcaption><b>{n}. {title}</b>{text}</figcaption>
        </figure></li>
'''
screens = ''.join([
    fig(1, 'login', 'Sign in', 'The logo, a Welcome Back heading, username and password fields, and a green Sign In button with a link to register.',
        'Chi Matcha sign-in screen: the logo, a Welcome Back heading, username and password fields, a green Sign In button and a Register link'),
    fig(2, 'register', 'Create an account', 'Join the Chi Matcha Family: username, password and confirm password.',
        'Create Account screen: Join the Chi Matcha Family, with username, password and confirm password fields and a green button'),
    fig(3, 'home', 'Home', 'A greeting, a cafe photo, and two big cards: Our Menu and Our Stores, then a short Why Chi Matcha? paragraph.',
        'Home screen: Good day, Welcome Guest, a cafe photo banner, Our Menu and Our Stores cards, and a Why Chi Matcha paragraph'),
    fig(4, 'menu', 'Our Menu', 'Five matcha drinks in a two-column grid, each with a photo, a name and a price.',
        'Our Menu screen: five matcha drinks in a two-column grid with photos, names and prices'),
    fig(5, 'item-detail', 'Item detail', 'Photo, price, description, Ice Level and Sweet Level dropdowns, quantity, optional notes and a Place Order button.',
        'Item detail for the Iced Matcha Latte: photo, price Rp. 45.000, description, Ice Level and Sweet Level dropdowns, quantity, notes and a Place Order button'),
    fig(6, 'branch', 'Our Stores', 'The branch with its address and opening hours (Chi Matcha - Kemang, 09:00 to 23:00).',
        'Our Stores screen listing Chi Matcha - Kemang with its address and opening hours 09:00 to 23:00'),
])

FIGMA = 'https://www.figma.com/design/XXO1QciNuYQYSa0wpI8P0k/User-Experience---AOL-Project---KelompokE'
GITHUB = 'https://github.com/JohnnyIsCodingSomething/UX-AOL-ChiMatcha'
PROTO = 'https://www.figma.com/proto/XXO1QciNuYQYSa0wpI8P0k/User-Experience---AOL-Project---KelompokE?node-id=14-20&amp;starting-point-node-id=14%3A20'

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Chi Matcha case study | Jonathan Richard</title>
  <meta name="description" content="Chi Matcha, a mobile cafe ordering app: designed in Figma, then built as an Android app in Java. A case study by Jonathan Richard." />
  <meta name="author" content="Jonathan Richard" />
  <meta name="theme-color" content="#a6d3ee" />
  <link rel="canonical" href="https://johnnyiscodingsomething.github.io/chi-matcha.html" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://johnnyiscodingsomething.github.io/chi-matcha.html" />
  <meta property="og:title" content="Chi Matcha case study | Jonathan Richard" />
  <meta property="og:description" content="A mobile cafe ordering app, designed in Figma and built in Java." />
  <meta property="og:image" content="https://johnnyiscodingsomething.github.io/assets/design/chi-matcha-og.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="722" />
  <meta property="og:image:alt" content="Chi Matcha app screens in the pixel-art portfolio style" />
  <meta name="twitter:title" content="Chi Matcha case study | Jonathan Richard" />
  <meta name="twitter:description" content="A mobile cafe ordering app, designed in Figma and built in Java." />
  <meta name="twitter:image" content="https://johnnyiscodingsomething.github.io/assets/design/chi-matcha-og.png" />
  ICONLINK
  <script>try { var t = localStorage.getItem('theme'); if (t === 'dark' || (t === null && matchMedia('(prefers-color-scheme: dark)').matches)) document.documentElement.setAttribute('data-theme', 'dark'); } catch (e) {}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Jersey+10&family=Golos+Text:wght@400;500;600&family=Playfair+Display:wght@700&family=DM+Sans:wght@400;700&display=swap" rel="stylesheet" />
  <style>
/*TOKENS*/
/*CSS*/
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="cs-bar">
    <div class="container">
      <a class="back" href="index.html#design">&larr; Back to my portfolio</a>
      <div class="cs-bar-tools">
        <span class="cs-title">Case study</span>
        <button type="button" class="btn-game" id="themeBtn">Dark mode</button>
      </div>
    </div>
  </header>

  <main id="main">
    <section class="cs-hero container" aria-labelledby="top">
      <p class="cs-kicker">Case study &middot; User Experience course &middot; Team project</p>
      <h1 id="top">Chi Matcha</h1>
      <p class="cs-lede">A mobile cafe ordering app. I designed it in Figma, then built it as an Android app in Java.</p>
      <ul class="chips" aria-label="Tools and topics">
        <li class="chip">Figma</li><li class="chip">UX</li><li class="chip">Android</li><li class="chip">Java</li>
      </ul>
      <div class="cs-actions">
        <a class="btn-game btn-primary-g" href="PROTO" target="_blank" rel="noopener noreferrer" aria-label="Try the Chi Matcha clickable prototype in Figma (opens in a new tab)">Try the prototype</a>
        <a class="btn-game" href="FIGMA" target="_blank" rel="noopener noreferrer" aria-label="View Chi Matcha in Figma (opens in a new tab)">View in Figma</a>
        <a class="btn-game" href="GITHUB" target="_blank" rel="noopener noreferrer" aria-label="View the Chi Matcha code on GitHub (opens in a new tab)">View Code on GitHub</a>
      </div>
      <picture>
        <img class="shot" src="assets/design/chi-matcha-large.webp" width="1600" height="962" alt="Chi Matcha app screens in Figma: the sign-in screen, the home screen with a cafe photo and Menu and Stores buttons, and the menu of matcha drinks with prices">
      </picture>
    </section>

    <section class="container" aria-labelledby="glance-h">
      <p class="sec-tag">Inventory</p>
      <h2 id="glance-h">At a glance</h2>
      <dl class="glance">
        <div><dt>My role</dt><dd>I designed most of the app's screens and components in Figma, and then built it in Java, working with my team.</dd></div>
        <div><dt>Team</dt><dd>Team project, team of 3.</dd></div>
        <div><dt>Course</dt><dd>User Experience, BINUS University.</dd></div>
        <div><dt>Tools</dt><dd>Figma for the design. Android Studio and Java for the build.</dd></div>
      </dl>
      <h3 class="slots-h">Tools in my bag</h3>
      <ul class="slots">
        <li class="slot"><b>Figma</b>screens and components</li>
        <li class="slot"><b>Android Studio</b>the app build</li>
        <li class="slot"><b>Java</b>the app code</li>
        <li class="slot"><b>UX</b>the course</li>
        <li class="slot empty" aria-hidden="true"></li><li class="slot empty" aria-hidden="true"></li><li class="slot empty" aria-hidden="true"></li><li class="slot empty" aria-hidden="true"></li>
      </ul>
    </section>

    <section class="container" aria-labelledby="problem-h">
      <p class="sec-tag">Crafting table</p>
      <h2 id="problem-h">The problem</h2>
      <p class="lead-quote">Ordering a customized drink at a cafe is slow.</p>
      <p>The idea: the app lets people pick a branch, browse the menu, and set ice and sugar levels before ordering.</p>
      <p class="note">This was the team's starting point. It is not something I measured with user research.</p>
    </section>

    <section class="container" aria-labelledby="flow-h">
      <h2 id="flow-h">The path through the app</h2>
      <ol class="steps">
        <li><h3>Sign in</h3><p>Sign in, or create an account first.</p></li>
        <li><h3>Home</h3><p>Choose Our Menu or Our Stores.</p></li>
        <li><h3>Pick a drink</h3><p>Five matcha drinks, each with a photo and a price.</p></li>
        <li><h3>Customize</h3><p>Set the ice level and the sweet level.</p></li>
        <li><h3>Details</h3><p>Add a quantity and optional notes.</p></li>
        <li><h3>Order</h3><p>Place the order.</p></li>
      </ol>
      <p class="note">Our Stores is a separate branch page with the address and opening hours.</p>
    </section>

    <section class="container" aria-labelledby="why-h">
      <h2 id="why-h">Why it works this way</h2>
      <div class="decision">
        <h3>Ice and sugar on every drink page</h3>
        <p>People often ask for less sugar or less ice. Setting it in the app, right on the drink, means fewer mistakes than telling the staff at the counter. The course brief also asked for drink customization, so we made each option a dropdown component with its own states.</p>
      </div>
      <div class="decision">
        <h3>A page for the branches</h3>
        <p>An order for pickup needs a place, and a branch can have different items or stock. Real cafe ordering apps we looked at show their branches, and the brief asked for it too, so Our Stores lists each branch with its address and opening hours.</p>
      </div>
      <div class="decision">
        <h3>A calm green style</h3>
        <p>Green is the color of matcha, the cafe's main product. The team picked the look from a moodboard: a soft sage background, white cards, and green only for buttons and prices, so the important parts stand out and the page feels calm, like a cafe.</p>
      </div>
      <div class="decision">
        <h3>What was hard</h3>
        <p>Agreeing on the order of the screens, from sign-in to placing an order. Keeping buttons, cards and spacing the same on every screen. Fitting the drink options on a small phone screen without clutter. And linking every screen in Figma so the prototype can be clicked through.</p>
      </div>
    </section>

    <section class="container" aria-labelledby="screens-h">
      <p class="sec-tag">Chest</p>
      <h2 id="screens-h">The screens</h2>
      <ul class="screens">
SCREENS      </ul>
      <p class="note">Each of the five drinks (Iced Matcha Latte, Hot Matcha Latte, Matcha Affogato, Matcha Tiramisu and Matcha Smoothie) has its own item page with the same layout.</p>
    </section>

    <section class="container" aria-labelledby="system-h">
      <h2 id="system-h">What the design file shows</h2>
      <h3>Colors</h3>
      <ul class="swatches">
        <li class="swatch"><i style="background:#DDEDE2"></i><b>#DDEDE2</b>Soft sage page background</li>
        <li class="swatch"><i style="background:#3F835B"></i><b>#3F835B</b>Green for buttons and prices</li>
        <li class="swatch"><i style="background:#FFFFFF"></i><b>#FFFFFF</b>Cards and input fields</li>
        <li class="swatch"><i style="background:#000000"></i><b>#000000</b>Headings</li>
        <li class="swatch"><i style="background:#8C8C8C"></i><b>#8C8C8C</b>Grey labels</li>
      </ul>
      <h3>Type</h3>
      <div class="type-demo" style="margin-top:16px">
        <div class="type-card"><p class="big serif">Iced Matcha Latte</p><p class="meta">Playfair Display Bold, for titles. Two heading styles.</p></div>
        <div class="type-card"><p class="big sans">Ice Level, Quantity, Notes</p><p class="meta">DM Sans Regular and Bold, for body text and labels. Three text styles.</p></div>
      </div>
      <h3>Components</h3>
      <figure class="components" style="margin-top:16px">
        <img class="shot" src="assets/case-study/chi-matcha/dropdown-states.webp" width="1994" height="353" loading="lazy" alt="The ice level dropdown component in its states: closed with a Select placeholder, open with four options (No Ice, Less ice, Normal ice, Extra Ice), a selected state for each option, and a list item hover state">
        <figcaption>The ice level dropdown, built as a component with six states: closed, open with four options (No Ice, Less ice, Normal ice, Extra Ice), and one selected state for each option. The sweet level dropdown has a matching set, and the list items have a hover state.</figcaption>
      </figure>
    </section>

    <section class="container" aria-labelledby="build-h">
      <h2 id="build-h">Building it in Java</h2>
      <ul class="ticks">
        <li>Login and registration with validation.</li>
        <li>A home page with an image carousel.</li>
        <li>Menu browsing with item details.</li>
        <li>Orders customized by ice level and sweetness level.</li>
        <li>A branch location page.</li>
      </ul>
    </section>

    <section class="container" aria-labelledby="improve-h">
      <p class="sec-tag">Quest board</p>
      <h2 id="improve-h">What I would improve next</h2>
      <p style="max-width:44em;margin-bottom:24px">I found these when I reviewed the file again for this page.</p>
      <ul class="ticks issues">
        <li><b>Prices do not match.</b> The item pages for the other four drinks still show Rp. 45.000, while the menu lists different prices (Matcha Affogato is Rp. 55.000 on the menu).</li>
        <li><b>Typos in the copy.</b> The Home screen text has &ldquo;mmfor&rdquo; and &ldquo;yyou&rdquo;.</li>
        <li><b>Low contrast on the grey labels.</b> Labels such as &ldquo;Ice Level&rdquo; use #8C8C8C on the sage background, about 2.8 to 1. The common guideline for small text is 4.5 to 1, so I would darken them.</li>
        <li><b>Dropdown positions.</b> The Ice and Sweet dropdowns sit at slightly different positions from one item page to the next.</li>
        <li><b>Empty space.</b> The Home and Our Stores screens leave a lot of unused space at the bottom.</li>
        <li><b>Branch before the menu.</b> Since items and stock can differ by branch, I would ask for the branch first, so the menu always matches the store you pick up from.</li>
        <li><b>Real users.</b> I have not tested the ordering flow with real users yet. That would be the first thing I do next.</li>
      </ul>
    </section>
  </main>

  <footer>
    <div class="container">
      <p>Designed and built by Jonathan Richard.</p>
      <p><a href="index.html#design">&larr; Back to my portfolio</a> &middot; <a href="index.html#contact">Contact</a></p>
    </div>
  </footer>

  <script>
    (function () {
      var btn = document.getElementById('themeBtn');
      function paint() { var d = document.documentElement.getAttribute('data-theme') === 'dark'; btn.textContent = d ? 'Light mode' : 'Dark mode'; }
      btn.addEventListener('click', function () {
        var d = document.documentElement.getAttribute('data-theme') === 'dark';
        if (d) document.documentElement.removeAttribute('data-theme'); else document.documentElement.setAttribute('data-theme', 'dark');
        try { localStorage.setItem('theme', d ? 'light' : 'dark'); } catch (e) {}
        paint();
      });
      paint();
    })();
  </script>
</body>
</html>
'''
html = HTML.replace('ICONLINK', ICON).replace('/*TOKENS*/', TOKENS).replace('/*CSS*/', CSS).replace('SCREENS', screens).replace('href="FIGMA"', f'href="{FIGMA}"').replace('href="PROTO"', f'href="{PROTO}"').replace('href="GITHUB"', f'href="{GITHUB}"')
open(os.path.join(root, 'chi-matcha.html'), 'w', encoding='utf-8').write(html)
print('written', len(html) // 1024, 'KB')
