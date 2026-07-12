# enigma2-madoe21-feed

[![Built with aiflow](https://img.shields.io/badge/built%20with-aiflow-6b46c1)](https://github.com/cyber93de/aiflow)

This project automatically downloads the latest release version of all Enigma2 plugins from GitHub and serves them as an opkg feed via GitHub Pages.

---

## Plugins in the feed

- enigma2-fakehls-plugin
- enigma2-fritzcall
- enigma2-fritzhome
- enigma2-fritzmon
- enigma2-homematic
- enigma2-lotto
- enigma2-openliga-db
- enigma2-spritpreise-checker
- enigma2-stocks
- enigma2-weather
- enigma2-wireguard

---

## How it works

- For each plugin the latest GitHub Release is downloaded (only tags like `v1.2.3`).
- The IPK files are collected and published as an opkg-compatible feed (`Packages` / `Packages.gz`).
- The feed is deployed to GitHub Pages automatically.

---

## Feed generation

The GitHub Actions workflow downloads all IPKs and runs `opkg-make-index` to generate the feed index.

The feed rebuilds when any plugin repo releases (see below), on its own nightly cron
(`build-feed.yml`, `17 3 * * *`), or on demand via `workflow_dispatch`. This repo's own
IPK (the feed-config package) is included in the feed too, but this repo does **not**
need a version bump to trigger a rebuild — the trigger always comes from the plugin
repos releasing, never the other way around.

### Wiring up a new plugin repo to trigger a feed rebuild

Each plugin repo's `release.yml` has a "Trigger feed rebuild" step that fires a
`repository_dispatch` (`plugin-released`) at this repo once its own release is
published. That call needs a token with write access here, stored as the
**`FEED_DISPATCH_TOKEN`** secret in the *plugin* repo (not this one) — the default
`GITHUB_TOKEN` GitHub gives every workflow is scoped to its own repo only and cannot
call another repo's API, cross-repo dispatch always needs a real token.

1. Generate a token with `repo` scope that can access `madoe21/enigma2-madoe21-feed`:
   - Classic PAT: [github.com/settings/tokens](https://github.com/settings/tokens) → *Generate new token (classic)* → scope `repo`.
   - Fine-grained PAT (tighter, recommended): [github.com/settings/personal-access-tokens](https://github.com/settings/personal-access-tokens) → repository access limited to `enigma2-madoe21-feed` → permission *Contents: Read and write* (needed to dispatch) — narrower than a classic token, since it can't touch any other repo.
2. Add it as a secret in **every plugin repo** that should trigger a rebuild:
   ```bash
   gh secret set FEED_DISPATCH_TOKEN --repo madoe21/<plugin-repo> --body "<token>"
   ```
   Repeat per plugin repo (currently: enigma2-fakehls-plugin, enigma2-fritzcall,
   enigma2-fritzhome, enigma2-fritzmon, enigma2-homematic, enigma2-lotto,
   enigma2-openliga-db, enigma2-spritpreise-checker, enigma2-stocks, enigma2-weather,
   enigma2-wireguard). Nothing needs to be added to *this* repo — it only receives the
   dispatch, it doesn't send one to itself for other plugins.
3. Verify: `gh secret list --repo madoe21/<plugin-repo>` should show `FEED_DISPATCH_TOKEN`.
   The step is a silent no-op (`if: ... && env.FEED_DISPATCH_TOKEN != ''`) when the
   secret is missing, so a stale feed after a plugin release usually means this secret
   isn't set (or the token expired) rather than a workflow failure.

---

## IPK Package

This repo also produces an installable IPK package that configures the madoe21 opkg feed on your Enigma2 receiver. Once installed, all madoe21 plugins become available through the standard package manager.

### Build

```bash
make ipk
```

The resulting `.ipk` is placed in `build/`.

### Quick install (recommended) — straight from the receiver, no build needed

You don't need this repo checked out anywhere for this. SSH into the receiver and run it there;
this downloads the already-published feed IPK and installs it directly, no local build step:

```bash
ssh root@<receiver-ip>

# fetch the current feed-config package straight from the published feed and install it
FEED=https://madoe21.github.io/enigma2-madoe21-feed/feed
IPK=$(wget -qO- "$FEED/Packages" | awk -v p=enigma2-plugin-extensions-madoe21-feed \
  '/^Package: /{pkg=$2} /^Filename: /{if (pkg==p) print $2}')
wget -O /tmp/madoe21-feed.ipk "$FEED/$IPK"
opkg install /tmp/madoe21-feed.ipk

# now the feed source is configured (/etc/opkg/madoe21-feed.conf) - pull the package lists
opkg update

# install whichever plugin(s) you want from the feed
opkg install enigma2-plugin-extensions-fritz-call
```

If `opkg install` ever complains about a missing source before you've run the steps above, you
can also just write the feed source by hand first: `echo 'src/gz madoe21 https://madoe21.github.io/enigma2-madoe21-feed/feed' > /etc/opkg/madoe21-feed.conf && opkg update`.

Once installed, `enigma2-plugin-extensions-madoe21-feed` upgrades itself the same way as any other
feed package (`opkg upgrade enigma2-plugin-extensions-madoe21-feed` or via the OpenATV plugin
manager), so re-running any of this by hand afterwards is normally not necessary.

### Build it yourself instead

1. Copy `.env.example` to `.env` and set your receiver's IP address:
   ```
   BOX_HOST=192.168.1.xxx
   BOX_USER=root
   BOX_PORT=22
   ```

2. Install the feed package and refresh the package list:
   ```bash
   make install
   ```

   This copies the IPK to the receiver, installs it, and runs `opkg update`.

### What it does

- Installs `/etc/opkg/madoe21-feed.conf` pointing to the GitHub Pages feed URL
- On uninstall, the feed config is cleanly removed
- Reinstalling (e.g. `opkg install --force-reinstall`) preserves the config

---

## Requirements

- Python 3
- `requests`

**Note:** The release workflows in the plugin repos build and publish IPK files automatically when a tag is pushed to main.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Found a bug or have a suggestion for improvement? Please create an issue or pull request.

I appreciate everyone who supports me and the project! For any requests and suggestions, feel free to provide feedback.

<p>
  <a href="https://www.buymeacoffee.com/madoe21">
    <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" height="50" alt="Buy Me a Coffee">
  </a>

  <a href="https://ko-fi.com/madoe21">
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" height="50" alt="Ko-fi">
  </a>

  <a href="https://paypal.me/MartinD809">
    <img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_111x69.jpg" height="50" alt="PayPal">
  </a>
</p>

---

## Built with aiflow

This project was built with support from **[aiflow](https://cyber93de.github.io/aiflow/)** — *built with aiflow*.
