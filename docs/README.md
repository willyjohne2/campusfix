# CampusFix

This repository contains the CampusFix Django application.

Deployment notes

- Set environment variables (see `.env.example`).
- Use PostgreSQL in production and set `DATABASE_URL` accordingly.
- Render: set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `ALLOWED_HOSTS`, and DB/SMTP credentials in the Render dashboard.

Local development

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
