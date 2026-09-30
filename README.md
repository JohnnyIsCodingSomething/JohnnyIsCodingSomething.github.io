# Jonathan Richard — CV website

Personal CV site, live at https://johnnyiscodingsomething.github.io/

- `index.html` — the whole site (inline CSS and JavaScript, no build step). Edit it directly.
- `Jonathan_Richard_CV.pdf` — the downloadable one-page CV, printed from `cv-print.html`.
- `tools/pixel-art/build.js` — generates the pixel-art farm island, portrait and pixel frames from ASCII sprites. Run `node tools/pixel-art/build.js` after editing a sprite; it only rewrites the `<!--gen:…-->` blocks inside `index.html`. Add `--zoom` to get an enlarged art sheet for checking.

Pixel icons: [pixelarticons](https://github.com/halfmage/pixelarticons) by Gerrit Halfmann (MIT License).
