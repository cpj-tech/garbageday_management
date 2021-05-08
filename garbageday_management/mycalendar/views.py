"""mycalendar views.py
    * A function that displays a scheduled monthly calendar
"""

from django.views import generic
from . import mixins
from garbageday.models import Garbageday
import logging
from django.shortcuts import redirect
logger = logging.getLogger(__name__)

class myCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    template_name = 'mycalendar/mycalendar.html'
    # Specifies which database table to use in the models.py file
    model = Garbageday

    def get_context_data(self, **kwargs):
        context = {}
        #If there is no lineid, it will transition to line login error
        try:
            logger.info('Calendar information acquisition start')
            context = super().get_context_data(**kwargs)
            calendar_context = self.get_month_calendar()
            context.update(calendar_context)
            logger.info('Successful acquisition of calendar information')
        except :
            logger.info('line login error')
            self.template_name = 'line/linelogin_error.html'
        return context
       
            