FROM python:3.10-slim

ENV PYTHONBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "promptingTutor.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "3600"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
