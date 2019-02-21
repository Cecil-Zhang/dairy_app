# Dairy_App Backend
Python Diary Web App built on top of django + vue + bootstrap + MySQL (Adaptive to Phone and Computer)
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
### Production Environment

#### Dairy Configuration
Step 1 ~ 5 in > Local Environment
Here we will not run development server with `manage.py`, host in WSGI server with [wsgi.py](https://github.com/Cecil-Zhang/dairy_app/tree/master/mysite/mysite/wsgi.py) instead

#### uWSGI and Unix Socket Configuration
Flow work as following
```
 Unix Socket <-> uWSGI <-> Django
```
We use uWSGI as our WSGI server with its [emperor mode](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#emperor-mode)
1. uWSGI emperor mode configuration file, save it as `emperor.ini` in `/etc/uwsgi/`
    ```
    [uwsgi]
    emperor = /etc/uwsgi/vassals
    uid = www-data
    gid = www-data
    vassal-set = threads=2
    vassal-set = chmod-socket=660
    ```
2. Start dairy_app as vassal of uWSGI emperor, save it as `dairy_app.ini` in `/etc/uwsgi/vassals/`
    ```
    [uwsgi]
    chdir = /path/to/dairy_app/mysite/
    module = mysite.wsgi.         # start of dairy_app
    logto = /var/log/uwsgi/%n.log # log file
    socket = /run/uwsgi/%n.sock   # unix socket file
    master = true
    vacum = true
    ```
3. After starting, you should see a unix socket file `dairy_app.sock` in `/run/uwsgi/` and logger file in `/var/log/uwsgi`

#### Nginx Configuration
Use nginx as proxy server, the flow works as following
```
 web client <-> Nginx <-> Unix Socket
```
1. Install Nginx
2. Configure Nginx
    - Configure Nginx listening path and connect to django (unix socket here)
    ```
    server {
        listen      80;
        server_name dairy_app; # substitute your machine's IP address or FQDN
        charset     utf-8;
        client_max_body_size 75M;   # adjust to taste
        
        # Django media
        location /media  {
            alias /var/dairy_app/media;  # your Django project's media files - amend as required      
        }
        
        # location /static {
        #     alias /home/ubuntu/git/dairy_app/mysite/static; # your Django project's static files - amend as required
        #  }

        # Finally, send all non-media requests to the Django server.
        location /api/v1 {
            rewrite ^/api/v1(.*) $1 break;
            uwsgi_pass  django;
            include     /home/ubuntu/git/dairy_app/uwsgi_conf/uwsgi_params; # the uwsgi_params file you installed 
        }
        ...
    }  
    ```
    - Save it to /etc/nginx/sites-available/dairy_app.conf, [example](https://github.com/Cecil-Zhang/dairy_app/blob/master/uwsgi_conf/dairy_app.conf)
    - Create Symlink so that Nginx can see it
    ```
    sudo ln -s /etc/nginx/sites-available/dairy_app.conf /etc/nginx/sites-enabled/
    ```
3. Start Nginx
    ```
    nginx start
    ```


#### Start uWSGI with `systemctl`
1. Save it as `/etc/systemd/system/emperor.uwsgi.service`
```
[Unit]
Description=Dairy Diary App running on uWSGI
After=syslog.target

[Service]
User=www-data
Group=www-data
RuntimeDirectory=uwsgi
ExecStart=/path/to/dairy_app/venv/bin/uwsgi --ini /etc/uwsgi/emperor.ini
Environment="PATH=/path/to/dairy_app/venv/bin"
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
2. Manage uWSGI as systemd service
```
systemctl start/status/stop emperor.uwsgi.service
```


## Development
### Apply DB change
1. Change your models (in models.py).
2. Run python manage.py makemigrations to create migrations for those changes
3. Run python manage.py sqlmigrate APP_NAME IDX to view db changes
3. Run python manage.py migrate to apply those changes to the database.

### Local Run with uWSGI
`uwsgi --http :8000 --module mysite.wsgi`

## Management command
- Export Diary to PDF: `python manage.py exportpdf`

### To set up scheduler job to export diaries as pdf
1. `sudo crontab -e`
2. Append `@monthly /path/to/venv/bin/python /path/to/dairy_app/mysite/manage.py exportpdf` to the crontab
3. Then the first day in each month, all diaries in last month will be exported to `BACKUP_ROOT` configured in settings.py as pdf

## Environment in TecentCloud
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
