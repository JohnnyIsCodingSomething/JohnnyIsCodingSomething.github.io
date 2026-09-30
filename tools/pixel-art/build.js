// Pixel-art generator for the CV site: the floating farm island, the portrait, and the
// stepped pixel frames (border-image SVGs) for both themes. Sprites are ASCII art below.
// usage:  node tools/pixel-art/build.js            (rewrites the marked blocks in index.html)
//         node tools/pixel-art/build.js --zoom     (also writes a 10x art sheet: zoom.html; add --dark for night)
const fs = require('fs'), path = require('path');
const dir = __dirname;

/* ───────────── palette (day) ───────────── */
const DAY = {
  g: '#8cc35c', d: '#6fa548', l: '#a9d677',          // grass, grass dark, grass light
  t: '#9a6843', f: '#74482c',                         // tilled soil, furrow
  c1: '#8d5d3b', c2: '#6c4329', c3: '#4b2d1b',        // cliff face
  p: '#e3cc9e', P: '#c9ab78',                         // path
  w: '#c38c56', W: '#8a5b34', v: '#dcaa72',           // wood, wood dark, wood light
  L: '#4f9a3c', D: '#2f6f2c', k: '#7cc25a',           // leaf, leaf dark, leaf light
  Y: '#f0c552', y: '#c48f31',                         // wheat
  O: '#ea8b3b', o: '#b8612a',                         // pumpkin
  '1': '#4f913f', '2': '#386f31', '3': '#76b353',     // tree canopy
  H: '#1c1b20', h: '#3d3a45', S: '#e2b48b', K: '#18171b', E: '#f3d6ba', e: '#18171b', r: '#a9534a',
  M: '#7c2335', m: '#5a1826', n: '#a23a4c', Q: '#3a3e55', B: '#2a2527',
  C: '#fbf8ee', c: '#d9d0bf', R: '#d8473a', b: '#e9ae3c', // chicken
  X: '#3b3437', A: '#fbe7a6',                         // lantern metal, lantern glass (unlit)
  U: '#ffffff', u: '#dce8ec',                         // cloud
  Z: '#fff6c9', z: '#f2d77a',                         // night-only: stars / glow
};
// Night: pull every colour toward a blue dusk, keep a few lit things bright.
const NIGHT_BASE = [0x1b, 0x2a, 0x46];
const hex = c => c.replace('#', '').match(/../g).map(h => parseInt(h, 16));
const toHex = a => '#' + a.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
const nightify = (c, k = 0.5) => toHex(hex(c).map((v, i) => v * (1 - k) * 0.95 + NIGHT_BASE[i] * k));
const NIGHT = {};
for (const [key, c] of Object.entries(DAY)) NIGHT[key] = nightify(c);
// Crops, grass and soil keep more of their colour at night so the beds still read (moonlit, not muddy).
for (const key of ['g', 'd', 'l', 't', 'f', 'p', 'P', 'Y', 'y', 'O', 'o', 'L', 'D', 'k', '1', '2', '3', 'C', 'c', 'R', 'b', 'M', 'm', 'n', 'S', 'E'])
  NIGHT[key] = nightify(DAY[key], 0.3);
Object.assign(NIGHT, { A: '#ffd257', Z: '#fff3b8', z: '#6d7d4c', U: '#34445f', u: '#2c3a55', H: '#141318', h: '#2c2a33', K: '#101014', e: '#101014' });

/* ───────────── canvas helpers ───────────── */
function Canvas(w, h) { const px = Array.from({ length: h }, () => Array(w).fill(null)); return { w, h, px }; }
function put(cv, x, y, k) { if (x >= 0 && y >= 0 && x < cv.w && y < cv.h && k) cv.px[y][x] = k; }
// sprite rows: tokens separated by spaces or single chars; '.' = transparent. Multi-char keys use spaces.
function sprite(rows) { return rows.map(r => (r.includes(' ') ? r.trim().split(/\s+/) : r.split(''))); }
function stamp(cv, spr, x0, y0) { spr.forEach((row, y) => row.forEach((k, x) => { if (k !== '.') put(cv, x0 + x, y0 + y, k); })); }
// Pseudo-random, deterministic
let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);

