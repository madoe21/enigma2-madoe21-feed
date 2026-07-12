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

---

## IPK Package

This repo also produces an installable IPK package that configures the madoe21 opkg feed on your Enigma2 receiver. Once installed, all madoe21 plugins become available through the standard package manager.

### Build

```bash
make ipk
```

The resulting `.ipk` is placed in `build/`.

### Install on receiver

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
