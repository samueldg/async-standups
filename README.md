# Async Standup

This tool helps you write, publish, and keep track of your async standup reports.

The standup data will be saved and manipulated in YAML files, and published to Slack in Markdown format.

## Setup

You will need [Python 3.7](https://www.python.org/downloads/) and [Pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today) installed. Then clone this repo and run:

```sh
pipenv install
pipenv run standup bootstrap
```

## Usage

* `standup --help`: Display general usage help.
* `standup bootstrap`: Create the basic project configuration.
* `standup copy`: Copy yesterday/today's standup file for the next day.
* `standup publish`: Publish your update on the right Slack channel.