// Run-length paths, one per colour
function toPaths(cv, clsPrefix = 'c-') {
  const byKey = {};
  for (let y = 0; y < cv.h; y++) {
    let x = 0;
    while (x < cv.w) {
      const k = cv.px[y][x];
      if (!k) { x++; continue; }
      let e = x; while (e + 1 < cv.w && cv.px[y][e + 1] === k) e++;
      (byKey[k] = byKey[k] || []).push(`M${x} ${y}h${e - x + 1}v1h-${e - x + 1}z`);
      x = e + 1;
    }
  }
  return Object.entries(byKey).map(([k, d]) => `<path class="${clsPrefix}${cls(k)}" d="${d.join('')}"/>`).join('');
}
const cls = k => ({ '1': 't1', '2': 't2', '3': 't3' }[k] || (/^[A-Z]$/.test(k) ? 'u' + k.toLowerCase() : k));

/* ───────────── sprites ───────────── */
const S = {
  // crops (5 wide, bottom-aligned on the bed)
  seed:     sprite(['.....', '..y..']),
  sprout:   sprite(['.k.k.', '..L..', '..D..']),
  young:    sprite(['k...k', '.L.L.', 'L.k.L', '.DLD.', '..D..']),
  wheat:    sprite(['..Y..', 'Y.Y.Y', 'Y.Y.Y', 'y.y.y', '.yyy.', '.DyD.', '..D..']),
  cabbage:  sprite(['.DkD.', 'DkLkD', 'LkLkL', 'DLkLD', '.DDD.']),
  pumpkin:  sprite(['..Dk.', '.OOO.', 'OoOoO', 'OoOoO', '.ooo.']),
  // player, 11 x 18, facing the viewer
  player: sprite([
    '...HHHHH...',
    '..HHhhHHH..',
    '.HHhHHHHHH.',
    '.HHHHHHHHH.',
    '.HHSSHSSHH.',
    '.KKKSSSKKK.',   // glasses: thin rims, light lenses, a pupil in each
    'KEEEKKKEEEK',
    'KEeESSSEeEK',
    '.KKKSSSKKK.',
    '..SSSSSSS..',
    '...SSrSS...',
    '..MnSSSnM..',
    '.MMMnSnMMM.',
    'MMMMMMMMMMM',
    'SmMMMMMMMmS',
    '..QQQQQQQ..',
    '..QQQ.QQQ..',
    '..BBB.BBB..',
  ]),
  chicken: sprite([
    '..R....',
    '.CCc...',
    'bCKC...',
    '.CCCCCc',
    '.cCCCCc',
    '..cccc.',
    '..b..b.',
  ]),
  lantern: sprite([
    '.XX.',
    'XAAX',
    'XAAX',
    '.XX.',
    '.wW.',
    '.wW.',
    '.wW.',
    '.wW.',
    '.wW.',
    'WwWW',
  ]),
  cloudA: sprite([
    '....UUU.......',
    '..UUUUUUU.UU..',
    '.UUUUUUUUUUUU.',
    'uUUUUUUUUUUUUu',
    '.uuuuuuuuuuuu.',
  ]),
  cloudB: sprite([
    '...UUU...',
    '.UUUUUUU.',
    'uUUUUUUUu',
    '.uuuuuuu.',
  ]),
  tuft: sprite(['d.d', '.d.']),
};

