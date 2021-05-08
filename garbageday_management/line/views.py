"""line views.py

    * Functions at the time of line login
    * Function when line callback occurs
"""

import datetime
import requests
import json
import jwt
from django.shortcuts import redirect,render
from garbageday.models import Garbageday
from .models import Line,LineUserName
from Crypto.Cipher import AES
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from linebot.models import TextSendMessage
from package import clsGetDate, clsGetLineInfo, clsOperateLineId
from line import line_push
import threading
import logging
from middleware import custom_logging
import os


#log setting
logger = logging.getLogger(__name__)
LOG＿DIR = "/var/log/"

#An instance of a class that encrypts the line id
operate_lineid = clsOperateLineId.OperateLineId()

#An instance of a class that get the line information
get_line_info = clsGetLineInfo.GetLineInfo()



def line_login(request):
    """line_login()

        A function that executes a line login request.

        Args:
            request : request

        Returns:
            returns the line login request

    """
    logger.info('Start creating information for Line login')
    random_state = os.urandom(16)
    channel_id = get_line_info.line_channel_id
    redirect_url = get_line_info.redirect_url
    logger.info('Information creation for Line login completed')
    return redirect(f'https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={channel_id}&redirect_uri={redirect_url}&state={random_state}&scope=openid%20profile')


def linelogin_success(request):
    """linelogin_success()

        IF line login authentication is successful, 
        the encrypted line_id is registered in the DB.
        
        If line login authentication fails, 
        the screen will change to the line_login_error screen.


        Args:
            request : request

        Returns:
            login_success : change to mycalendar screen
            login_fails: change to linelogin_error screen

    """
    #  Get an user infomation
    if request.GET.get('error') == None:
        # Get an authorization code
        request_code = request.GET.get('code')
        uri_access_token = "https://api.line.me/oauth2/v2.1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data_params = {
            "grant_type": "authorization_code",
            "code": request_code,
            "redirect_uri": get_line_info.redirect_url,
            "client_id": get_line_info.line_channel_id,
            "client_secret": get_line_info.line_channel_secret
        }
        # Send a request to get an access token
        response_post = requests.post(
            uri_access_token, headers=headers, data=data_params)
        # use the id_token
        line_id_token = json.loads(response_post.text)["id_token"]
        # Get user information by decoding the pay_load part
        user_profile = jwt.decode(line_id_token,
                                    get_line_info.line_channel_secret,
                                    audience=get_line_info.line_channel_id,
                                    issuer='https://access.line.me',
                                    algorithms=['HS256'])

        # Encryption process
        enc_lineid = operate_lineid.encrypt(user_profile['sub'])

        # Register line_id in session
        request.session['line_id'] = user_profile['sub']
        # Register line_display_name in session
        request.session['name'] = user_profile['name']

        now = datetime.datetime.now()
        log_path = LOG＿DIR + os.path.sep + "line.log"
        massage = 'Successful line login authentication!!'
        with open(log_path, "a") as f:
            f.write('{now} [INFO] ./mycalendar/views.py:47 user={name} {massage}'.format(now=now, name=user_profile['name'], massage=massage))
    
        # DB registration for the first time, skip for the second and subsequent times
        db_line = ""
        try:
            db_line=Line.objects.get(id=enc_lineid)
        except:
            pass
        if  db_line == "":
            obj_lineid = Line.objects.create(id=enc_lineid)
            LineUserName.objects.create(line=obj_lineid, display_name=user_profile['name'])
        return HttpResponseRedirect(reverse('mycalendar', args=request))
    else:
        # In case of authentication error, please go back and log in again.
        error = request.GET.get('error')
        error_description = request.GET.get('error_description')
        state = request.GET.get('state')
        logger.info(f'linelogin_success error {error}')
        logger.info(f'linelogin_success error {error_description}')
        return redirect('/line/linelogin_error')
        
def linelogin_error(request):
    """linelogin_error()

        request the linelogin_error screen

        Args:
            request : request

        Returns:
            change to linelogin_error screen

    """
    
    return render(request, 'line/linelogin_error.html')

