#!/bin/bash

set -e

# Sicherstellen dass die notwendigen Verzeichnisse existieren
mkdir -p /app/logs /app/db

# Timestamp für diese Session
NOW=$(date +"%Y%m%d_%H%M%S")

# Logfile definieren
LOGFILE="/app/logs/startup_${NOW}.log"

# Funktion zum Wiederholen eines Befehls
retry() {
  local n=1
  local max=5
  local delay=5
  while true; do
    "$@" && break || {
      if [[ $n -lt $max ]]; then
        ((n++))
        echo "Command failed. Attempt $n/$max in $delay seconds..."
        sleep $delay;
      else
        echo "The command has failed after $n attempts."
        return 1
      fi
    }
  done
}

# Führe migrationen aus
echo "Applying database migrations ..." | tee -a "$LOGFILE"
retry python manage.py migrate --noinput | tee -a "$LOGFILE"

# Sammle statische Dateien
echo "Collecting static files ..." | tee -a "$LOGFILE"
python manage.py collectstatic --noinput | tee -a "$LOGFILE"

# Erstelle Superuser, falls nicht vorhanden
echo "Creating superuser if it does not exist..." | tee -a "$LOGFILE"
retry python manage.py shell <<EOF | tee -a "$LOGFILE" || true
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
EOF

# Starte Anwendungsserver
exec "$@"
