<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:111827,100:0f766e&height=160&section=header&text=Folder%20Footprint&fontSize=38&fontColor=ffffff" width="100%" alt="Folder Footprint banner" />
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=2800&pause=700&color=0F766E&center=true&vCenter=true&width=820&lines=Understand+where+your+disk+space+goes" alt="Animated project title" />
<p>Generate a read-only HTML report showing folder sizes, top-level breakdowns, and the largest files.</p>
<p><img src="https://img.shields.io/github/license/CyberLoop-dev/folder-footprint?style=for-the-badge" alt="MIT license" /> <img src="https://img.shields.io/github/languages/top/CyberLoop-dev/folder-footprint?style=for-the-badge" alt="Top language" /> <img src="https://img.shields.io/github/stars/CyberLoop-dev/folder-footprint?style=for-the-badge" alt="Stars" /> <img src="https://img.shields.io/github/last-commit/CyberLoop-dev/folder-footprint?style=for-the-badge" alt="Last commit" /></p>
<img src="assets/illustration.svg" width="92%" alt="Folder size report illustration" /></div>

## 🎯 Overview

Folder Footprint scans a directory and creates a portable HTML report with total size, top-level folder sizes, and the largest files. It is read-only: it skips symlinks and common generated folders, and never deletes or changes source files.

## ✨ Features

- 📁 Summarizes sizes of top-level folders and files.
- 📦 Lists the largest files in the scanned tree.
- 📊 Generates a clean, responsive HTML report with relative-size bars.
- 🛡️ Skips symlinks and common generated directories.
- 🔒 Performs no cleanup or destructive actions.

## 🎬 Demo

<pre><code>python main.py ~/Downloads --output downloads-report.html</code></pre>

Open the generated HTML file in your browser.

## 🚀 Quick Start

<pre><code>python main.py ./your-folder --output folder-footprint.html</code></pre>

## 🧰 Tech Stack

- Python 3.10+ standard library
- pathlib, os.scandir, and HTML escaping

## 🗂️ Folder Structure

<pre><code>folder-footprint/
├── main.py
├── requirements.txt
└── assets/
    └── illustration.svg</code></pre>

## 🧭 Roadmap

- [ ] Add an optional JSON report format.
- [ ] Add configurable directory exclusions.
- [ ] Add a treemap visualization for nested folders.

## 🤝 Contributing

Issues and pull requests are welcome. Include your operating system, a small directory example, and the command used when reporting a bug.

## 📄 License

Released under the MIT License. See [LICENSE](LICENSE).

<div align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f766e,100:111827&height=110&section=footer" width="100%" alt="Animated wave footer" /></div>