def linebot_push(user_id, reply_message):
    """linebot_push()

        Function to push garbage schedule for 1 week or 1 month

        Args:
            user_id　str : line_id to push
            reply_message str: Weekly or monthly garbage schedule information

    """
    
    logger.info('Line API response information transmission preparation.')
    messages = TextSendMessage(text=reply_message)
    get_line_info.line_bot_api.push_message(user_id, messages)
    logger.info('Line API response information transmission completed.')

    
def make_set_data(data, get_date, year, month, nth_week, day_of_week, get_day_of_week_display):
    """make_set_data()

        Function to set line_push information to dict

        Args:
            data queryset: DB 1 record queryset
            get_date obj: Instance of the class to get the date
            year int : Current year
            month int: Current month
            nth_week int: Current week_number
            day_of_week int: week_number registered in DB
            get_day_of_week_display: day_of_week_display registered in DB

        Returns:
            retun the  line_push information as dict

    """
    logger.info('Start creating garbage day information for reply.')
    set_data = {}
    date=get_date.get_date_of_nth_dow(year, month ,nth_week, day_of_week)
    set_data['date'] = str(date.strftime ('%Y年%m月%d日'))
    set_data['garbage_type'] = data.get_garbage_type_display()
    set_data['day'] = date.day
    set_data['day_of_week_display'] = get_date.get_week(get_day_of_week_display)
    logger.info('Completion of garbage day information creation for reply.')
    return set_data

def make_reply_message(enc_lineid, text):
    """make_reply_message()

        Function to set line_push information to dict

        Args:
            enc_lineid str: Encrypted line_id
            text str: message obtained from line
            
        Returns:
            Arrange the message in the form for line_push

    """
    logger.info('Start composing a reply message.')
    messages = {}
    set_list = []
    reply_data = ''
    i = 0
    every_week=[1,2,3,4,5]
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    get_date = clsGetDate.GetDate()
    if text == '1週間の予定':
        #Get what week number the current date is
        nth_week = get_date.get_nth_week2_datetime(year,month,day)
        queryset=Garbageday.objects.filter(line=enc_lineid)
        for data in queryset:
            if data.week1 == 0:
                try:
                    set_data = make_set_data(data, get_date,year,month,nth_week, data.day_of_week1, data.get_day_of_week1_display())
                    messages[i] = set_data
                    i+=1
                except:
                    pass
                if not data.day_of_week2==None:
                    try:
                        set_data = make_set_data(data, get_date, year, month, nth_week, data.day_of_week2, data.get_day_of_week2_display())
                        messages[i] = set_data
                        i+=1
                    except:
                        pass
                    continue
            elif data.week1 == nth_week:
                try:
                    set_data = make_set_data(data, get_date,year,month,nth_week, data.day_of_week1, data.get_day_of_week1_display())
                    messages[i] = set_data
                    i+=1
                except:
                    pass
                if not data.day_of_week2==None:
                    try:
                        set_data = make_set_data(data, get_date, year, month, nth_week, data.day_of_week2, data.get_day_of_week2_display())
                        messages[i] = set_data
                        i+=1
                    except:
                        pass
                    continue
            elif data.week2 == nth_week:
                try:
                    set_data = make_set_data(data, get_date, year, month, nth_week, data.day_of_week1, data.get_day_of_week1_display())
                    messages[i] = set_data 
                    i+=1
                except:
                    pass
        if len(messages) >= 1:
            #Sort by date in ascending order
            for i in messages:
                set_list.append(messages[i])
            send_data = sorted(set_list, key=lambda x: x['day'])
            for data in send_data:
                if data["date"] in reply_data:
                    reply_data = reply_data[:-1]+f'  {data["garbage_type"]}\n'
                else:
                    reply_data = reply_data + f'{data["date"]}{data["day_of_week_display"]}  {data["garbage_type"]}\n'

            reply_message = f'1週間の予定は以下になります。\n{reply_data}'
            logger.info('Weekly reply message: Garbageday schedule created.')
        else:
            reply_message = "1週間の予定はありません。"
            logger.info('Weekly reply message: Garbageday schedule is empty.')
    elif text =='1ヶ月の予定':
        queryset=Garbageday.objects.filter(line=enc_lineid)
        for data in queryset:
            if data.week1 == 0:
                for week in every_week:
                    week1= week
                    try:
                        set_data = make_set_data(data, get_date, year, month, week1, data.day_of_week1, data.get_day_of_week1_display())
                        messages[i] = set_data
                        i+= 1
                    except:
                        pass
                if not data.day_of_week2==None:
                    for week in every_week:
                        week1= week
                        try:
                            set_data = make_set_data(data, get_date, year, month, week1, data.day_of_week2, data.get_day_of_week2_display())
                            messages[i] = set_data
                            i+=1
                        except:
                            pass
                    continue
            elif not data.week1 == 0:
                try:
                    set_data = make_set_data(data, get_date, year, month, data.week1, data.day_of_week1, data.get_day_of_week1_display())
                    messages[i] = set_data
                    i+=1
                except:
                    pass
                if not data.day_of_week2==None:
                    try:
                        set_data = make_set_data(data, get_date, year, month, data.week1, data.day_of_week2, data.get_day_of_week2_display())
                        messages[i] = set_data
                        i+=1
                    except:
                        pass
                    continue
                if not data.week2 == None :
                    try:
                        set_data = make_set_data(data, get_date, year, month, data.week2, data.day_of_week1, data.get_day_of_week1_display())
                        messages[i] = set_data
                        i+=1
                    except:
                        pass
        #Sort by date in ascending order
        for i in messages:
            set_list.append(messages[i])
        send_data = sorted(set_list, key=lambda x: x['day'])
        for data in send_data:
            if data["date"] in reply_data:
                reply_data = reply_data[:-1]+f'  {data["garbage_type"]}\n'
            else:
                reply_data = reply_data + f'{data["date"]}{data["day_of_week_display"]}  {data["garbage_type"]}\n'
        reply_message = f'1ヶ月の予定は以下になります。\n{reply_data}'
        logger.info('monthly reply message: Garbageday schedule created.')
    else:
        reply_message = '申し訳ございませんが、個別のお問い合わせには対応しておりません。'
        logger.info('Unacceptable reply message: Unresponsive message creation.')
    logger.info('Send the created the message.')
    return reply_message



