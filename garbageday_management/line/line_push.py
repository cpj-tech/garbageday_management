"""line line_push

    * Push notification time

"""
import time, datetime
from linebot.models import TextSendMessage
from garbageday.models import Garbageday
from package import clsGetDate, clsGetLineInfo, clsOperateLineId
import base64


def line_push(push_data_list):
    """line_push()

        A function that pushes the argument list one by one.

        Args:
            push_data_list list:Store data to push

        Returns:
            sent_date_time: Returns the pushed time

    """
    operate_lineid = clsOperateLineId.OperateLineId()
    get_line_info = clsGetLineInfo.GetLineInfo()
    print('Start preparing the message.')
    for push_data in push_data_list:   
        if push_data['today_flg'] == 1:
            reply_message =f"明日は{push_data['garbage_type']}の日です。\n"    
        else:
            reply_message =f"今日は{push_data['garbage_type']}の日です。\n"
        messages = TextSendMessage(text=reply_message)    
        dec_lineid = operate_lineid.decrypt(push_data['line_id'])
        get_line_info.line_bot_api.push_message(dec_lineid.decode(), messages)
        time.sleep(0.5)
        print('The message has been sent.')

    sent_date_time = str(datetime.datetime.now())
    sent_date_time = sent_date_time[0:16]

    return sent_date_time


def check_append_data(data, date, push_data_list, push_data_info, current_date_time):
    """check_append_data()

        A function that pushes the argument list one by one.

        Args:
            data obj: record obtained from the database
            date datetime: Date registered in the database
            push_data_list list: list to push
            push_data_info dict: dict to push
            current_date_time datetime : curent date

        Returns:
            push_data_list: Returns the list to push

    """
    #If the alarm setting date is the previous day, reduce  1 day from the date
    if  data.alarm_day == 1:
        date = date + datetime.timedelta(days=-1)
    notify_date_time = str(date) + ' ' + data.get_alarm_time_display()

    # Date match check
    if current_date_time == notify_date_time:
        push_data_info['line_id'] = bytes(data.binary_lineid)
        push_data_info['garbage_type'] = data.get_garbage_type_display()
        push_data_info['today_flg'] = data.alarm_day
        push_data_list.append(push_data_info)

    return push_data_list

    
def db_roop():
    """db_roop()

        A function that gets the DB value at 10-second intervals and 
        pushes line when the notification time matches.
        
    """
    
    print('Start checking the value of the database.')
    sent_date_time  = ''
    get_date = clsGetDate.GetDate()
    while True:
        start = time.time()
        queryset = Garbageday.objects.all()
        push_data_list = []
        today = datetime.datetime.now()
        current_date_time = str(today)[0:16]
        month = today.month
        year = today.year
        
        for data in queryset:
            #If the alarm is ON, check the DB value in a loop
            if data.manage_alarm:
                push_data_info = {'line_id': None, 'garbage_type': None, 'today_flg': 0}

                #When the value of week1 is weekly
                if data.week1 == 0:
                    every_week=[1,2,3,4,5]
                    for week1 in every_week:
                        # Get DB registration date as datetime type
                        date = get_date.get_date_of_nth_dow(year, month, week1, data.day_of_week1)
                        if date != None:
                            # If the notification time and the current time match, get  the push_data_list
                            push_data_list = check_append_data(data, date, push_data_list, push_data_info, current_date_time)
                        #When there is a value in day_of_week2
                        if data.day_of_week2 != None:
                            date2 = get_date.get_date_of_nth_dow(year, month, week1, data.day_of_week2)
                            if date2 != None:
                                push_data_list = check_append_data(data, date2, push_data_list, push_data_info, current_date_time)

                # When week1 is not weekly    
                else:   
                    date3 = get_date.get_date_of_nth_dow(year, month, data.week1, data.day_of_week1)
                    if date3 != None:
                        push_data_list = check_append_data(data, date3, push_data_list, push_data_info, current_date_time)

                    # When there is a value in day_of_week2
                    if data.day_of_week2 != None:
                        date4 = get_date.get_date_of_nth_dow(year, month, data.week1, data.day_of_week2)
                        if date4 != None:
                            push_data_list = check_append_data(data, date4, push_data_list, push_data_info, current_date_time)

                    # When there is a value in week2
                    if data.week2 != None:
                        date5 = get_date.get_date_of_nth_dow(year, month, data.week2, data.day_of_week1)
                        if date5 != None:
                            push_data_list = check_append_data(data, date5, push_data_list, push_data_info, current_date_time)

        # When there is a value in push_data_list
        if push_data_list != [] and sent_date_time != current_date_time:
            sent_date_time = line_push(push_data_list)

        elapsed_time = time.time() - start
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        time.sleep(10)