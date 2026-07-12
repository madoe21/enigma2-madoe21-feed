# example-plugin — template, not a real plugin

This folder is **not built, not packaged, and not part of the feed.** It exists so anyone
cloning `enigma2-madoe21-feed` and wanting to build their own Enigma2 plugin that plugs
into a feed like this one has a working starting point instead of reverse-engineering the
structure from the 11 real plugin repos.

Everything here is inert by construction: the workflow files live under
`example-plugin/.github/workflows/`, not the repo root `.github/workflows/`, so GitHub
Actions never picks them up. Nothing runs, nothing builds, nothing gets published from
this folder on its own.

## How to actually use this

1. Copy the whole `example-plugin/` folder out into a **new, separate repo** (this is a
   template for *a plugin repo*, structurally the same shape as
   `enigma2-fritzcall`/`enigma2-lotto`/etc. — it is not meant to live inside a feed repo).
2. Move `.github/workflows/*.yml` to that new repo's root `.github/workflows/` so Actions
   picks them up.
3. Rename things:
   - `PLUGIN_NAME` / `PACKAGE_NAME` in `Makefile`
   - `Package:` / `Description:` / `Maintainer:` in `control/control`
   - `src/example_plugin/` directory name (must match `PLUGIN_NAME`)
   - the `YOUR-GITHUB-USERNAME/YOUR-FEED-REPO` placeholder in
     `.github/workflows/release.yml`'s "Trigger feed rebuild" step
4. Replace `src/example_plugin/plugin.py` with your actual plugin logic. The
   `PluginDescriptor`/`Screen`/config-in-`/etc/enigma2/settings` shape is the one every
   plugin in this feed uses; the services/business logic is entirely up to you.
5. Set `VERSION` to `0.1.0` (or wherever you're starting), push to `main`. `release.yml`
   builds the IPK, tags `v<VERSION>`, publishes a GitHub Release with the IPK attached,
   and (once you've set `FEED_DISPATCH_TOKEN` — see the feed repo's own README section
   "Wiring up a new plugin repo to trigger a feed rebuild") tells your feed to pull it in.
6. Add your new plugin's repo name to the `PLUGINS` array in the feed repo's
   `.github/workflows/build-feed.yml` so it actually gets included.

## What's deliberately left out

- No icons (`plugin.png` etc.) — Enigma2 falls back to a default icon without one; add
  your own 56x38 PNG and uncomment the `icon=` line in `plugin.py` when you have one.
- No locale/`.po`/`.mo` files — see any real plugin here (e.g. `enigma2-fritzcall`) for
  the `compile-locales` Makefile pattern if you want translations.
- No settings-persistence-from-file boilerplate — Enigma2's `config.plugins.*` already
  persists to `/etc/enigma2/settings` on its own; only add manual file parsing if you
  need to read values *before* the config system is up (autostart timing edge case a
  couple of the real plugins here hit).
- No CI beyond a build-check — copy `ci.yml`/`guard-*.yml`/`bump-develop.yml` from any
  of the real plugin repos if you want the same branch-protection/version-bump
  automation this feed's plugins use.