/* ───────────── the island ───────────── */
function buildFarm() {
  const W = 104, H = 76;
  const base = Canvas(W, H);
  // island top bounds per row
  const top = 10, bottom = 58;
  // a pixel-rounded rectangle: the corners step in over four rows
  const bounds = y => {
    const inset = [10, 6, 4, 2, 1, 1];
    const i = Math.min(y - top, bottom - y);
    const d = i < inset.length ? inset[i] : 0;
    return [7 + d, 96 - d];
  };
  const inside = (x, y) => y >= top && y <= bottom && x >= bounds(y)[0] && x <= bounds(y)[1];
  const lowest = []; // lowest grass row per column
  for (let y = top; y <= bottom; y++) {
    const [a, b] = bounds(y);
    for (let x = a; x <= b; x++) { put(base, x, y, 'g'); lowest[x] = y; }
  }
  // the floating underside: a straight earth band that tapers to a rocky keel
  const cx = 51.5, hw = 45;
  let jitter = 0;
  for (let x = 7; x <= 96; x++) {
    const y0 = lowest[x];
    const t = Math.abs(x - cx) / hw;                      // 0 centre … 1 edge
    if (x % 3 === 0) jitter = Math.round(rnd() * 2) - 1;  // lumpy, but in 3px steps
    const depth = Math.max(3, Math.round(5 + 10 * (1 - t * t) + jitter));
    for (let i = 1; i <= depth; i++) {
      const y = y0 + i;
      let k = 'c1';
      if (i === 1) k = 'd';                          // grass lip
      else if (i === 2) k = 'c1';
      else if (i === 4 || i === 8) k = 'c2';         // strata
      else if (i >= depth - 1) k = 'c3';             // shadowed keel
      else if (i > 9) k = 'c2';
      put(base, x, y, k);
    }
    if (x % 13 === 5) { put(base, x, y0 + depth + 1, 'c3'); if (rnd() > .5) put(base, x, y0 + depth + 2, 'c3'); } // roots
  }
  // a few stones in the earth band
  [[20, 63], [34, 66], [47, 68], [60, 67], [73, 64], [85, 62], [55, 71]].forEach(([x, y]) => { if (base.px[y][x] && base.px[y][x].startsWith('c')) { put(base, x, y, 'c3'); put(base, x + 1, y, 'c2'); } });
  // edge light on the north / west rim, dark on the east rim
  for (let y = top; y <= bottom; y++) {
    const [a, b] = bounds(y);
    put(base, a, y, 'l');
    put(base, b, y, 'd');
  }
  for (let x = 0; x < W; x++) {
    for (let y = top; y <= bottom; y++) if (inside(x, y)) { if (!inside(x, y - 1)) put(base, x, y, 'l'); break; }
  }
  // grass texture: tufts and light specks
  for (let i = 0; i < 70; i++) {
    const x = 9 + Math.floor(rnd() * 84), y = 13 + Math.floor(rnd() * 42);
    if (inside(x, y) && inside(x + 2, y + 1)) stamp(base, S.tuft, x, y);
  }
  for (let i = 0; i < 40; i++) {
    const x = 9 + Math.floor(rnd() * 84), y = 12 + Math.floor(rnd() * 44);
    if (inside(x, y) && base.px[y][x] === 'g') put(base, x, y, 'l');
  }

  // path: from the south edge up to the plot
  const pathPx = (x, y) => {
    const edge = (x + y) % 3 === 0 ? 'P' : 'p';
    put(base, x, y, edge);
  };
  for (let y = 40; y <= 58; y++) for (let x = 27; x <= 32; x++) if (inside(x, y)) pathPx(x, y);
  for (let y = 40; y <= 45; y++) for (let x = 27; x <= 46; x++) pathPx(x, y);
  // path border darkening for definition
  for (let y = 40; y <= 58; y++) { if (inside(26, y) && y > 45) put(base, 26, y, 'd'); if (inside(33, y) && y > 46) put(base, 33, y, 'd'); }
  for (let x = 34; x <= 46; x++) { put(base, x, 39, 'd'); put(base, x, 46, 'd'); }

  // tree shadow (dither) + tree
  for (let y = 27; y <= 32; y++) for (let x = 10; x <= 30; x++) {
    const dx = (x - 20) / 10, dy = (y - 30) / 3;
    if (dx * dx + dy * dy <= 1 && (x + y) % 2 === 0) put(base, x, y, 'd');
  }
  for (let y = 25; y <= 30; y++) for (let x = 18; x <= 21; x++) put(base, x, y, x === 21 ? 'W' : 'w');
  put(base, 17, 30, 'W'); put(base, 22, 30, 'W');
  for (let y = 9; y <= 27; y++) for (let x = 9; x <= 31; x++) {
    const dx = (x - 20) / 11.2, dy = (y - 18) / 9.4;
    const r = dx * dx + dy * dy;
    if (r > 1) continue;
    let k = '1';
    if (dx + dy > 0.55 || r > 0.8 && dy > 0.2) k = '2';
    else if (dx + dy < -0.6 || (r < 0.35 && dx < -0.1 && dy < -0.1)) k = '3';
    // lumpy edge
    if (r > 0.86 && (x * 3 + y) % 4 === 0) continue;
    put(base, x, y, k);
  }
  // a few leaf clusters for texture
  [[14, 14], [22, 12], [25, 17], [16, 20], [22, 21]].forEach(([x, y]) => { put(base, x, y, '3'); put(base, x + 1, y, '3'); put(base, x, y + 1, '1'); });
  [[26, 22], [19, 24], [28, 18]].forEach(([x, y]) => { put(base, x, y, '2'); put(base, x - 1, y + 1, '2'); });

  // fence along the north side
  const fy = 13;
  for (let x = 36; x <= 92; x++) {
    put(base, x, fy + 1, 'v'); put(base, x, fy + 2, 'W');
    put(base, x, fy + 4, 'v'); put(base, x, fy + 5, 'W');
  }
  for (let x = 36; x <= 92; x += 8) {
    put(base, x, fy - 1, 'v'); put(base, x + 1, fy - 1, 'v');
    for (let y = fy; y <= fy + 6; y++) { put(base, x, y, 'w'); put(base, x + 1, y, 'W'); }
    put(base, x, fy + 7, 'd'); put(base, x + 1, fy + 7, 'd');
  }

  // tilled beds
  const beds = [24, 32, 40, 48], bx0 = 49, bx1 = 92;
  beds.forEach(by => {
    for (let y = by; y < by + 5; y++) for (let x = bx0; x <= bx1; x++) put(base, x, y, y === by + 4 || x === bx1 ? 'f' : 't');
    for (let x = bx0 + 1; x < bx1; x += 3) put(base, x, by + 2, 'f');       // furrow marks
  });

  // lantern beside the path, below the bend
  const LX = 36, LY = 47;
  put(base, LX + 1, LY + 10, 'd'); put(base, LX + 3, LY + 10, 'd'); put(base, LX + 4, LY + 9, 'd'); // shadow
  stamp(base, S.lantern, LX, LY);

  // chicken
  for (let x = 13; x <= 20; x++) if ((x) % 2 === 0) put(base, x, 51, 'd'); // shadow
  stamp(base, S.chicken, 13, 45);

  // player on the path, facing the viewer
  for (let x = 28; x <= 38; x++) if (x % 2 === 1) put(base, x, 44, 'P');
  stamp(base, S.player, 28, 26);

  // flowers
  [[12, 38], [16, 41], [44, 53], [60, 56], [84, 56], [9, 47], [41, 20], [90, 12]].forEach(([x, y]) => { if (inside(x, y)) { put(base, x, y, 'C'); if (inside(x, y + 1)) put(base, x, y + 1, 'L'); } });

  // clouds (sky decoration)
  stamp(base, S.cloudA, 88, 2);
  stamp(base, S.cloudB, 0, 2);

  // crops: rows × stages, drawn on their own layers so they can "grow"
  const types = ['wheat', 'cabbage', 'wheat', 'pumpkin'];
  const stages = ['seed', 'sprout', 'young'];
  const cols = [51, 58, 65, 72, 79, 86];
  let crops = '';
  beds.forEach((by, r) => {
    for (let s = 0; s < 4; s++) {
      const cv = Canvas(W, H);
      cols.forEach(cx => {
        const spr = s < 3 ? S[stages[s]] : S[types[r]];
        stamp(cv, spr, cx, by + 3 - spr.length + 1);
      });
      crops += `<g class="st s${s}" style="--r:${r}">${toPaths(cv)}</g>`;
    }
  });

  // night-only: lantern glow (dither ring), fireflies and stars
  const night = Canvas(W, H);
  const ground = /^(g|d|l|p|P)$/;
  for (let y = LY - 6; y <= LY + 14; y++) for (let x = LX - 12; x <= LX + 16; x++) {
    const dx = (x - (LX + 1.5)) / 12, dy = (y - (LY + 5)) / 8;
    const r = dx * dx + dy * dy, k = base.px[y] && base.px[y][x];
    if (!k || !ground.test(k) || r > 1) continue;
    if (r < 0.4 ? (x + y) % 2 === 0 : (x % 2 === 0 && y % 2 === 0)) put(night, x, y, 'z');
  }
  [[4, 9], [30, 3], [60, 5], [74, 1], [100, 30], [2, 30], [99, 50], [3, 60], [100, 66]].forEach(([x, y]) => put(night, x, y, 'Z'));   // stars
  [[60, 21], [84, 30], [70, 38], [56, 46]].forEach(([x, y]) => put(night, x, y, 'Z'));                                               // fireflies

  const svg = `<svg class="farm" viewBox="0 0 ${W} ${H}" width="${W * 5}" height="${H * 5}" shape-rendering="crispEdges" role="img" aria-label="Pixel-art farm: a small floating island with a fence, a tree, a chicken, four tilled beds of wheat, cabbage and pumpkins, and Jonathan standing on the path.">`
    + `<g class="base">${toPaths(base)}</g><g class="crops">${crops}</g><g class="night-only">${toPaths(night)}</g></svg>`;
  return { svg, W, H };
}

