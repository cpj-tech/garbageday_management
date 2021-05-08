"""garbageday views

    * use to control the garbageday data

"""
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Garbageday, Line
from .forms import GarbageDayForm
from line.models import Line
from django.contrib import messages
import logging
from package import clsOperateLineId

logger = logging.getLogger(__name__)
operate_lineid = clsOperateLineId.OperateLineId()

class IndexView(View):
    """IndexView"""

    def get(self, request, *args, **kwargs):
        """ IndexView get()

        If the user is logged in, display the data associated with line_id in session_id.
        Otherwise, the line login error screen will be displayed.

        Args:
            self:instance
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the garbage day list screen
            error:Display the line login error screen

        """
        logger.info('Garbageday information list acquisition start.')
        if 'line_id' in request.session and request.session['line_id'] != '':
            #Get the data associated with line_id in session_id
            garbageday_data = Garbageday.objects.filter(line_id=operate_lineid.encrypt(request.session['line_id']))
            logger.info('Garbageday information list display.')
            return render(request, 'garbageday/index.html', {
                'garbageday_data': garbageday_data,
                'display_name':self.kwargs['display_name'],
            })
        else:
            #go to line login screen
            logger.info('line login error')
            return redirect('/line/linelogin_error')

class GarbagedayDetailView(View):
    """GarbagedayDetailView"""

    def get(self, request, *args, **kwargs):
        """ GarbagedayDetailView get()

        If the user is logged in, display the detail data associated with line_id in session_id.
        Otherwise, the line login error screen will be displayed.

        Args:
            self:instance
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the garbage day detail screen
            error:Display the line login error screen

        """
        logger.info('Garbageday detailed information acquisition start.')
        #Display index if logged in, otherwise return to line login screen
        try:
            garbageday_data = Garbageday.objects.get(id=self.kwargs['pk'],line_id=operate_lineid.encrypt(request.session['line_id']))            
            logger.info('Garbageday detailed information display')
            return render(request, 'garbageday/garbageday_detail.html', {
                'garbageday_data': garbageday_data,
                'display_name':self.kwargs['display_name']
            })
        except:
            logger.info('line login error')
            return redirect('/line/linelogin_error')

    def post(self, request, *args, **kwargs):
        """ GarbagedayDetailView post()

        When the user in the login status and push the delete button, 
        the selected data is deleted from the DataBase.
        Otherwise, the line login error screen will be displayed.

        Args:
            self:instance　
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the garbage day detail screen
            error:Display the line login error screen


        """
        if 'line_id' in request.session and request.session['line_id'] != '':
            logger.info('Garbageday deletion information acquisition start.')
            delete_data = Garbageday.objects.get(line_id=operate_lineid.encrypt(request.session['line_id']), id=self.kwargs['pk'])
            delete_data.delete()
            messages.info(request, '{}を削除しました。'.format(delete_data.get_garbage_type_display()))
            logger.info('Garbageday information deleted.')
            return redirect('garbageday', self.kwargs['display_name'])
        else:
            logger.info('line login error')
            return redirect('/line/linelogin_error')


class CreateGarbagedayView(View):
    """CreateGarbagedayView"""

    def get(self, request, *args, **kwargs):
        """ CreateGarbagedayView get()

        When the user in the login status , 
        display the form screen.
        Otherwise, the line login error screen will be displayed.

        Args:
            self:instance
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the form screen
            error:Display the line login error screen

        """
        logger.info('Get form information for garbageday creation.')
        if 'line_id' in request.session and request.session['line_id'] != '':
            form = GarbageDayForm(request.POST or None)
            logger.info('Successful acquisition of form information for garbageday creation.')
            return render(request, 'garbageday/garbageday_form.html', {
                'form': form,
                'display_name':self.kwargs['display_name']
            })
        else:
            logger.info('line login error')
            return redirect('/line/linelogin_error')
    
    def post(self, request, *args, **kwargs):
        """ CreateGarbagedayView post()

        When the registration button is pressed, 
        the garbage day data is registered in the DB.

        Args:
            self:instance
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the garbageday list screen
            Data already registered:Display the form screen
            error:Display the line login error screen


        """
        logger.info('Garbageday creation information acquisition start.')
        line_id = Line.objects.get(id=operate_lineid.encrypt(request.session['line_id']))
        form = GarbageDayForm(request.POST or None)
        # Checking if the field specified in forms.py exists in POST
        if form.is_valid():
            if form.cleaned_data['manage_alarm']:
                if form.cleaned_data['alarm_day'] ==None or form.cleaned_data['alarm_time'] ==None:
                    logger.error('An error in which the alarm is ON but the set date or notification time are not entered.')
                    messages.error(request, 'アラームONの場合は設定日と通知時間を入力してください。')
                    return redirect('garbageday_new', self.kwargs['display_name'])
            is_garbagedatas = Garbageday.objects.filter(line=line_id, garbage_type=form.cleaned_data['garbage_type'])
            garbageday_data = Garbageday()
            garbageday_data.line = line_id
            garbageday_data.binary_lineid = operate_lineid.encrypt(request.session['line_id'])
            garbageday_data.garbage_type = form.cleaned_data['garbage_type']
            # If there is a registered garbage type, the garbage day creation screen is redisplayed.
            for is_garbagedata in is_garbagedatas:
                if is_garbagedata.garbage_type == form.cleaned_data['garbage_type']:
                    logger.error('An Error that there is already a registered garbage type.')
                    messages.error(request, '{}は登録済みです。'.format(garbageday_data.get_garbage_type_display()))
                    return redirect('garbageday_new', self.kwargs['display_name'])
            garbageday_data.week1 = form.cleaned_data['week1']
            garbageday_data.week2 = form.cleaned_data['week2']
            garbageday_data.day_of_week1 = form.cleaned_data['day_of_week1']
            garbageday_data.day_of_week2 = form.cleaned_data['day_of_week2']
            garbageday_data.manage_alarm = form.cleaned_data['manage_alarm']
            garbageday_data.alarm_day = form.cleaned_data['alarm_day']
            garbageday_data.alarm_time = form.cleaned_data['alarm_time']
            garbageday_data.save()
            logger.info('Successful addition of garbageday information.')
            messages.info(request, '{}を登録しました。'.format(garbageday_data.get_garbage_type_display()))
            return redirect('garbageday', self.kwargs['display_name'])

        return render(request, 'garbageday/garbageday_form.html', {
            'form': form,
            'display_name':self.kwargs['display_name']
        })

