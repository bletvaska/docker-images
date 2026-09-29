# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (`YYYY.M.PATCH`).

## [Unreleased]

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
