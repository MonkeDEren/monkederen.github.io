# 🔡 Permutation App

A fast, intuitive tool to generate **N-letter permutations with fixed positions**, built using **Python + Kivy** and also available as a **GitHub Pages web app**.

---

## 🚀 Features

### 🧠 Core Functionality
- Generate permutations of a word
- Choose desired word length
- Fix letters at specific positions
- Remove duplicate arrangements
- Filter results to genuine English words
- APK works fully offline

### 🌐 Web Version
- 🌗 Dark/Light theme toggle
- 📄 Download results as TXT
- 📱 Mobile-friendly responsive UI
- ✨ Smooth animations
- 📘 Tutorial section
- Uses the same bundled `words.txt` dictionary as the APK

---

## 📱 Android APK

The latest successful APK is published as a GitHub Release:

👉 **[Download latest APK](https://github.com/MonkeDEren/monkederen.github.io/releases/latest/download/PermutationApp-1.0-release.apk)**

Compatible with Android 5.0+.

The APK does not require the Android `INTERNET` permission and does not download a dictionary when starting.

---

## 📚 Offline Dictionary

`words.txt` is part of the application source and is included in the Android build by `buildozer.spec`.

The repository contains a manual GitHub Actions workflow named **Generate Offline Dictionary**. It generates `words.txt` from the `english-words` package when manually requested.

The web app loads the same `words.txt` from GitHub Pages, so the web and APK versions use the same dictionary data.

---

## 🌐 Web App

Use the app directly in your browser:

👉 **https://monkederen.github.io**

No installation needed.

---

## 🖥️ Desktop Version (Python + Kivy)

### Requirements
- Python 3.10-3.11
- Kivy

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Android Build

The GitHub Actions build uses a pinned Buildozer release instead of `master`.

On pushes to `main`, the workflow builds the APK, stores it as an Actions artifact, and publishes it as a GitHub Release asset.

The release asset is always named:

`PermutationApp-1.0-release.apk`

---

## ⚠️ Branding Assets

`buildozer.spec` expects these files in the repository root:

- `presplash.png`
- `icon.png`

They must be added before a production APK build if they are not already present.

---

## 📄 License

Add a `LICENSE` file if you plan to distribute or accept forks of the project.
