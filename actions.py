#!/usr/bin/python3.6

import requests


class WebhookPost():
    """
    Class responsible for posting a JSON payload to a webhook.
    """


    def __init__(self, webhook_url):
        self.__webhook_url = webhook_url


    def execute(self, platform, library_name, latest_info, current_info):
        payload = {"platform": platform,
                   "library_name": library_name,
                   "latest_info": latest_info,
                   "current_info": current_info}
        requests.post(self.__webhook_url, data=payload)
