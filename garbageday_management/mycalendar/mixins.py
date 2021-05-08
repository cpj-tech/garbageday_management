import calendar
import datetime
import itertools
from collections import deque
import logging
from line.models import LineUserName
from package import clsGetDate, clsOperateLineId
EVERY_WEEK = [1, 2, 3, 4, 5]
logging.basicConfig(level=logging.DEBUG)

operate_lineid = clsOperateLineId.OperateLineId()


class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    first_weekday = 6  # 0は月曜から、1は火曜から。6なら日曜日からになります。お望みなら、継承したビューで指定してください。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def _setup_calendar(self):
        """内部カレンダーの設定処理

        calendar.Calendarクラスの機能を利用するため、インスタンス化します。
        Calendarクラスのmonthdatescalendarメソッドを利用していますが、デフォルトが月曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理です。

        """
        #月曜日をはじめとするカレンダーモジュールを作成
        self._calendar = calendar.Calendar(self.first_weekday)

    def _get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        #deque()でlistのようなものを生成
        week_names = deque(self.week_names)
         #リスト内の要素を右に1つずつ移動
        week_names.rotate(-self.first_weekday)  
        return week_names

class MonthCalendarMixin(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""

    def _get_previous_month(self, date):
        """前月を返す"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def _get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def _get_month_days(self, date):
        """その月の全ての日を返す"""
        #year 年 month 月の週のリストを返します。
        return self._calendar.monthdatescalendar(date.year, date.month)

    def _get_current_month(self):
        """現在の月を返す"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """月間カレンダー情報の入った辞書を返す"""
        self._setup_calendar()
        current_month = self._get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            #その月の全ての日を返す二次元のリスト
            'month_days': self._get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self._get_previous_month(current_month),
            'month_next': self._get_next_month(current_month),
            #['月', '火', '水'...]といった曜日のリストを返す
            'week_names': self._get_week_names(),
        }
        return calendar_data



class MonthWithScheduleMixin(MonthCalendarMixin):
    """スケジュール付きの、月間カレンダーを提供するMixin"""

    def _get_month_schedules(self, days):
        """１ヶ月のユーザスケジュールを返す"""
        # ユーザのごみの日スケジュールを取得
        queryset = self.model.objects.filter(line=operate_lineid.encrypt(self.request.session['line_id']))
        look_month = days[2][2].month
        # {1日のdatetime: 1日のスケジュール全て, 2日のdatetime: 2日の全て...}のような辞書を作る
        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_dates = self._get_schedule_dates(schedule, look_month)
            for schedule_date in schedule_dates:
            #スケジュールの日付をキーとしてスケジュールデータを辞書に格納
                if schedule_date != None:
                    day_schedules[schedule_date].append(schedule)
        # 日数をsizeへ格納
        size = len(day_schedules)
        #1週間ごとの辞書にしている
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i+7)} for i in range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        #[[datetime.date(2020, 10, 26),~全てのlist
        month_days = calendar_context['month_days']
        calendar_context['month_day_schedules'] = self._get_month_schedules(
            month_days
        )
        if 'line_id' in self.request.session and self.request.session['line_id'] != '':
            #session_idの中のline_idにひもづくデータを取得する
            queryset=LineUserName.objects.filter(line_id=operate_lineid.encrypt(self.request.session['line_id']))
            for line_data in queryset:
                line_display_name=line_data.display_name
            calendar_context['display_name'] = line_display_name

        return calendar_context


    def _get_schedule_dates(self, schedule, look_month):
        today = datetime.date.today()
        today_year = today.year
        schedule_dates = []
        get_date = clsGetDate.GetDate()

        # ごみの日が毎週の場合
        if schedule.week1 == 0:
            for wth in EVERY_WEEK:
                schedule_date1 = get_date.get_date_of_nth_dow(today_year, look_month, wth, schedule.day_of_week1)

                # 曜日２が空ではない場合
                if schedule.day_of_week2 != None:
                    schedule_date2 = get_date.get_date_of_nth_dow(today_year, look_month, wth, schedule.day_of_week2)
                    schedule_dates.append(schedule_date2)
                schedule_dates.append(schedule_date1)
            return schedule_dates

        # ごみの日が毎週以外の場合
        else:
            schedule_date1 = get_date.get_date_of_nth_dow(today_year, look_month, schedule.week1, schedule.day_of_week1)
            # 週２が空ではない場合
            if schedule.week2 != None:
                schedule_date2 = get_date.get_date_of_nth_dow(today_year, look_month, schedule.week2, schedule.day_of_week1)
                schedule_dates.append(schedule_date2)
            # 曜日２が空ではない場合
            if schedule.day_of_week2 != None:
                schedule_date3 = get_date.get_date_of_nth_dow(today_year, look_month, schedule.week1, schedule.day_of_week2)
                schedule_dates.append(schedule_date3)
            schedule_dates.append(schedule_date1)
            return schedule_dates

    