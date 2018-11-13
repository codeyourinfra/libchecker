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


class SlackWebhookPost():
    """
    Class responsible for posting a message to a Slack incoming webhook.
    """


    def __init__(self, slack_webhook_url):
        self.__slack_webhook_url = slack_webhook_url


    def execute(self, platform, library_name, latest_info, current_info):
        message_text = "New *%s* version released in *%s*: *%s* !!!" % (library_name,
                                                                        platform,
                                                                        current_info["latest_release_number"])
        message = {"text": message_text}
        requests.post(self.__slack_webhook_url, data=message)
