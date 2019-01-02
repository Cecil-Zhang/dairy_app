# Dairy_App
Python Dairy Web App

pip install django
pip install mysqlclient

python manage.py runserver

## DB change
1. Change your models (in models.py).
2. Run python manage.py makemigrations to create migrations for those changes
3. Run python manage.py sqlmigrate APP_NAME IDX to view db changes
3. Run python manage.py migrate to apply those changes to the database.