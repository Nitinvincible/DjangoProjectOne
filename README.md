# Django Project One

A Django web application project.

## Project Structure

```
DjangoProjectOne/
├── config/              # Project configuration
│   ├── __init__.py
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL routing
│   ├── asgi.py         # ASGI config
│   └── wsgi.py         # WSGI config
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Setup Instructions

### 1. Create a virtual environment (recommended)
```bash
python -m venv venv
```

### 2. Activate the virtual environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Technologies Used

- **Python**: 3.13.7
- **Django**: 5.2.8

## Development

### Running the server
```bash
python manage.py runserver
```

### Creating a new app
```bash
python manage.py startapp app_name
```

### Making migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## License

This project is open source and available under the MIT License.
