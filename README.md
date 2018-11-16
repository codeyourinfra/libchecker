# libchecker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Docker Build status](https://img.shields.io/docker/build/codeyourinfra/libchecker.svg)](https://hub.docker.com/r/codeyourinfra/libchecker/builds) [![Docker Pulls](https://img.shields.io/docker/pulls/codeyourinfra/libchecker.svg)](https://hub.docker.com/r/codeyourinfra/libchecker)

Checks the update of a library's version and executes some actions if so.

## How it works

![How it works](http://codeyourinfra.today/wp-content/uploads/2018/11/libchecker.png)

**libchecker** gets the current library data from the [Libraries.io API](http://libraries.io/api) every minute. Then, compares the current version with the latest one, previously stored in a [MongoDB](https://www.mongodb.com) instance. If a new version of the library have just released, **libchecker** automaticaly execute one or more configured actions.

## Supported actions

It's a work in progress. Please contribute with the project adding more actions. At this moment the supported actions are:

- WebhookPost - Posts a JSON payload to a [webhook](https://en.wikipedia.org/wiki/Webhook)
- SlackWebhookPost - [Posts a message to a Slack incoming webhook](https://api.slack.com/incoming-webhooks)
- TravisCIBuildTrigger - [Triggers a build in Travis CI](https://docs.travis-ci.com/user/triggering-builds)

## Configuration

**libchecker** requires a configuration file. Take a look at the content of [config.json](config.json):

```json
{
    "librariesio_api_key": "env.LIBRARIESIO_API_KEY",
    "libraries_platform": "pypi",
    "library_name": "ansible",
    "mongodb": {
        "uri": "mongodb://mongo/",
        "username": "dbuser",
        "password": "dbpassword"
    },
    "actions": [{
        "classname": "SlackWebhookPost",
        "parameters": {
            "slack_webhook_url": "env.SLACK_WEBHOOK_URL"
        }
    }, {
        "classname": "TravisCIBuildTrigger",
        "parameters": {
            "travis_api_token": "env.TRAVIS_API_TOKEN",
            "repo_api_endpoint": "https://api.travis-ci.org/repo/codeyourinfra%2Fdocker/requests"
        }
    }, {
        "classname": "TravisCIBuildTrigger",
        "parameters": {
            "travis_api_token": "env.TRAVIS_API_TOKEN",
            "repo_api_endpoint": "https://api.travis-ci.org/repo/codeyourinfra%2Foracle_java8/requests"
        }
    }]
}
```

In this example, **libchecker** is configured to check new releases of [Ansible](https://www.ansible.com) in [PyPI](https://pypi.org). The [Libraries.io API](http://libraries.io/api) requires a key, which is defined in the environment variable *LIBRARIESIO_API_KEY*.

For sensitive data, you may prefer environment variables. If it's the case, start the value of the parameter with *env.*, and **libchecker** will get the configuration from the environment variable specified right after.