@csrf_exempt
def callback(request):
    """callback()

        Called when receiving a line_message or deleting a line account.

        Args:
            request: request
            
        Returns:
            Arrange the message in the form for line_push

    """
    logger.info('Get Line API request information.')
    if request.method == 'POST':
        request_json = json.loads(request.body.decode('utf-8'))
        events = request_json['events']
        line_id = events[0]['source']['userId']
        enc_lineid = operate_lineid.encrypt(line_id)

        if 'message' in events[0]:
            if events[0]['message']['type'] == 'text':
                text = events[0]['message']['text']
                #Check if line_id is registered in DB
                if len(Garbageday.objects.filter(line=enc_lineid)) != 0:
                    reply_message = make_reply_message(enc_lineid,text)
                    logger.info('Create LineAPI response information. weekly or monthly.')
                    linebot_push(line_id, reply_message)
                else:
                    if text == '1週間の予定' or text =='1ヶ月の予定':
                        #Response message when line_id is not registered in DB
                        reply_message = "ごみの日が登録されていません。\nメニューのカレンダーボタンからごみの日を登録してください。"
                    else:
                        reply_message = '申し訳ございませんが、個別のお問い合わせには対応しておりません。'
                    logger.info('Create LineAPI response information. Garbageday is not registered.')
                    linebot_push(line_id, reply_message)
        if 'type' in events[0]:
            #When canceling friend registration
            if events[0]['type'] == 'unfollow':
                logger.info('"Garbageday management" has been unfollowed.')
                Line.objects.filter(id=enc_lineid).delete()

    return HttpResponse()



