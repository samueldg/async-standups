import configparser
import os
import stat
import time
from datetime import datetime
from datetime import timedelta
from enum import IntEnum
from pathlib import Path

import click
import jinja2
import yaml
from slack_sdk import WebClient


CONFIG_FILE = "config.ini"
STANDUP_TEMPLATE_FILE = "standup.md.j2"
CONFIG_TEMPLATE_FILE = "config.ini.j2"

TODAY_TIME_STRUCT = time.localtime()
TODAY = datetime(*TODAY_TIME_STRUCT[:3])  # Keep only year, month and day

DATA_FOLDER = "data"
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


TEMPLATE_LOADER = jinja2.PackageLoader(package_name="standup")
TEMPLATE_ENV = jinja2.Environment(loader=TEMPLATE_LOADER)
STANDUP_TEMPLATE = TEMPLATE_ENV.get_template(STANDUP_TEMPLATE_FILE)
CONFIG_TEMPLATE = TEMPLATE_ENV.get_template(CONFIG_TEMPLATE_FILE)


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


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
    return Path(DATA_FOLDER, year_folder, month_folder, standup_filename)


def generate_new_standup_data(from_date, to_date, interactive=False):
    input_standup_path = get_standup_file_path(from_date)
    output_standup_path = get_standup_file_path(to_date)
    config = read_config()

    with open(input_standup_path) as input_data_file:

        output_data = yaml.safe_load(input_data_file)

        for channel, standup_data in output_data.items():
            standup_data["yesterday"] = standup_data["today"]
            standup_data["today"] = [{"action": "TODO", "projects": []}]

    month_directory = output_standup_path.parent
    month_directory.mkdir(parents=True, exist_ok=True)

    with open(output_standup_path, "x") as output_data_file:
        yaml.dump(
            output_data,
            output_data_file,
            default_flow_style=None,
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
    """Publish the standup data to the appropriate Slack channel.

    The message will be formatted as a markdown code block.
    """
    standup_data_file_path = get_standup_file_path(TODAY)

    with open(standup_data_file_path) as standup_data_file:
        standup_data = yaml.safe_load(standup_data_file)

    for channel, standup_data in standup_data.items():
        rendered_text = get_formatted_standup(standup_data)

        if dry_run:
            print(f"#{channel}\n{rendered_text}")
        else:
            config = read_config()
            slack = WebClient(token=config["slack"]["api_token"])
            slack.chat_postMessage(channel=channel, text=rendered_text, as_user=True)


@cli.command()
def bootstrap():
    """Create the basic project setup and configuration.

    This will:
      - Create the scaffolding for data files.
      - Create a config file to store your Slack API token.
    """
    click.echo(
        "You will be redirected to the Slack docs page to get a token.",
        color="green",
    )
    click.echo(
        "Please sign in and copy the legacy API token to your clipboard.",
        color="green",
    )
    click.pause("Press any key to open a new browser tab to get your token...")
    click.launch("https://api.slack.com/custom-integrations/legacy-tokens")
    token = click.prompt("Copy your Slack token here, then press <enter>")
    config = CONFIG_TEMPLATE.render(token=token)
    with open(CONFIG_FILE, "x") as config_file:
        config_file.write(config)
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)


if __name__ == "__main__":
    cli()
