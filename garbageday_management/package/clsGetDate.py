"""package clsGetDate.py
    * Class to get the date from the argument
"""
import datetime
import calendar

class GetDate:
    """GetDate"""
    
    def get_nth_week2_datetime(self,year, month, day, firstweekday=0):
        """get_nth_week2_datetime()

        A function that returns the number of weeks from the current date

        Args:
            self: instance
            year int: current year
            month int: current month
            day int: current day
            firstweekday int: 0:Monday,6:Subday
            
        Returns:
            the number of weeks from the current date
        """
        first_dow = datetime.date(year, month, 1).weekday()
        offset = (first_dow - firstweekday) % 7
        return (day + offset - 1) // 7 + 1
        
    

    def _get_day_of_nth_dow(self,year, month, nth, dow):
        """_get_day_of_nth_dow()

        Function to get the date from the argument

        Args:
            self: instance
            year int: current year
            month int: current month
            nth int:　current weeks
            dow int: 0:Monday,6:Subday
            
        Returns:
            the number of weeks from the current date
        """
        if nth < 1 or dow < 0 or dow > 6:
            return None

        first_dow, n = calendar.monthrange(year, month)
        day = 7 * (nth - 1) + (dow - first_dow) % 7 + 1

        return day if day <= n else None
    
    def get_date_of_nth_dow(self,year, month, nth, dow):
        """get_date_of_nth_dow()

        Function to get the date from the argument

        Args:
            self: instance
            year int: current year
            month int: current month
            nth int:　current weeks
            dow int: 0:Monday,6:Subday
            
        Returns:
            current date
        """
        day = self._get_day_of_nth_dow(year, month, nth, dow)
        return datetime.date(year, month, day) if day else None

    def get_week(self,week):
        """get_week()

        Function to get the date from the argument

        Args:
            self: instance
            week str: current day of week
            
            
        Returns:
            current current day of week form ()
        """
        if week == '月曜日':
            return '(月)'
        if week == '火曜日':
            return '(火)'
        if week == '水曜日':
            return '(水)'
        if week == '木曜日':
            return '(木)'
        if week == '金曜日':
            return '(金)'
        if week == '土曜日':
            return '(土)'
        if week == '日曜日':
            return '(日)'