"""middleware custom_logging.py
    * Used for log output 
"""

import logging
import threading
from package import clsGetLineInfo, clsOperateLineId
import json


local = threading.local()


class CustomAttrMiddleware:
    """CustomAttrMiddleware"""
    
    def __init__(self, get_response):
        """__init__()

            __init__ function

        """
    
        self.get_response = get_response

    def __call__(self, request):
        """__call__()

        Get the username of the request when requesting from the client
        Temporarily saved in threading.local ()

            Args:
                self : instance
                request : request

            Returns:
                eturns the line login request

        """

        if 'json' in request.headers.get('content-type'):
            request_json = json.loads(request.body.decode('utf-8'))
            events = request_json['events']
            if events[0]['type'] != 'unfollow':
                get_line_info = clsGetLineInfo.GetLineInfo()
                profile = get_line_info.line_bot_api.get_profile(events[0]['source']['userId'])
                request.user.username = profile.display_name
            else:
                from line.models import LineUserName
                operate_lineid = clsOperateLineId.OperateLineId()
                lineUserName = LineUserName.objects.get(line=operate_lineid.encrypt(events[0]['source']['userId']))
                request.user.username = lineUserName.display_name

        elif 'name' in request.session:
            request.user.username = request.session['name']
        else:
            pass

        if request.user:
            setattr(local, 'user', request.user.username)
        else:
            setattr(local, 'user', None)

        response = self.get_response(request)

        # Clear at the time of response
        setattr(local, 'user', None)

        return response

class CustomAttrFilter(logging.Filter):
    """CustomAttrFilter"""
    def filter(self, record):
        """filter()"""
        record.user = getattr(local, 'user', None)
        return True