/* ───────────── portrait (16×16) ───────────── */
function buildAvatar() {
  const rows = [
    '................',
    '....HHHHHHHH....',
    '...HHhhHHHHHH...',
    '..HHhHHHHHHHHH..',
    '..HHSHHHHHSHHH..',
    '..HSSSSSSSSSSH..',
    '..KKKKKSSKKKKK..',
    '.SKEeEKKKKEeEKS.',
    '.SKEeEKSSKEeEKS.',
    '..KKKKKSSKKKKK..',
    '..SSSSSSSSSSSS..',
    '...SSSSrrSSSS...',
    '....SSSSSSSS....',
    '...MnnSSSSnnM...',
    '.MMMMMnSSnMMMMM.',
    'MMMMMMMnnMMMMMMM',
  ];
  const map = { H: 'av-hair', h: 'av-hair-hi', S: 'av-skin', E: 'av-lens', e: 'av-eye', r: 'av-mouth', M: 'av-top', K: 'av-rim', n: 'av-collar' };
  const by = {};
  rows.forEach((row, y) => {
    let x = 0;
    while (x < 16) {
      const k = row[x];
      if (k === '.') { x++; continue; }
      let e = x; while (e + 1 < 16 && row[e + 1] === k) e++;
      (by[k] = by[k] || []).push(`M${x} ${y}h${e - x + 1}v1h-${e - x + 1}z`);
      x = e + 1;
    }
  });
  return `<svg class="avatar" viewBox="0 0 16 16" width="64" height="64" shape-rendering="crispEdges" role="img" aria-label="Pixel-art portrait of Jonathan: black hair, dark-rimmed rectangular glasses, maroon collared shirt">`
    + Object.entries(by).map(([k, d]) => `<path class="${map[k]}" d="${d.join('')}"/>`).join('') + '</svg>';
}

