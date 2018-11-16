#!/usr/bin/python3.6

import logging
import requests
from config import Config


class WebhookPost():
    """
    Class responsible for posting a JSON payload to a webhook.
    """


    def __init__(self, **parameters):
        self.__logger = logging.getLogger("libchecker")
        self.__webhook_url = Config.get_value(parameters, "webhook_url")
        self.__logger.debug("WebhookPost initialized.")


    def execute(self, platform, library_name, current_info, latest_info):
        payload = {"platform": platform,
                   "library_name": library_name,
                   "current_info": current_info,
                   "latest_info": latest_info}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.__webhook_url, data=payload, headers=headers)
            if response.status_code == 200:
                self.__logger.info("Success on posting the JSON payload to the webhook.")
            else:
                self.__logger.warn("Failure on posting the JSON payload to the webhook. Status code: %s.", response.status_code)
        except requests.exceptions.ConnectionError:
            self.__logger.exception("Error on posting the JSON payload to the webhook. Stack trace:")


class SlackWebhookPost():
    """
    Class responsible for posting a message to a Slack incoming webhook.
    """


    def __init__(self, **parameters):
        self.__logger = logging.getLogger("libchecker")
        self.__slack_webhook_url = Config.get_value(parameters, "slack_webhook_url")
        self.__logger.debug("SlackWebhookPost initialized.")


    def execute(self, platform, library_name, current_info, latest_info):
        message_text = "New *%s* version released in *%s*: *%s* !!!" % (library_name,
                                                                        platform,
                                                                        current_info["latest_release_number"])
        message = {"text": message_text}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.__slack_webhook_url, data=message, headers=headers)
            if response.status_code == 200:
                self.__logger.info("Success on posting the message to Slack.")
            else:
                self.__logger.warn("Failure on posting the message to Slack. Status code: %s. Slack response: %s", response.status_code, response.text)
        except requests.exceptions.ConnectionError:
            self.__logger.exception("Error on posting the message to Slack. Stack trace:")


class TravisCIBuildTrigger():
    """
    Class responsible for triggering a build in Travis CI.
    """


    def __init__(self, **parameters):
        self.__logger = logging.getLogger("libchecker")
        self.__travis_api_token = Config.get_value(parameters, "travis_api_token")
        self.__repo_api_endpoint = Config.get_value(parameters, "repo_api_endpoint")
        self.__logger.debug("TravisCIBuildTrigger initialized.")


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
            response = requests.post(self.__repo_api_endpoint, data=body, headers=headers)
            if response.status_code == 200:
                self.__logger.info("Success on triggering the build in Travis CI.")
            else:
                self.__logger.warn("Failure on triggering the build in Travis CI. Status code: %s. Travis CI response: %s", response.status_code, response.text)
        except requests.exceptions.ConnectionError:
            self.__logger.exception("Error on triggering the build in Travis CI. Stack trace:")
