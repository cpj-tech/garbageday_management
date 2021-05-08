"""
WSGI config for garbageday_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import threading


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garbageday_management.settings')
application = get_wsgi_application()

from line import line_push
#Loop the DB and push the data of the notification time that matches the current time.
t1=threading.Thread(target=line_push.db_roop)
t1.start()
print('DB_ROOP STARTED')