/* ───────────── stepped pixel frames (border-image) ───────────── */
// 8×8 units of 2px: pixel-rounded rectangle with a 1-unit outline. Slice = 3 units (6px).
function frame(outline, fill) {
  const o = [], f = [];
  const O = (x, y, w = 1) => o.push(`M${x * 2} ${y * 2}h${w * 2}v2h-${w * 2}z`);
  const F = (x, y, w) => f.push(`M${x * 2} ${y * 2}h${w * 2}v2h-${w * 2}z`);
  O(2, 0, 4); O(1, 1); O(6, 1); for (let y = 2; y <= 5; y++) { O(0, y); O(7, y); } O(1, 6); O(6, 6); O(2, 7, 4);
  F(2, 1, 4); for (let y = 2; y <= 5; y++) F(1, y, 6); F(2, 6, 4);
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' shape-rendering='crispEdges'>`
    + (fill ? `<path fill='${fill}' d='${f.join('')}'/>` : '') + `<path fill='${outline}' d='${o.join('')}'/></svg>`;
  return `url("data:image/svg+xml,${svg.replace(/#/g, '%23').replace(/</g, '%3C').replace(/>/g, '%3E')}")`;
}

const THEME = {
  light: { page: '#eef3ef', panel: '#fbfcf8', ink: '#2e2419', line: '#c9d0c6', tint: '#e2e9e1', wheat: '#efc24e', wheatHi: '#f6d77f' },
  dark:  { page: '#1a2436', panel: '#223047', ink: '#eef0e4', line: '#3c4b64', tint: '#2a3a54', wheat: '#efc24e', wheatHi: '#f6d77f' },
};
function frameVars(t, dark) {
  return [
    `--fr-panel: ${frame(t.ink, t.panel)};`,
    `--fr-soft: ${frame(t.line, t.panel)};`,
    `--fr-slot: ${frame(t.line, t.tint)};`,
    `--fr-tag: ${frame(t.tint, t.tint)};`,
    `--fr-btn: ${frame(dark ? '#0f1522' : t.ink, t.wheat)};`,
    `--fr-btn-hi: ${frame(dark ? '#0f1522' : t.ink, t.wheatHi)};`,
    `--fr-btn2: ${frame(t.ink, t.panel)};`,
    `--fr-key: ${frame(t.line, t.panel)};`,
  ].join('\n      ');
}

