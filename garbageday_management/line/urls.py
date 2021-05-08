from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('linelogin/', views.line_login, name='linelogin'),
    path('linelogin_success/', views.linelogin_success),
    path('linelogin_error/', views.linelogin_error, name='linelogin_error'),
    path('callback/', views.callback, name='callback'),

#STATIC_URLで定義した文字列に合致したrequestが送られてきた場合に、STATIC_ROOT(STATIC_ROOTがなければ、STATICFILES_DIRSをみる)で
# 指定したディレクトリの中のCSSファイルを読み込む
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
