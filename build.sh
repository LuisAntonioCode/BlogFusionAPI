#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# ----------------------------------------------------
# Bloque de Creación de Superusuario
# ----------------------------------------------------
# Solo ejecuta si la variable de control existe
if [ "$CREATE_SUPERUSER" = "True" ]; then
    echo "Intentando crear el superusuario..."
    # El comando --noinput obliga a Django a usar las variables de entorno
    python manage.py createsuperuser --noinput
    echo "Superusuario creado."
fi
# ----------------------------------------------------