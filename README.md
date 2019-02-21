# Dairy_App
Python Diary Web App (Adaptive to Phone and Computer)
Preview at [Screenshots](https://github.com/Cecil-Zhang/dairy_app/tree/master/screenshots)

## Installation
### Local Environment
1. Clone source code
```
$ git clone git@github.com:Cecil-Zhang/dairy_app.git
$ cd /path/to/dairy_app/
```
2. Create a virtual environment
```
$ python3 -m venv venv  # create a virtual environment in root folder
$ . venv/bin/activate   # activate virtual environtment
```
3. Install python library
```
$ pip install -r requirements.txt # install dependencies required by dairy app
```
4. Configure database
    - Configure database connection in `mysite/mysite/settings.py`
        ```
        DATABASES = {
                'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'dairy',
                'USER': 'dairy',
                'PASSWORD': '****',
                'OPTIONS': {
                            'charset': 'utf8mb4',
                            'use_unicode': True, }
            }
        }
        ```
    - Apply DDL
        ```
        $ python mysite/manage.py migrate
        ```
5. Collect static files into static folder [STATICFILES_FINDERS](https://docs.djangoproject.com/en/2.1/intro/tutorial06/)
    ```
    $ python mysite/manage.py runserver
    ```
6. Start server
    ```
    $ python mysite/manage.py runserver
    ```


## Apply DB change
1. Change your models (in models.py).
2. Run python manage.py makemigrations to create migrations for those changes
3. Run python manage.py sqlmigrate APP_NAME IDX to view db changes
3. Run python manage.py migrate to apply those changes to the database.

## Management command
- Export Diary to PDF: `python manage.py exportpdf`

## To set up scheduler job to export diaries as pdf
1. `sudo crontab -e`
2. Append `@monthly /path/to/venv/bin/python /path/to/dairy_app/mysite/manage.py exportpdf` to the crontab
3. Then the first day in each month, all diaries in last month will be exported to `BACKUP_ROOT` configured in settings.py as pdf

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
