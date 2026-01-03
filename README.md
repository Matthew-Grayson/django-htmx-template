# django-htmx-template

A Django project template with [django-htmx](https://github.com/adamchainz/django-htmx) integration, following the layout conventions from the [django-htmx/example](https://github.com/adamchainz/django-htmx/tree/main/example) project.

## Features

✅ Django 5.2.9 with Python 3.11
✅ django-htmx integration with middleware
✅ HTMX loaded via template tags
✅ CSRF protection configured for HTMX requests
✅ App-based template organization
✅ Development tools: black, djhtml, pre-commit, django-extensions

## Project Structure

```
django-htmx-template/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                # Main application
│   ├── templates/
│   │   └── core/
│   │       ├── _base.html
│   │       ├── index.html
│   │       └── partials/
│   │           └── ping.html
│   ├── views.py
│   ├── urls.py
│   └── ...
├── manage.py
├── pyproject.toml       # uv project metadata & dependencies
└── uv.lock              # uv dependency lock file
```

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Matthew-Grayson/django-htmx-template.git
cd django-htmx-template
```

2. Install dependencies (uv will automatically create a virtual environment):
```bash
uv sync
```

3. Run migrations:
```bash
uv run python manage.py migrate
```

4. Start the development server:
```bash
uv run python manage.py runserver
```

5. Visit http://127.0.0.1:8000/ in your browser

### Alternative: Manual Virtual Environment

If you prefer to activate the virtual environment manually:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python manage.py runserver
```

## Usage

The home page demonstrates a simple HTMX interaction:
- Click "Send HTMX Request" to fetch content without a page refresh
- The `/ping/` endpoint returns a partial template
- The `request.htmx` attribute is available in views (provided by HtmxMiddleware)

## Development

### Code Formatting with Pre-commit

Install pre-commit hooks (runs black, djhtml, and other checks automatically):

```bash
uv run pre-commit install
```

Run checks manually:

```bash
uv run pre-commit run --all-files
```

## Django-HTMX Integration

This project follows the recommended django-htmx setup:

1. **INSTALLED_APPS**: Added `django_htmx`
2. **MIDDLEWARE**: Added `django_htmx.middleware.HtmxMiddleware`
3. **Templates**:
   - Base template loads HTMX via `{% htmx_script %}`
   - CSRF token configured in `hx-headers` on `<body>`
4. **Views**: Can access `request.htmx` to detect HTMX requests

## License

This is a template project for educational and development purposes.
