from django.urls import path
from garbageday import views


urlpatterns = [
    path('<str:display_name>', views.IndexView.as_view(), name='garbageday'),
    path('mygarbageday/<str:display_name>/<int:pk>', views.GarbagedayDetailView.as_view(), name='garbageday_detail'),
    path('mygarbageday/<str:display_name>/new', views.CreateGarbagedayView.as_view(), name='garbageday_new'),
    path('mygarbageday/<str:display_name>/<int:pk>/edit', views.GarbagedayEditView.as_view(), name='garbageday_edit'),
]
