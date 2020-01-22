# libchecker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Docker Build status](https://img.shields.io/docker/build/codeyourinfra/libchecker.svg)](https://hub.docker.com/r/codeyourinfra/libchecker/builds) [![Docker Pulls](https://img.shields.io/docker/pulls/codeyourinfra/libchecker.svg)](https://hub.docker.com/r/codeyourinfra/libchecker)

Checks the update of a library's version and executes some actions if so.

## How it works

![How it works](http://codeyourinfra.today/wp-content/uploads/2018/11/libchecker-1.png)

**libchecker** gets the current library data from the [Libraries.io API](http://libraries.io/api) every minute. Then, compares the current version with the latest one, previously stored in a [MongoDB](https://www.mongodb.com) instance. If a new version of the library have just released, **libchecker** automaticaly execute one or more configured actions.

## Supported actions

It's a work in progress. Please contribute with the project adding more actions. At this moment the supported actions are:

- WebhookPost - Posts a JSON payload to a [webhook](https://en.wikipedia.org/wiki/Webhook)
- SlackWebhookPost - [Posts a message to a Slack incoming webhook](https://api.slack.com/incoming-webhooks)
- TravisCIBuildTrigger - [Triggers a build in Travis CI](https://docs.travis-ci.com/user/triggering-builds)
- GithubIssueCreate - [Creates an issue in a GitHub repository](https://developer.github.com/v3/issues/#create-an-issue)
- EmailSend - Sends an email to one or more recipients

Each action is implemented by a Python class of the [actions](actions.py) module.

## Configuration

**libchecker** requires a configuration file. Take a look at the content of [config.yaml](config.yaml):

```yaml
---
- librariesio_api_key: env.LIBRARIESIO_API_KEY
  libraries_platform: pypi
  library_name: ansible
  mongodb:
    uri: env.MONGO_URI
    username: env.MONGO_USERNAME
    password: env.MONGO_PASSWORD
  actions:
    - classname: SlackWebhookPost
      parameters:
        slack_webhook_url: env.SLACK_WEBHOOK_URL
    - classname: TravisCIBuildTrigger
      parameters:
        travis_api_token: env.TRAVIS_API_TOKEN
        repo_api_endpoint: https://api.travis-ci.org/repo/codeyourinfra%2Fdocker/requests
    - classname: TravisCIBuildTrigger
      parameters:
        travis_api_token: env.TRAVIS_API_TOKEN
        repo_api_endpoint: https://api.travis-ci.org/repo/codeyourinfra%2Fjava8/requests

- librariesio_api_key: env.LIBRARIESIO_API_KEY
  libraries_platform: maven
  library_name: com.fasterxml.jackson.core:jackson-core
  mongodb:
    uri: env.MONGO_URI
    username: env.MONGO_USERNAME
    password: env.MONGO_PASSWORD
  actions:
    - classname: EmailSend
      parameters:
        smtp_host: env.SMTP_HOST
        smtp_port: 587
        smtp_username: env.SMTP_USERNAME
        smtp_password: env.SMTP_PASSWORD
        sender: gustavo@codeyourinfra.today
        receivers:
          - gustavo@esign.com.br
    - classname: GithubIssueCreate
      parameters:
        github_api_token: env.GITHUB_API_TOKEN
        username: esign-consulting
        reponame: google-geocode
```

In this example, **libchecker** is configured to check new releases of [Ansible](https://www.ansible.com) in [PyPI](https://pypi.org). The [Libraries.io API](http://libraries.io/api) requires a key, which is defined in the environment variable *LIBRARIESIO_API_KEY*.

For sensitive data, you may prefer environment variables. If it's the case, start the value of the parameter with *env.*, and **libchecker** will get the configuration from the environment variable specified right after.

Based on this configuration, **libchecker** will execute 3 actions, if a new version of [Ansible](https://www.ansible.com) is released in [PyPI](https://pypi.org):

1. A message will be sent to a [Slack](https://slack.com) channel, through a POST request to a [Slack incoming webhook](https://api.slack.com/incoming-webhooks);
2. A build will be triggered in [Travis CI](https://travis-ci.org), through a POST request to the [Travis CI API v3](https://docs.travis-ci.com/user/developer/#api-v3);
3. Another build will be triggered in [Travis CI](https://travis-ci.org), the same way.

## Slack workspace

Join the **libchecker** workspace on Slack by clicking [here](https://join.slack.com/t/libchecker/shared_invite/enQtNDgxNTA1MDY4MDgwLWM0OWIxYTVhOTY5YWQ5YjdhMzY1MmRjMzlkZTQ4OGMzY2UyZDVjZTMzMDJkNzg3M2RiYjBjYTA3ZTk5YjI4YWM). There we can talk more about the project.

If you would like to be notified about your favorite library releases, feel free to request a channel with that purpose. The goal is keep everyone up to date when any library is released :)
