#!/usr/bin/python3.6

import json
import logging
import requests
from config import Config


class WebhookPost():
    """
    Class responsible for posting a JSON payload to a webhook.
    """


    def __init__(self, **parameters):
        self.__webhook_url = Config.get_value(parameters, "webhook_url")


    def execute(self, platform, library_name, current_info, latest_info):
        payload = {"platform": platform,
                   "library_name": library_name,
                   "current_info": current_info,
                   "latest_info": latest_info}
        try:
            response = requests.post(self.__webhook_url, json=payload)
            if response.status_code == 200:
                logging.info("Success on posting the JSON payload to the webhook.")
            else:
                logging.warn("Failure on posting the JSON payload to the webhook. Status code: %s.", response.status_code)
        except requests.exceptions.ConnectionError:
            logging.exception("Error on posting the JSON payload to the webhook. Stack trace:")


class SlackWebhookPost():
    """
    Class responsible for posting a message to a Slack incoming webhook.
    """


    def __init__(self, **parameters):
        self.__slack_webhook_url = Config.get_value(parameters, "slack_webhook_url")


    def execute(self, platform, library_name, current_info, latest_info):
        message_text = "New *%s* version released in *%s*: *%s* !!!" % (library_name,
                                                                        platform,
                                                                        current_info["latest_release_number"])
        message = {"text": message_text}
        try:
            response = requests.post(self.__slack_webhook_url, json=message)
            if response.status_code == 200:
                logging.info("Success on posting the message to Slack.")
            else:
                logging.warn("Failure on posting the message to Slack. Status code: %s. Slack response: %s", response.status_code, response.text)
        except requests.exceptions.ConnectionError:
            logging.exception("Error on posting the message to Slack. Stack trace:")


class TravisCIBuildTrigger():
    """
    Class responsible for triggering a build in Travis CI.
    """


    def __init__(self, **parameters):
        self.__travis_api_token = Config.get_value(parameters, "travis_api_token")
        self.__repo_api_endpoint = Config.get_value(parameters, "repo_api_endpoint")


    def execute(self, platform, library_name, current_info, latest_info):
        build_message = "New %s version released in %s: %s !!!" % (library_name,
                                                                   platform,
                                                                   current_info["latest_release_number"])
        body = {"request": {
            "message": build_message,
            "branch": "master"
        }}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Travis-API-Version": "3",
            "Authorization": "token %s" % self.__travis_api_token
        }
        try:
            response = requests.post(self.__repo_api_endpoint, data=json.dumps(body), headers=headers)
            if response.status_code == 202:
                logging.info("Success on triggering the build in Travis CI.")
            else:
                logging.warn("Failure on triggering the build in Travis CI. Status code: %s. Travis CI response: %s", response.status_code, response.text)
        except requests.exceptions.ConnectionError:
            logging.exception("Error on triggering the build in Travis CI. Stack trace:")
