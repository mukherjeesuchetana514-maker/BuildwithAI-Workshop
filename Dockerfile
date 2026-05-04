FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend ./frontend
COPY backend ./backend

ENV PORT 8080
EXPOSE 8080

CMD ["gunicorn", "--chdir", "backend", "main:app", "-b", "0.0.0.0:8080"]
