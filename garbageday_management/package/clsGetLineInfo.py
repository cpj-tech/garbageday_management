"""package clsGetLineInfo.py
    * Class get Line Information
"""
from linebot import LineBotApi
import json
class GetLineInfo(object):
    """GetLineInfo"""
    
    def __init__(self):
        self._line_channel_id = None
        self._line_channel_secret = None
        self._redirect_url = None
        self._line_bot_api = None
        self._getSettingValue()

    
    @property
    def line_channel_id(self):
        return self._line_channel_id
    @property
    def line_channel_secret(self):
        return self._line_channel_secret
    @property
    def redirect_url(self):
        return self._redirect_url
    @property
    def line_bot_api(self):
        return self._line_bot_api

    def _getSettingValue(self):
        file = open('./settings/info_settings.json', 'r')
        info = json.load(file)

        self._line_bot_api = LineBotApi(
            info['CHANNEL_ACCESS_TOKEN']
            )

        self._line_channel_id = info['LINE_CHANNEL_ID']
        self._line_channel_secret = info['LINE_CHANNEL_SECRET']
        self._redirect_url = info['REDIRECT_URL']
    
    