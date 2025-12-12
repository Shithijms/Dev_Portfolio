#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Convert all static files (CSS/Images) for WhiteNoise
python manage.py collectstatic --no-input

# 3. Update the database structure
python manage.py migrate

# 4. (The Special Sauce) Fetch your GitHub projects automatically on deploy
python manage.py fetch_projects