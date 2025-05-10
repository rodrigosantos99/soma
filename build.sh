#!/usr/bin/env bash

# Exit on any error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files without prompt
python manage.py collectstatic --no-input