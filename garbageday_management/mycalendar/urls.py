from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #スケジュール付き月間カレンダー
    path('',views.myCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/',views.myCalendar.as_view(), name='mycalendar'),
    #nameはhtmlで使用
    # #int:year>/<int:month>で取得した引数はMonthCalendarで**kwargsに格納される

#STATIC_URLで定義した文字列に合致したrequestが送られてきた場合に、STATIC_ROOT(STATIC_ROOTが設定されてなければ、STATICFILES_DIRSをみる)で
# 指定したディレクトリの中のCSSファイルを読み込む
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
