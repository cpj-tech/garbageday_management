from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    #admin以外のurlの場合、全てmycalendarのurls.pyに遷移する
    path('', include('mycalendar.urls')),
    path('garbageday/', include('garbageday.urls')),
    path('line/', include('line.urls')),
]
