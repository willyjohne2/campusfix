FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["gunicorn", "campusFix.wsgi:application", "--bind", "0.0.0.0:8000"]