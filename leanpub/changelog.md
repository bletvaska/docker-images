# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (`YYYY.M.PATCH`).

## [Unreleased]

## [2026.10.1] - 2026-10-04

### Added

- `jekyll-theme-nucky/_includes/mermaid.html`
  - diagrams written as ```` ```mermaid ```` code blocks are rendered with
    [Mermaid](https://mermaid.js.org) 11.15.0; the theme of the diagrams
    follows the light / dark mode and they are redrawn when it is switched;
    `default.html` includes it only on pages containing a diagram
- `jekyll-theme-nucky/_includes/lightbox.html`
  - classes `.wide-100` and `.wide-75` (`![popis](obrazok.svg){.wide-100}`)
    show an image in `<figure>` over the full width of the text, resp. at 75 %
    of it, without the limit of half of the window width and 60 % of its height

### Changed

- `app/pandoc/crossref.yaml`
  - a figure made from a div (`::: {#fig:nazov}` ... `:::`), e.g. around
    a Mermaid diagram, gets the caption `Obr. N: Popisok` like an image,
    without the period pandoc-crossref adds by default
- `jekyll-theme-nucky/assets/css/nucky.css`
  - Mermaid diagrams in a numbered figure are centered like images
  - headings of the alert blocks (`[lecturer]`, `[comment]`, `[warning]` ...)
    are semibold
- `jekyll-theme-nucky/_includes/lightbox.html`
  - SVG images can always be zoomed (vector images stay sharp, and an SVG
    without `width` and `height` has no real natural size) and in the preview
    they are stretched to the size of the window instead of their natural size

### Fixed

- `jekyll-theme-nucky/assets/css/print.css`
  - labels of pins (`.pin`, white text on a coloured background) disappeared
    when printing outside of alert blocks, because browsers drop background
    colours; they keep their colours now (`print-color-adjust: exact`)
- `app/pandoc/defaults/citations.yaml`
  - citations (`@kluc`) and references to figures (`@fig:...`) in alert blocks
    (`[comment]`, `[warning]` ...) were not processed, because `alerts.lua`
    turned the content of a block into HTML before `pandoc-crossref` and
    `citeproc` ran; `alerts.lua` runs after them now

## [2026.9.10] - 2026-09-30

### Added

- `jekyll-theme-nucky/_includes/math.html`
  - math in LaTeX syntax (`$...$`, `$$...$$`) is rendered with
    [KaTeX](https://katex.org) 0.18.9; `default.html` includes it only on pages
    containing math

- `justfile` for building and releasing the image: `just build` (image `dev`),
  `just release VERSION` (tags `VERSION`, `YYYY.M`, `YYYY` and `latest`,
  refuses a version missing in the changelog or already on Docker Hub) and
  `just push VERSION` (pushes the four tags if they point to the same image)

### Changed

- identifiers of headings are generated without diacritics (Pandoc extension
  `ascii_identifiers` in `_config_defaults.yml`), e.g. `## Hysterézia` gets
  `id="hysterezia"` instead of `id="hysterézia"`; links to headings with
  diacritics in the anchor (`#hysterézia`) have to be rewritten

- files copied into `/app` in the image are moved to the `app/` folder of the
  repository (`justfile`, `entrypoint.sh`, `tasks.py`, `liquid_render.rb`,
  `_config_defaults.yml`, `pandoc/`, `texmf/`), which is copied as a whole
  with `COPY app/ /app/`; the content of the image is unchanged

### Deprecated

- `jekyll-theme-nucky/_includes/mathjax.html` (MathJax 2.7.3, which a page had
  to include by itself with `{% include mathjax.html %}`) does nothing now and
  can be removed from the pages

### Fixed

- math on pages without `{% include mathjax.html %}` was shown as raw LaTeX
  (e.g. `\[ e = w - y \]`)

- the table of contents lost or froze its highlighting of the current section
  after the URL got a `#heading` (a click in the table of contents); `nucky.css`
  set `html { height: 100% }`, so tocbot considered the page always scrolled to
  the bottom and highlighted the heading from the URL, which it does not find
  for headings with diacritics (`#hyster%C3%A9zia`)

## [2026.9.9] - 2026-09-30

### Added

- `jekyll-theme-nucky/_includes/toc.html`
  - table of contents of the page ([tocbot](https://tscanlin.github.io/tocbot/) 4.36.8)
    in a panel left of the text, which stays in place while scrolling on wide
    screens (from 1200 px) and slides in with the "Obsah" button on narrower
    ones; the section being read is highlighted, steps (`.step`) are numbered
    like in the text; hidden when printing, on pages with less than 2 headings
    and on pages with `toc: false` in the front matter
- `jekyll-theme-nucky/_layouts/labs.html`, `jekyll-theme-nucky/_layouts/lecture.html`
  - table of contents with `h2` and `h3` headings without tasks (`.task`) in labs
    and with `h2` to `h4` headings in lectures

### Changed

- `jekyll-theme-nucky/_layouts/lecture.html`
  - videos of a lecture are listed in `videos` (like in a lab) instead of
    a single `video`, which is not supported anymore, and they are laid out
    in two columns like the videos of a lab, instead of one video over
    the full width
  - heading is "Video k prednáške" for one video and "Videá k prednáške"
    for more, instead of "Záznam z prednášky"

## [2026.9.8] - 2026-09-30

### Added

- `jekyll-theme-nucky/_includes/seo.html` (taken from the IoT course)
  - `<title>` in the form `Page · Course`, meta description, canonical URL,
    Open Graph and Twitter Card tags and favicon (`assets/img/favicon.png`);
    configured with `title`, `description`, `url`, `og_image` and
    `paths.assets` (defaults to `baseurl` + `/assets`) in `_config.yml`
    and `title`, `description`, `subtitle`, `image` in the page front matter
- `jekyll-theme-nucky/assets/js/nucky.js` (taken from the IoT course)
  - light/dark color mode set before the page is rendered (stored choice or
    system setting), switching of the highlight.js theme and the mode switcher
    in the navigation (`[data-bs-theme-value]`, `#theme-icon`)
  - syntax highlighting with `hljs.highlightAll()` and Bootstrap classes
    `table table-striped` for tables
- `jekyll-theme-nucky/assets/css/nucky.css`
  - dark mode colors for the jumbotron, footer, `theme-alert-*` boxes and
    license icons
  - images in the content are at most as wide as the text (`main img`)
- `jekyll-theme-nucky/_includes/lightbox.html`
  - images in `<figure>` and their captions are centered, images are scaled down
    to at most half of the window width (the width of the text on narrow screens)
    and 60 % of the window height; a scaled down image opens in its original size
    with its caption after a click ([GLightbox](https://github.com/biati-digital/glightbox) 3.3.1),
    the preview is closed with ESC, by clicking the image, outside of it or on X
  - images have a white background (with a small padding in dark mode and in
    the preview), so images with a transparent background stay readable
- `jekyll-theme-nucky/_includes/navigation.html`
  - fallback navigation with the course title and the color mode switcher;
    a course replaces it with its own `_includes/navigation.html`

### Changed

- `jekyll-theme-nucky/assets/css/print.css`
  - images in `<figure>` are printed at most 75 % of the text width
- `jekyll-theme-nucky/assets/css/nucky.css`
  - sticky footer with a flex layout (`body` is a column at least as tall as
    the window, `main` fills the free space) instead of the footer with
    a fixed height of 250 px, which overlapped the content with a longer
    course description
  - base font size is `1.4rem` instead of `1.3em`
  - list indentation applies only to the content (`main ol`, `main ul`),
    not to the navigation
  - paragraph in `.footer-copyright` has no margins instead of `auto !important`
- `jekyll-theme-nucky/_layouts/default.html` (taken from the IoT course)
  - meta tags from `seo.html`, light/dark color mode with `nucky.js`,
    configurable highlight.js 11.11.1 with a light and a dark theme
    (`highlightjs.version`, `highlightjs.theme_light`, `highlightjs.theme_dark`),
    Font Awesome 5.15.4 from cdnjs, zooming of images with `lightbox.html`
  - navigation from `_includes/navigation.html` instead of the missing `nav.html`
  - content is placed directly in `<main>` instead of `<div class="container">`,
    so the jumbotron of the layouts spans the full width and containers are
    not nested
  - paths to the assets from `paths.assets` (defaults to `baseurl` + `/assets`)
  - additional stylesheets of the course listed in `extra_css` in `_config.yml`
    (paths relative to `assets/css/`) are loaded after `nucky.css`
  - course description in the footer is not wrapped in another `<p>`
  - removed scrollspy for the old `#sidenav` and the inline script adding
    `img-fluid` to all images (done by CSS now)

## [2026.9.7] - 2026-09-30

### Added

- `pandoc/defaults/citations.yaml`, `pandoc/crossref.yaml`
  - numbering of figures with `pandoc-crossref` for Jekyll pages: figures
    with a label (`![Popisok](obrazok.png){#fig:nazov}`) get the caption
    `Obr. N: Popisok` and can be referred to from the text with `@fig:nazov`,
    which is rendered as just the number linking to the figure
    (`na obrázku @fig:nazov` -> `na obrázku N`); figures without a label
    are not numbered

### Changed

- `jekyll-theme-nucky/assets/css/print.css`
  - left page margin is increased from 15 mm to 20 mm

## [2026.9.6] - 2026-09-29

### Changed

- `jekyll-theme-nucky/_layouts/outline.html`
  - lectures and labs are taken from the collections `site.lectures` and `site.labs`
    instead of filtering `site.pages` by `layout` and `year`
  - year in the title is taken from `site.year` instead of `page.year`
- `jekyll-theme-nucky/_layouts/default.html`
  - copyright years in the footer are taken from `site.since` (the year of
    the first run of the course, defaults to `site.year`) and `site.year`
    instead of the years of all pages with layout `outline`

## [2026.9.5] - 2026-09-29

### Changed

- `jekyll-theme-nucky/_layouts/lecture.html`
  - lecture recording is embedded with Bootstrap 5 classes (`ratio ratio-16x9`)
  - the recording section (including its heading) is hidden when printing (`d-print-none`)
- `jekyll-theme-nucky/_includes/video.html`
  - video is embedded with Bootstrap 5 classes (`ratio ratio-16x9`)
  - the video (including its heading) is hidden when printing (`d-print-none`)

### Fixed

- `jekyll-theme-nucky/_layouts/lecture.html`, `jekyll-theme-nucky/_includes/video.html`
  - videos were rendered with Bootstrap 4 classes (`embed-responsive*`),
    which do not exist in Bootstrap 5, so the embedded players had
    the default iframe size of 300×150 px
- `jekyll-theme-nucky/_includes/video.html`
  - heading was never shown because of the typo `include.titlet`

## [2026.9.4] - 2026-09-29

### Added

- `jekyll-theme-nucky/_layouts/labs.html`
  - title is prefixed with `Lab #N:` when the page defines `week`
  - "Todo" box with items from `page.todo`, shown only in the lecturer build (`site.lecturer`)
- `jekyll-theme-nucky/assets/css/nucky.css`
  - styles for step headings (`### Title {.step}`): underline and a CSS counter
    rendering `Krok N` above the title, colors taken from Bootstrap variables
    (`--bs-link-color`, `--bs-emphasis-color`), so they work in dark mode too
- `Dockerfile`
  - build argument `VERSION` (default `dev`), exposed as `LEANPUB_VERSION`
    environment variable and `version` label
- `justfile`
  - recipe `versions` prints the version of the image
- `entrypoint.sh`
  - recipes working with the site (`build`, `clean`, `serve`, `deploy`, `epub`, `pdf`)
    stop with a readable error when there is no `_config.yml` in the current folder

### Changed

- `jekyll-theme-nucky/_layouts/labs.html`
  - heading above videos is "Video pre cvičenie" for one video and
    "Videá pre cvičenie" for more
  - videos are laid out with Bootstrap 5 classes (`row`, `col-6`, `ratio ratio-16x9`)
  - the whole video section (including its heading) is hidden when printing (`d-print-none`)
- `jekyll-theme-nucky/assets/js/labs.js`
  - step numbers are no longer inserted as `Krok #N:` text, the numbering
    is done by CSS in `nucky.css`

### Removed

- `Dockerfile`
  - fixed `LABEL version="2026.09"`, replaced by the `VERSION` build argument

### Fixed

- `jekyll-theme-nucky/_layouts/labs.html`
  - videos were rendered with Bootstrap 4 classes (`embed-responsive*`),
    which do not exist in Bootstrap 5, so the embedded players had
    the default iframe size of 300×150 px
  - invalid Liquid syntax `{% for video in page.videos: %}`
