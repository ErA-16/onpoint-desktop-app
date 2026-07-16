# OnPoint

A desktop application built with Python and PySide6 — featuring user authentication, a personal post feed, profile management, and a local SQLite database, all packaged into a single Windows executable.

## The Story

This project started as a challenge from my uncle, David — a way to push myself into real desktop application development, not just tutorials. I began with a simple login screen sketch and, piece by piece, built it into a full multi-page app with signup validation, password hashing, a working database, a collapsible sidebar, a live post feed, and profile editing.

I used AI assistance throughout — especially for concepts I hadn't touched before, like `QStackedWidget` navigation, SQLite integration, and password hashing. It helped me move faster and understand *why* things work, not just copy code. Every feature here, I read, tested, and debugged myself, one small step at a time.

This is one project in an ongoing journey toward becoming a stronger developer. There's another one coming after this.

## Features

- **Authentication** — signup with full validation (name, username format, password strength, terms agreement) and secure login with hashed passwords (SHA-256)
- **Persistent local database** — SQLite, created automatically on first run
- **Collapsible sidebar navigation** — Home, About, Profile, Contact
- **Personal post feed** — write and view posts, saved per user, newest first
- **Profile management** — circular avatar upload, view account details, change password
- **Toast notifications** — non-blocking feedback instead of pop-up dialogs
- **Packaged as a single `.exe`** — no Python installation required to run it

## Tech Stack

- **Python 3.13**
- **PySide6** (Qt for Python) — UI framework
- **SQLite** — local persistent storage
- **PyInstaller** — packaging into a standalone executable

## Getting Started

### Run from source
```bash
pip install PySide6
python main.py
```

### Run the packaged app
Download the latest `main.exe` from the [Releases page](https://github.com/ErA-16/onpoint-desktop-app/releases) and run it directly — no installation needed.

### Default login
A default account is seeded automatically on first run:
- **Username:** `admin`
- **Password:** `Admin123!`

## Project Structure

```
├── main.py                # App entry point, page switching, event wiring
├── login_interface.py     # Login page UI
├── signup_interface.py    # Signup page UI with validation
├── welcome_interface.py   # Main dashboard (sidebar, home, profile, about, contact)
├── database.py            # SQLite setup and all data access functions
├── toast.py               # Custom toast notification widget
├── resource_path.py       # Handles asset paths for both dev and packaged builds
└── images/                # Logo, icons, and default avatar
```

## What I Learned

- Structuring a multi-file PySide6 application with reusable functions
- Nested navigation using `QStackedWidget`
- Working with SQLite: schema design, parameterized queries, and safe password hashing
- Building custom widgets (toast notifications, circular avatars via `QPainter`)
- Packaging a Python GUI app into a distributable `.exe` with PyInstaller, including handling bundled assets

---

Built by Taiwo Oni ([@ErA-16](https://github.com/ErA-16))