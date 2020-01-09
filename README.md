# Async Standup

This tool helps you write, publish, and keep track of your async standup reports.

The standup data will be saved and manipulated in YAML files, and published to Slack in Markdown format.

## Setup

You will need [Python 3.6+](https://www.python.org/downloads/) and [Poetry](https://github.com/python-poetry/poetry) installed. Then clone this repo and run:

```sh
poetry install
poetry run standup bootstrap
```

## Usage

* `standup --help`: Display general usage help.
* `standup bootstrap`: Create the basic project configuration.
* `standup copy`: Copy yesterday/today's standup file for the next day.
* `standup publish`: Publish your update on the right Slack channel.
