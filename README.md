# Robotics Store

> A Flask web storefront and admin panel for browsing and managing robotics components, with category filtering, search, and Firebase-hosted product images.

**Frontend UI Preview:** https://gasparyanvazgen.github.io/robotics-store *(static UI showcase only — Flask backend, database filtering, and `/admin` panel are not active on this link)*

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)

---

## Overview

Robotics Store ("RoboShop") is a small product catalog site for selling robotics parts and devices. Visitors can browse products, filter them by category and availability, and search by name or description. The public interface is in Armenian.

The storefront is a catalog only: there is no cart or checkout. The landing page tells visitors that purchases are made by phone or message. Store owners sign in to a password-protected admin panel to manage categories, products (including image uploads), and admin users. Product data is stored in PostgreSQL and product images are stored in Firebase Cloud Storage.

---

## Key Features

**Storefront**
- Product listing with pagination
- Filter by category (radio-button selector)
- "Only in stock" filter (products with amount greater than zero)
- Keyword search across product name and description, with name matches ranked above description matches
- Fallback image for products without a photo
- Responsive landing page with animated sections (AOS) and a custom category dropdown

**Admin panel** (built with Flask-Admin, available at `/admin`)
- Login-protected access (Flask-Login) with a "keep me logged in" option
- CRUD management for categories, products, and users
- Product search by name, detail view, and data export
- Image upload for `jpg`, `jpeg`, and `png` files, resized to fit within 1000×1000 and given a random filename
- Uploaded images are pushed to Firebase Storage, made public, and the temporary local copy is deleted; images are also removed from Firebase when a product is deleted
- Server-side validation: price and amount must be non-negative integers
- Passwords stored as hashes
- An initial admin account is created on the first request from environment variables

---

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python 3 |
| Web framework | Flask `2.2.2` |
| Admin UI | Flask-Admin `1.6.0` (Bootstrap 4 template mode) |
| Authentication | Flask-Login `0.6.2` |
| Forms | Flask-WTF `1.0.1`, WTForms `3.0.1` |
| ORM / Database | Flask-SQLAlchemy `2.5.1`, SQLAlchemy `1.4.46`, PostgreSQL (`psycopg2-binary` `2.9.9`) |
| File storage | Firebase Admin SDK `6.2.0` (Cloud Storage) |
| Image handling | Pillow `9.2.0` |
| Production server | Gunicorn `20.1.0` |
| Frontend | Jinja2 templates, HTML, CSS, vanilla JavaScript, Font Awesome `6.2.1` (CDN), AOS (CDN) |

All pinned dependencies are listed in `requirements.txt`.

---

## Project Structure

```text
robotics-store/
├── app/
│   ├── __init__.py          # Application factory: config, extensions, blueprints, Firebase init
│   ├── models.py            # SQLAlchemy models: Category, Product, User
│   ├── admin/
│   │   ├── __init__.py      # Flask-Admin setup and registered views
│   │   └── views.py         # Admin views, image upload/delete logic (Firebase Storage)
│   ├── main/
│   │   ├── __init__.py      # Routes: "/" (storefront), "/login", login manager
│   │   ├── filter.py        # Category / availability / search filtering and pagination
│   │   └── forms.py         # Login form
│   ├── templates/
│   │   ├── base.html        # Base layout (header, footer, contact links)
│   │   ├── index.html       # Landing page and product catalog
│   │   └── login.html       # Admin login page
│   └── static/
│       ├── css/             # style.css, login.css
│       ├── js/index.js      # Category dropdown and intro button behavior
│       └── img/             # Logo, backgrounds, default product image
├── config.py                # App configuration (database, Firebase, admin credentials)
├── run.py                   # Entry point; creates the initial admin user
├── requirements.txt         # Python dependencies
└── .gitignore
```

---

## Getting Started

### Prerequisites

- **Python:** `3.9` or `3.10` (recommended for compatibility with Flask `2.2.2` and SQLAlchemy `1.4.46`)
- **pip** and **venv**
- **Rust toolchain (`rustup`):** Required if any Python dependencies (such as `cryptography`) need to be compiled from source on your platform.
  - **Unix / Linux / macOS:**
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://rustup.rs | sh
    # source "$HOME/.cargo/env"
    ```
  - **Windows:** Download and run `rustup-init.exe` from [rustup.rs](https://rustup.rs). (Visual Studio C++ build tools may also be required.)
- **PostgreSQL** database you can connect to
- A **Firebase project** with Cloud Storage enabled, and a service account key (JSON file)
- **Git**

### Installation

```bash
# 1. Clone the repository
git clone [INSERT_REPOSITORY_URL]
cd robotics-store

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Configuration is split between environment variables and constants in `config.py`.

