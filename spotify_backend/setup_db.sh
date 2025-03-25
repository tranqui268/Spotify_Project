#!/bin/bash
sudo -u postgres psql -c "CREATE USER spotify_user WITH PASSWORD '123456' CREATEDB;"
source myenv/bin/activate
python manage.py makemigrations
python manage.py migrate