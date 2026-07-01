# Hefesto

> *Forge your world. Automate everything.*

![Flask](https://img.shields.io/badge/Flask-000000.svg?style=flat-square&logo=Flask&logoColor=white)  ![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white)  ![bat](https://img.shields.io/badge/bat-31369E.svg?style=flat-square&logo=bat&logoColor=white)

## Overview

Hefesto is a Python automation framework for complex system administration. It bootstraps required dependencies on first launch, provides a one-click Windows installer, and exposes a unified interface for orchestrating multi-step deployment and configuration workflows.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

---

## Features

|      | Component         | Details                                                                                                                                                                                                                                          |
| :--- | :---------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ⚙️  | **Architecture**  | <ul><li>Python-based monolithic utility tool</li><li>Flask web server via `waitress` as WSGI production server</li><li>Async I/O support through `asyncio_dgram` for UDP stream handling</li><li>Script-driven entry points (`run.bat`, `install.bat`)</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>Structured around `.py` modules with `.bat` automation scripts</li><li>Dependency versions pinned via `requirements.txt`</li><li>No evidence of linting or formatting tooling (e.g., `flake8`, `black`)</li></ul>                        |
| 📄 | **Documentation** | <ul><li>No dedicated docs directory or wiki detected</li><li>No `README.md` or inline docstring evidence found</li><li>`license` file present — project has defined legal terms</li></ul>                                                        |
| 🔌 | **Integrations**  | <ul><li>**Shodan API** — network intelligence & device scanning via `shodan`</li><li>**Discord Rich Presence** via `pypresence`</li><li>HTTP client integrations: `requests` (sync) + `httpx` (async)</li><li>DNS resolution via `dnspython`</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Separated concerns: web layer (`flask`/`waitress`), networking (`dnspython`, `httpx`), async I/O (`asyncio_dgram`)</li><li>`.bat` scripts decouple install and runtime steps</li><li>`install_modules.bat` isolates dependency bootstrapping</li></ul> |
| ⚡️  | **Performance**   | <ul><li>Async UDP streams via `asyncio_dgram` for non-blocking I/O</li><li>Async HTTP via `httpx` reduces blocking on network calls</li><li>`waitress` replaces Flask dev server for improved throughput</li></ul>                               |

---

## Project Structure

```
└── Hefesto/
    ├── hefesto.py
    ├── icon.ico
    ├── install.bat
    ├── install_modules.bat
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    └── run.bat
```

---

## Getting Started

### Prerequisites

- Python 3.10+ / Node.js 18+ *(depending on the stack above)*

### Installation

```sh
git clone "https://github.com/IlluzyonistCode/Hefesto
cd Hefesto"
pip install -r requirements.txt
```

### Usage

```sh
install.bat
```

---

## Contributing

- [Report Issues](https://github.com/IlluzyonistCode/Hefesto/issues)
- [Submit Pull Requests](https://github.com/IlluzyonistCode/Hefesto/pulls)
- [Discussions](https://github.com/IlluzyonistCode/Hefesto/discussions)

---

## License

Distributed under the [AGPL-3.0](LICENSE) license.
