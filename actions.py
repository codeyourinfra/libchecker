#!/usr/bin/python3.6

import json
import logging
import requests
import smtplib
from email.message import EmailMessage
from config import Config


class WebhookPost():
    """
    Class responsible for posting a JSON payload to a webhook.
    """


    def __init__(self, **parameters):
        """
        The class requires the webhook URL.
        """

        self.__webhook_url = Config.get_value(parameters, "webhook_url")


    def execute(self, platform, library_name, current_info, latest_info):
        """
        Makes a POST request to the webhook.
        """

        payload = {"platform": platform,
                   "library_name": library_name,
                   "current_info": current_info,
                   "latest_info": latest_info}
        try:
            response = requests.post(self.__webhook_url, json=payload)
            if response.status_code == 200:
                logging.info("Success on posting the JSON payload to the webhook.")
            else:
                logging.warning("Failure on posting the JSON payload to the webhook. "
                                "Status code: %s. Webhook response: %s",
                                response.status_code, response.text)
            result = response.text
        except requests.exceptions.ConnectionError:
            logging.exception("Error on posting the JSON payload to the webhook. Stack trace:")
            result = None
        return result


class SlackWebhookPost():
    """
    Class responsible for posting a message to a Slack incoming webhook.
    """


    def __init__(self, **parameters):
        """
        The class requires the Slack incoming webhook URL.
        """

        self.__slack_webhook_url = Config.get_value(parameters, "slack_webhook_url")


    def execute(self, platform, library_name, current_info, latest_info):
        """
        Makes a POST request to the webhook.
        """

        new_version = current_info["latest_release_number"]
        message_text = "New *%s* version released in *%s*: *%s* !!!" % (library_name,
                                                                        platform,
                                                                        new_version)
        message = {"text": message_text}
        try:
            response = requests.post(self.__slack_webhook_url, json=message)
            if response.status_code == 200:
                logging.info("Success on posting the message to Slack.")
            else:
                logging.warning("Failure on posting the message to Slack. "
                                "Status code: %s. Slack response: %s",
                                response.status_code, response.text)
            result = response.text
        except requests.exceptions.ConnectionError:
            logging.exception("Error on posting the message to Slack. Stack trace:")
            result = None
        return result


class TravisCIBuildTrigger():
    """
    Class responsible for triggering a build in Travis CI.
    """


    def __init__(self, **parameters):
        """
        The class requires the Travis API token and the repository API endpoint.
        """

        self.__travis_api_token = Config.get_value(parameters, "travis_api_token")
        self.__repo_api_endpoint = Config.get_value(parameters, "repo_api_endpoint")


    def execute(self, platform, library_name, current_info, latest_info):
        """
        Makes a POST request to the endpoint.
        """

        new_version = current_info["latest_release_number"]
        build_message = "New %s version released in %s: %s !!!" % (library_name,
                                                                   platform,
                                                                   new_version)
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
            response = requests.post(self.__repo_api_endpoint,
                                     data=json.dumps(body),
                                     headers=headers)
            if response.status_code == 202:
                logging.info("Success on triggering the build in Travis CI.")
            else:
                logging.warning("Failure on triggering the build in Travis CI. "
                                "Status code: %s. Travis CI response: %s",
                                response.status_code, response.text)
            result = response.text
        except requests.exceptions.ConnectionError:
            logging.exception("Error on triggering the build in Travis CI. Stack trace:")
            result = None
        return result


class EmailSend():
    """
    Class responsible for sending an email.
    """


    def __init__(self, **parameters):
        """
        The class requires SMTP credential settings.
        """

        self.__smtp_host = Config.get_value(parameters, "smtp_host")
        self.__smtp_port = Config.get_value(parameters, "smtp_port")
        self.__smtp_username = Config.get_value(parameters, "smtp_username")
        self.__smtp_password = Config.get_value(parameters, "smtp_password")
        self.__sender = Config.get_value(parameters, "sender")
        self.__receivers = parameters.get("receivers", None)


    def execute(self, platform, library_name, current_info, latest_info):
        """
        Sends the email.
        """

        new_version = current_info["latest_release_number"]
        message = "New %s version released in %s: %s !!!" % (library_name,
                                                             platform,
                                                             new_version)
        msg = EmailMessage()
        msg["Subject"] = "libchecker release monitor notification"
        msg["From"] = self.__sender
        msg["To"] = self.__receivers
        msg.set_content(message)

        server = smtplib.SMTP_SSL(self.__smtp_host, self.__smtp_port)
        server.login(self.__smtp_username, self.__smtp_password)
        server.send_message(msg)
        server.quit()
