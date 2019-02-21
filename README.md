# Dairy_App
Python Diary Web App

        pip install -r requirements.txt
        python manage.py migrate
        python manage.py collectstatic
        python manage.py runserver

## Apply DB change
1. Change your models (in models.py).
2. Run python manage.py makemigrations to create migrations for those changes
3. Run python manage.py sqlmigrate APP_NAME IDX to view db changes
3. Run python manage.py migrate to apply those changes to the database.

## Management command
- Export Diary to PDF: `python manage.py exportpdf`

## Local Run with uWSGI
`uwsgi --http :8000 --module mysite.wsgi`

# Environment in TecentCloud
### Django Directory
/home/ubuntu/git/dairy_app  

### uWSGI Unit Service
*/etc/systemd/system/emperor.uwsgi.service*

**Notes:**
- Running in uWSGI Emperor Mode
- *emperor.ini* put in */etc/uwsgi/*
- *app.ini* file put in */etc/uwsgi/vassals*

### Nginx Configuration
- Configuration file in */etc/nginx/sites-available*