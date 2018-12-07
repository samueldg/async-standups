# Async Standup

This tool helps you write, publish, and keep track of your async standup reports.

## Setup

You will need [Python 3.7](https://www.python.org/downloads/) and [Pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today) installed. Then clone this repo and run:

```sh
pipenv install
```

In order to post your status to Slack, you will need to [get a Slack API token](https://api.slack.com/custom-integrations/legacy-tokens), and create a `config.ini` file like so:

```ini
[slack]

api_token = MY_SLACK_API_TOKEN
```

Since this file will contain a token to act on Slack on your behalf, you should make sure only you have access to it:

```sh
chmod 600 config.ini
```

## Usage

* `python standup.py copy`: Copy yesterday/today's standup file for the next day.
* `python standup.py publish`: Publish your update on the right Slack channel.
