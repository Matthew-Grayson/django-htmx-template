# django-htmx-template

A Django project template demonstrating integration with htmx for building modern, dynamic web applications with minimal JavaScript.

## Requirements

- **Python**: 3.11.x or newer
- **Django**: 4.2+ (LTS) or 5.x
- **uv**: Modern Python package manager (recommended for dependency management)

## Local Setup (uv)

### First-time setup

1. **Initialize the project** (if not already done):
   ```bash
   uv init --python 3.11
   ```

2. **Create a virtual environment**:
   ```bash
   uv venv
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```
   
   Or, if building incrementally:
   ```bash
   uv add django django-htmx
   uv add --dev black djhtml pre-commit django-extensions
   ```

4. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   uv run python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/` in your browser.

### Activating the virtual environment (alternative)

If you prefer to activate the virtual environment instead of using `uv run`:

```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

Then run commands without the `uv run` prefix:
```bash
python manage.py runserver
```

## Project Layout

This project follows Django conventions with a clear separation between project configuration and application code:

```
django-htmx-template/
├── config/                 # Django project package (settings, URLs, WSGI)
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── <app_name>/            # Your Django application (e.g., "core", "web")
│   ├── migrations/
│   ├── templates/         # App-specific templates
│   │   ├── <app_name>/    # Namespaced templates
│   │   │   ├── base.html
│   │   │   └── index.html
│   │   └── partials/      # htmx fragment templates
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/             # Optional: global/shared templates
├── static/                # Static files (CSS, JS, images)
├── manage.py
├── pyproject.toml         # Project dependencies and metadata
├── uv.lock                # Locked dependency versions
└── README.md
```

### Why this layout?

- **`config/`**: Holds project-wide settings, not application logic. Keeps the root directory clean.
- **`<app_name>/templates/`**: Each app owns its templates, following Django's `APP_DIRS` pattern. This makes apps more portable and self-contained.
- **`templates/` (optional)**: Use this for truly global templates that don't belong to any specific app.
- **`partials/`**: A convention for organizing htmx-specific fragment templates that are loaded dynamically.

## django-htmx Integration

This project uses [`django-htmx`](https://github.com/adamchainz/django-htmx) to simplify integration with htmx.

### Setup

1. **Add to `INSTALLED_APPS`** in `config/settings.py`:
   ```python
   INSTALLED_APPS = [
       # ...
       "django_htmx",
       # ...
   ]
   ```

2. **Add middleware** in `config/settings.py`:
   ```python
   MIDDLEWARE = [
       # ...
       "django_htmx.middleware.HtmxMiddleware",
       # ...
   ]
   ```
   
   This middleware enables `request.htmx` in your views, which lets you detect htmx requests and access htmx-specific headers.

### Base Template Requirements

Your base template should include:

```html
{% load django_htmx %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My App{% endblock %}</title>
    {% htmx_script %}
</head>
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
    {% block content %}{% endblock %}
</body>
</html>
```

**Key points:**
- `{% load django_htmx %}` at the top
- `{% htmx_script %}` in `<head>` — loads htmx from CDN and includes django-htmx extensions
- `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on `<body>` — ensures htmx POST/PUT/DELETE requests include the CSRF token

### Using `request.htmx` in Views

```python
def my_view(request):
    if request.htmx:
        # Return a partial template for htmx requests
        return render(request, "partials/fragment.html", context)
    else:
        # Return a full page for regular requests
        return render(request, "app_name/page.html", context)
```

## Developer Tooling

### Pre-commit Hooks

This project uses `pre-commit` to automatically format and lint code before commits.

1. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

2. **Run manually** (optional):
   ```bash
   uv run pre-commit run --all-files
   ```

### Formatting

- **Python**: `black`
  ```bash
  uv run black .
  ```

- **Templates**: `djhtml` (Django template formatter)
  ```bash
  uv run djhtml <app_name>/templates/
  ```

### Linting

Add linters like `ruff` or `flake8` as needed:
```bash
uv add --dev ruff
uv run ruff check .
```

## Common Commands (via uv)

```bash
# Create new migrations after model changes
uv run python manage.py makemigrations

# Apply migrations to the database
uv run python manage.py migrate

# Create a superuser for Django admin
uv run python manage.py createsuperuser

# Start development server
uv run python manage.py runserver

# Open Django shell with app models loaded
uv run python manage.py shell

# Run tests
uv run python manage.py test

# Collect static files for production
uv run python manage.py collectstatic
```

## Troubleshooting

### Missing `request.htmx` attribute

**Symptom**: `AttributeError: 'WSGIRequest' object has no attribute 'htmx'`

**Solution**: Ensure `HtmxMiddleware` is added to `MIDDLEWARE` in `config/settings.py`:
```python
MIDDLEWARE = [
    # ...
    "django_htmx.middleware.HtmxMiddleware",
    # ...
]
```

### htmx POST requests return 403 (Forbidden)

**Symptom**: htmx POST/PUT/DELETE requests fail with 403 errors.

**Solution**: Add the CSRF token to htmx requests. In your base template:
```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
```

This ensures all htmx requests include the CSRF token in their headers.

### Static files not loading

**Symptom**: CSS/JS files return 404 in development.

**Solution**: 
1. Ensure `django.contrib.staticfiles` is in `INSTALLED_APPS`
2. Set `STATIC_URL = "static/"` in settings
3. For development, Django serves static files automatically when `DEBUG=True`

### Templates not found

**Symptom**: `TemplateDoesNotExist` error.

**Solution**:
1. Ensure `APP_DIRS=True` in the `TEMPLATES` setting
2. Check that your app is in `INSTALLED_APPS`
3. Verify template path follows Django's convention: `<app_name>/templates/<app_name>/template.html`

## Next Steps

- Explore the [django-htmx documentation](https://django-htmx.readthedocs.io/)
- Read the [htmx documentation](https://htmx.org/docs/)
- Check out [django-htmx examples](https://github.com/adamchainz/django-htmx/tree/main/example)
- Learn about [Django best practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)

## Contributing

Contributions are welcome! Please follow the existing code style and run pre-commit hooks before submitting pull requests.

## License

[Add your license here]