function farmCss() {
  const keys = Object.keys(DAY);
  const rule = (pal) => keys.map(k => `--f-${cls(k)}: ${pal[k]};`).join(' ');
  const fills = keys.map(k => `.farm .c-${cls(k)} { fill: var(--f-${cls(k)}); }`).join('\n    ');
  return `:root { ${rule(DAY)} }\n    :root[data-theme="dark"] { ${rule(NIGHT)} }\n    ${fills}`;
}

// ───────────── output ─────────────
// The generated pieces live in index.html between marker comments, e.g.
//   <!--gen:farm--> … <!--/gen:farm-->   and   /*gen:farmcss*/ … /*/gen:farmcss*/
// Running this script replaces only what is between the markers, so the rest of
// index.html can be edited by hand as usual.
const args = process.argv.slice(2);
const argVal = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const target = path.resolve(argVal('--target') || path.join(dir, '..', '..', 'index.html'));
const farm = buildFarm();
const blocks = {
  farm: ['html', farm.svg],
  avatar: ['html', buildAvatar()],
  farmcss: ['css', farmCss()],
  'frames-light': ['css', frameVars(THEME.light, false)],
  'frames-dark': ['css', frameVars(THEME.dark, true)],
};
const wrap = (kind, k, v) => kind === 'html' ? `<!--gen:${k}-->${v}<!--/gen:${k}-->` : `/*gen:${k}*/\n      ${v}\n      /*/gen:${k}*/`;
const esc = s => s.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&');

let page;
const existing = fs.existsSync(target) ? fs.readFileSync(target, 'utf8') : '';
if (existing.includes('<!--gen:farm-->')) {
  // patch mode: refresh the generated blocks in place
  page = existing;
  for (const [k, [kind, v]] of Object.entries(blocks)) {
    const [a, b] = kind === 'html' ? [`<!--gen:${k}-->`, `<!--/gen:${k}-->`] : [`/*gen:${k}*/`, `/*/gen:${k}*/`];
    const re = new RegExp(esc(a) + '[\\s\\S]*?' + esc(b));
    if (!re.test(page)) throw new Error('marker block missing in ' + target + ': ' + k);
    page = page.replace(re, () => wrap(kind, k, v));
  }
} else {
  // first build: fill the placeholders of page.src.html
  page = fs.readFileSync(path.join(dir, 'page.src.html'), 'utf8')
    .replace('<!--ICONS-->', () => fs.readFileSync(path.join(dir, 'icons.html'), 'utf8'))
    .replace('<!--FARM-->', () => wrap('html', 'farm', farm.svg))
    .replace('<!--AVATAR-->', () => wrap('html', 'avatar', buildAvatar()))
    .replace('/*FARMCSS*/', () => wrap('css', 'farmcss', farmCss()))
    .replace('/*FRAMES-LIGHT*/', () => wrap('css', 'frames-light', frameVars(THEME.light, false)))
    .replace('/*FRAMES-DARK*/', () => wrap('css', 'frames-dark', frameVars(THEME.dark, true)));
}
fs.writeFileSync(target, page);
console.log('wrote', target, page.length, 'bytes; farm svg', farm.svg.length, 'bytes');

// optional: a zoomed art sheet to review the sprites (node build.js --zoom [--dark])
if (args.includes('--zoom')) {
  const dark = args.includes('--dark');
  const avatarCss = (page.match(/\.av-hair \{[^\n]*\n[^\n]*\n/) || [''])[0];
  const file = path.join(dir, dark ? 'zoom-dark.html' : 'zoom.html');
  fs.writeFileSync(file, `<!doctype html><html${dark ? ' data-theme="dark"' : ''}><head><style>${farmCss()} ${avatarCss}
body{margin:0;padding:20px;display:flex;gap:20px;align-items:flex-start;background:${dark ? '#1a2436' : '#eef3ef'}}
.farm{width:${farm.W * 10}px;height:${farm.H * 10}px}.avatar{width:256px;height:256px;background:#e2e9e1}.farm .st{opacity:0}.farm .st.s3{opacity:1}
.night-only{display:none}[data-theme=dark] .night-only{display:inline}</style></head><body>${farm.svg}${buildAvatar()}</body></html>`);
  console.log('zoom sheet:', file);
}
