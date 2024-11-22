# Async Standup

This tool helps you write, publish, and keep track of your async standup reports.

The standup data will be saved and manipulated in YAML files, and published to Slack in Markdown format.

## Setup

You will need [Python 3.9+](https://www.python.org/downloads/) and [uv](https://docs.astral.sh/uv) installed.

Then clone this repo and run:

```sh
uv sync
uv run standup bootstrap
```

## Usage

* `standup --help`: Display general usage help.
* `standup bootstrap`: Create the basic project configuration.
* `standup copy`: Copy yesterday/today's standup file for the next day.
* `standup publish`: Publish your update on the right Slack channel.

### Slack App Configuration

In order to publish your updates to Slack, you will need to:

1. Create a Slack app.
1. Add the `chat:write` scope to the app's _User Token Scopes_.
1. Install the app to your workspace.
1. Authorize your user with the app.
1. Add the app to the channel where you want to post.

Once these steps are complete, go through `standup bootstrap` and you'll be prompted for the token and channel ID.
