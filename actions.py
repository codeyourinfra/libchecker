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

class TravisCIBuildTrigger():
    """
    Class responsible for triggering a build in Travis CI.
    """


    def __init__(self, travis_api_token, repo_api_endpoint):
        self.__travis_api_token = travis_api_token
        self.__repo_api_endpoint = repo_api_endpoint


    def execute(self, platform, library_name, latest_info, current_info):
        build_message = "New *%s* version released in *%s*: *%s* !!!" % (library_name,
                                                                         platform,
                                                                         current_info["latest_release_number"])
        body = {"request": {
            "message": build_message,
            "branch": "master"
        }}
        headers = {
            "Travis-API-Version": "3",
            "Authorization": "token %s" % self.__travis_api_token
        }
        requests.post(self.__repo_api_endpoint, data=body, headers=headers)