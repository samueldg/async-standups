import time
from datetime import datetime
from datetime import timedelta
from enum import IntEnum
from textwrap import dedent

import click
import yaml
from slack_sdk import WebClient

from .config import CONFIG_FILE
from .config import DATA_DIR
from .config import read_config
from .config import write_config
from .templating import STANDUP_TEMPLATE

TODAY_TIME_STRUCT = time.localtime()
TODAY = datetime(*TODAY_TIME_STRUCT[:3])  # Keep only year, month and day

YEAR_FOLDER_FORMAT = r"%Y"  # e.g. '2018'
MONTH_FOLDER_FORMAT = r"%m - %B"  # e.g. '06 - June'
STANDUP_FILENAME_FORMAT = r"%Y-%m-%d.yml"  # e.g. '2018-01-09.yml'


WeekDays = IntEnum(
    "WeekDays",
    "MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY",
    start=0,
)

DAYS_OFF = {
    WeekDays.SATURDAY,
    WeekDays.SUNDAY,
}


def get_formatted_standup(data):
    """From the data dictionary, get the markdown-formatted standup"""
    return STANDUP_TEMPLATE.render(sections=data)


def get_previous_work_day(date):
    previous_day = date - timedelta(days=1)
    while previous_day.weekday() in DAYS_OFF:
        previous_day = previous_day - timedelta(days=1)
    return previous_day


def get_next_work_day(date):
    next_day = date + timedelta(days=1)
    while next_day.weekday() in DAYS_OFF:
        next_day = next_day + timedelta(days=1)
    return next_day


def get_standup_file_path(date):
    year_folder = date.strftime(YEAR_FOLDER_FORMAT)
    month_folder = date.strftime(MONTH_FOLDER_FORMAT)
    standup_filename = date.strftime(STANDUP_FILENAME_FORMAT)
    return DATA_DIR / year_folder / month_folder / standup_filename


def generate_new_standup_data(from_date, to_date, interactive=False):
    input_standup_path = get_standup_file_path(from_date)
    output_standup_path = get_standup_file_path(to_date)
    config = read_config()

    with open(input_standup_path) as input_data_file:
        output_data = yaml.safe_load(input_data_file)

    output_data["yesterday"] = output_data["today"]
    output_data["today"] = ["TODO"]

    month_directory = output_standup_path.parent
    month_directory.mkdir(parents=True, exist_ok=True)

    with open(output_standup_path, "x") as output_data_file:
        yaml.dump(
            output_data,
            output_data_file,
            default_flow_style=False,
            width=120,
            allow_unicode=True,
        )

    editor = config.get("editor", "path", fallback=None)
    if interactive:
        click.edit(
            filename=str(output_standup_path),
            extension=".yml",
            editor=editor,
            require_save=True,
        )


cli = click.Group()


@cli.command()
@click.option("--edit", "-e", is_flag=True, default=False)
def copy(edit):
    """Create the standup file data for today or tomorrow.

    If the data file for today exists, one will be created for tomorrow.
    Otherwise, yesterday's file will be used to create today's.
    """
    if not get_standup_file_path(TODAY).exists():
        from_date = get_previous_work_day(TODAY)
        to_date = TODAY
    else:
        from_date = TODAY
        to_date = get_next_work_day(TODAY)

    generate_new_standup_data(
        from_date,
        to_date,
        interactive=edit,
    )


@cli.command()
@click.option("--dry-run", "-n", is_flag=True, default=False)
def publish(dry_run):
    """Publish the standup data to the configured Slack channel.

    The message will be formatted as a markdown code block.
    """
    config = read_config()
    channel = config["slack"]["channel"]

    standup_data_file_path = get_standup_file_path(TODAY)

    with open(standup_data_file_path) as standup_data_file:
        standup_data = yaml.safe_load(standup_data_file)

    rendered_text = get_formatted_standup(standup_data)

    if dry_run:
        click.echo(f"#{channel}\n{rendered_text}")
    else:
        slack = WebClient(token=config["slack"]["api_token"])
        slack.chat_postMessage(
            channel=channel,
            text=rendered_text,
        )


@cli.command()
def bootstrap():
    """Create the basic project setup and configuration.

    This will:
      - Create the scaffolding for data files. (TODO)
      - Create a file to store your Slack token and configuration.
    """
    # Get the User OAuth Token from Slack
    click.echo(
        dedent(
            """\
            You will be redirected to Slack's app management.
            Please select the app that will post your standups.
            The app will need the chat:write permission.

            Get the token from:

              OAuth & Permissions > User OAuth Token.
            """
        )
    )
    click.pause("Press any key to open a new browser tab to get your token...")
    click.launch("https://api.slack.com/apps")

    token = click.prompt("\nEnter your User OAuth Token")
    channel = click.prompt("Enter the Channel ID where you'll post updates")

    # Render the config file
    write_config(token=token, channel=channel)

    # Indicate successful completion
    click.secho(
        "All set!",
        fg="green",
    )
    click.echo(
        f"Please review your config: {CONFIG_FILE}",
    )


if __name__ == "__main__":
    cli()