class GarbagedayEditView( View):
    """GarbagedayEditView"""

    def get(self, request, *args, **kwargs):
        """ GarbagedayEditView get()

        When the edit button is pressed, 
        Display a screen where you can edit the garbage schedule.
        If you are not logged in, a login error screen will be displayed.

        Args:
            self:instance
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the form  screen
            error:Display the line login error screen

        """
        logger.info('Get form information for garbageday edit.')
        try:
            garbageday_data = Garbageday.objects.get(id=self.kwargs['pk'],line_id=operate_lineid.encrypt(request.session['line_id']))
            form = GarbageDayForm(
                request.POST or None,
                initial={
                    'garbage_type': garbageday_data.garbage_type,
                    'week1': garbageday_data.week1,
                    'week2': garbageday_data.week2,
                    'day_of_week1': garbageday_data.day_of_week1,
                    'day_of_week2': garbageday_data.day_of_week2,
                    'manage_alarm': garbageday_data.manage_alarm,
                    'alarm_day': garbageday_data.alarm_day,
                    'alarm_time': garbageday_data.alarm_time,
                }
            )
            logger.info('Successful acquisition of form information for garbageday edit.')
            return render(request, 'garbageday/garbageday_form.html', {
                'form': form,
                'display_name':self.kwargs['display_name']
            })
        except:
            logger.info('line login error')
            return redirect('/line/linelogin_error')

    def post(self, request, *args, **kwargs):
        """ GarbagedayEditView post()

        When the registration button is pressed, 
        the edited data is registered in the DB.

        Args:
            self:instance
            request:request
            *args:nothing
            **kwargs:Parameters got by url

        Returns:
            normal:Display the garbageday list screen
            error:Display the form screen

        """
        logger.info('Garbageday editing information acquisition start.')
        line_id = Line.objects.get(id=operate_lineid.encrypt(request.session['line_id']))
        form = GarbageDayForm(request.POST or None)
        garbageday_data = Garbageday.objects.get(id=self.kwargs['pk'])
        if form.is_valid():
            if form.cleaned_data['manage_alarm']:
                if form.cleaned_data['alarm_day'] ==None or form.cleaned_data['alarm_time'] ==None:
                    logger.error('An error in which the alarm is ON but the set date or notification time are not entered.')
                    messages.error(request, 'アラームONの場合は設定日と通知時間を入力してください。')
                    return render(request, 'garbageday/garbageday_form.html', {
                        'form': form,
                        'display_name':self.kwargs['display_name']
                    })
            if not garbageday_data.garbage_type == form.cleaned_data['garbage_type']:
                is_garbagedatas = Garbageday.objects.filter(line=line_id, garbage_type=form.cleaned_data['garbage_type'])
                for is_garbagedata in is_garbagedatas:
                    if is_garbagedata.garbage_type == form.cleaned_data['garbage_type']:
                        logger.error('An Error that there is already a registered garbage type.')
                        messages.error(request, '{}は登録済みです。'.format(is_garbagedata.get_garbage_type_display()))
                        return render(request, 'garbageday/garbageday_form.html', {
                            'form': form,
                            'display_name':self.kwargs['display_name']
                        })
            garbageday_data.line = line_id
            garbageday_data.binary_lineid = operate_lineid.encrypt(request.session['line_id'])
            garbageday_data.garbage_type = form.cleaned_data['garbage_type']
            garbageday_data.week1 = form.cleaned_data['week1']
            garbageday_data.week2 = form.cleaned_data['week2']
            garbageday_data.day_of_week1 = form.cleaned_data['day_of_week1']
            garbageday_data.day_of_week2 = form.cleaned_data['day_of_week2']
            garbageday_data.manage_alarm = form.cleaned_data['manage_alarm']
            garbageday_data.alarm_day = form.cleaned_data['alarm_day']
            garbageday_data.alarm_time = form.cleaned_data['alarm_time']
            garbageday_data.save()
            logger.info('Successful editing of form information for garbageday edit.')
            messages.info(request, '{}を編集しました。'.format(garbageday_data.get_garbage_type_display()))
            return redirect('garbageday', self.kwargs['display_name'])

        return render(request, 'garbageday/garbageday_form.html', {
            'form': form,
            'display_name':self.kwargs['display_name']
        })




