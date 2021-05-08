from django import forms
from garbageday.models import Garbageday

class GarbageDayForm(forms.ModelForm):
    class Meta:
        model = Garbageday
        fields = ('garbage_type', 'week1', 'week2', 'day_of_week1', 'day_of_week2',
                'manage_alarm', 'alarm_day', 'alarm_time')