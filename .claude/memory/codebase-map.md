# Codebase map (onboarding 2026-07-08)

**enigma2-madoe21-feed** — publishes all madoe21 Enigma2 plugins as an
**opkg feed** on GitHub Pages, and ships a small ipk that registers that feed
on a receiver so the plugins appear in the package manager.

## Pieces
- `src/madoe21-feed.conf` — the opkg source line installed to
  `/etc/opkg/madoe21-feed.conf`. **Must** point at the `/feed` subdirectory:
  `src/gz madoe21 https://madoe21.github.io/enigma2-madoe21-feed/feed`.
- `Makefile` — builds the ipk; copies `src/madoe21-feed.conf` into
  `data/etc/opkg/`. `control/{control,postinst,prerm}` — ipk metadata; postinst
  just tells the user to run `opkg update`.
- `generate_feed.py` — local helper: downloads each plugin's latest release ipk
  (GitHub API) into `ipks/`. The CI does the same with `gh release download`.
- `.github/workflows/build-feed.yml` — the real feed build: downloads every
  plugin's latest `*.ipk` into `public/feed/`, runs `opkg-make-index . >
  Packages` (+ gzip), writes an index/landing page, deploys `public/` to Pages.
  Triggered by `repository_dispatch: plugin-released`, a daily cron, or manual.

## The plugin list (keep in sync in 3 places)
`generate_feed.py` PLUGINS, the workflow's `PLUGINS=(…)`, and README. Current:
fakehls-plugin, fritzcall, fritzhome, fritzmon, homematic, lotto, openliga-db,
spritpreise-checker, stocks, weather, wireguard.

## Discovery gotchas (the bug that hid the plugins)
- The installed `.conf` URL and the **published path must match**. Pages serves
  the feed under `/feed`; a `.conf` without `/feed` → `opkg update` 404s on
  `Packages.gz` → empty feed → plugins "not findable". (Fixed.)
- `opkg-make-index`'s `-p` is a filename **PREFIX**, not an output file — it
  corrupts `Filename:` paths. Use `opkg-make-index . > Packages`. (Fixed.)
- After a fix, the feed only updates once the workflow re-runs and Pages
  redeploys; on the box run `opkg update` then
  `opkg list | grep enigma2-plugin-extensions-`.

## Note
This repo has no application code to optimize — it is packaging + CI. Value is
in the correctness of the feed URL/index and the plugin-list sync.