**1. Environment variables (required)**

The app reads the admin credentials from the environment at startup and will not start without them.

| Variable | Description |
| --- | --- |
| `USER` | Username of the initial admin account |
| `PASSWORD` | Password of the initial admin account |

```bash
# Linux / macOS
export USER=[INSERT_ADMIN_USERNAME]
export PASSWORD=[INSERT_ADMIN_PASSWORD]

# Windows (Command Prompt)
set USER=[INSERT_ADMIN_USERNAME]
set PASSWORD=[INSERT_ADMIN_PASSWORD]
```

> `USER` is often already set by the operating system to your login name. Set it explicitly to the admin username you want.

**2. Database connection (`config.py`)**

Replace the placeholder `SQLALCHEMY_DATABASE_URI` in the `Config` class with your own PostgreSQL connection string:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://[DB_USER]:[DB_PASSWORD]@[DB_HOST]/[DB_NAME]'
```

Tables are created automatically on startup (`db.create_all()`).

**3. Firebase Storage (`config.py`)**

| Setting | Description |
| --- | --- |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to your Firebase service account key JSON. The default is `serviceAccountKey.json` in the project root. |
| `STORAGE_BUCKET` | Your storage bucket name. Replace the placeholder with `[INSERT_FIREBASE_STORAGE_BUCKET]`. |

To get a key, open the Firebase console, go to Project settings, then Service accounts, and select "Generate new private key". Save the file as `serviceAccountKey.json` in the project root.

**4. Optional settings (`config.py`)**

| Setting | Description |
| --- | --- |
| `PRODUCTS_PER_PAGE` | Number of products shown per page. It is currently `1`, so increase it for a real catalog. |
| `IMAGE_UPLOADS` | Local temporary directory for uploads before they are sent to Firebase. |

**5. Site contact details**

The header and footer in `app/templates/base.html` contain placeholder social links, an email address, and a phone number. Replace them with your own.

**Security notes**

- Never commit `serviceAccountKey.json` or real database credentials. The default `.gitignore` does not exclude `serviceAccountKey.json`, so add it before your first commit:
  ```bash
  echo "serviceAccountKey.json" >> .gitignore
  ```
- `SECRET_KEY` is generated randomly each time the app starts. Sessions are invalidated on restart, and multiple Gunicorn workers will not share sessions. For production, load a fixed secret from an environment variable instead.

---

## Usage

### Run in development

```bash
# Linux / macOS
export FLASK_APP=run.py
export FLASK_DEBUG=1      # optional: debug mode
flask run

# Windows (Command Prompt)
set FLASK_APP=run.py
set FLASK_DEBUG=1
flask run
```

Or run the entry point directly:

```bash
python3 run.py
```

The app is available at http://127.0.0.1:5000.

### Run in production

```bash
gunicorn run:app
```

### Routes

| Route | Description |
| --- | --- |
| `/` | Storefront. Query parameters: `search`, `category_id`, `availability=on`, `page` |
| `/login` | Admin login |
| `/admin` | Admin dashboard (requires login) |
| `/admin/category/` | Manage categories |
| `/admin/product/` | Manage products and images |
| `/admin/user/` | Manage admin users |
| `/admin/logout/` | Log out and return to the storefront |

Example storefront queries:

```text
/?search=arduino
/?category_id=2&availability=on
/?search=sensor&category_id=3&page=2
```

### Managing the catalog

1. Start the app with the `USER` and `PASSWORD` environment variables set. The admin account is created on the first request.
2. Open `/login` and sign in.
3. Create at least one **Category**, then add **Products** (name, price, amount, description, category, image).
4. Products appear on the storefront immediately. A product with an amount of `0` is hidden when visitors enable the "only available" filter.

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository.
2. Clone your fork and create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. Set up the project locally by following [Getting Started](#getting-started).
4. Make your changes and test them manually (the repository has no automated test suite yet).
5. Commit your changes using the commit message convention below.
6. Push your branch:
   ```bash
   git push origin feat/your-feature-name
   ```
7. Open a Pull Request describing what you changed and why.

### Commit message convention

All commit messages **must** follow the `type: message` format, with **no space after the colon**.

```text
feat: add product sorting
fix: resolve image upload error
docs: update readme
```

Common commit types:

| Type | Use for |
| --- | --- |
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting changes that do not affect code behavior |
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `build` | Build system or dependency changes |
| `ci` | CI configuration changes |
| `chore` | Maintenance tasks and other changes |
| `revert` | Reverting a previous commit |
