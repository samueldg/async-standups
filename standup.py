import configparser
import time
from datetime import datetime
from datetime import timedelta
from enum import IntEnum
from pathlib import Path

import click
import jinja2
import yaml
from slackclient import SlackClient


CONFIG_FILE = 'config.ini'
TEMPLATE_FILE = 'template.md.j2'

TODAY_TIME_STRUCT = time.localtime()
TODAY = datetime(*TODAY_TIME_STRUCT[:3])  # Keep only year, month and day

DATA_FOLDER = 'data'
YEAR_FOLDER_FORMAT = r'%Y'  # e.g. '2018'
MONTH_FOLDER_FORMAT = r'%m - %B'  # e.g. '06 - June'
STANDUP_FILENAME_FORMAT = r'%Y-%m-%d.yml'  # e.g. '2018-01-09.yml'


WeekDays = IntEnum(
    'WeekDays',
    'MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY',
    start=0,
)

DAYS_OFF = {
    WeekDays.SATURDAY,
    WeekDays.SUNDAY,
}


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def get_formatted_standup(data):
    """From the data dictionary, get the markdown-formatted standup"""
    template_loader = jinja2.FileSystemLoader(searchpath='.')
    template_env = jinja2.Environment(
        loader=template_loader,
    )
    template = template_env.get_template(TEMPLATE_FILE)
    return template.render(sections=data)


def get_previous_work_day(date):
    previous_day = date - timedelta(days=1)
    while previous_day.weekday() in DAYS_OFF:
        previous_day = date - timedelta(days=1)
    return previous_day


def get_standup_file_path(date):
    year_folder = date.strftime(YEAR_FOLDER_FORMAT)
    month_folder = date.strftime(MONTH_FOLDER_FORMAT)
    standup_filename = date.strftime(STANDUP_FILENAME_FORMAT)
    return Path(DATA_FOLDER, year_folder, month_folder, standup_filename)


def generate_new_standup_data(from_date, to_date):
    input_standup_path = get_standup_file_path(from_date)
    output_standup_path = get_standup_file_path(to_date)

    with open(input_standup_path) as input_data_file:

        output_data = yaml.safe_load(input_data_file)

        for channel, standup_data in output_data.items():
            standup_data['yesterday'] = standup_data['today']
            standup_data['today'] = [{
                'action': 'TODO',
                'projects': [],
            }]

    with open(output_standup_path, 'x') as output_data_file:
        yaml.dump(output_data, output_data_file)


cli = click.Group()


@cli.command()
def copy():
    """Create the standup file data for today (if nonexistent)
    or tomorrow (otherwise).
    """
    if not get_standup_file_path(TODAY).exists():
        from_date = TODAY - timedelta(days=1)  # Yesterday
        to_date = TODAY
    else:
        from_date = TODAY
        to_date = TODAY + timedelta(days=1)  # Tomorrow

    generate_new_standup_data(from_date, to_date)


@cli.command()
@click.option('--dry-run', '-n', is_flag=True, default=False)
def send(dry_run):
    config = read_config()
    slack = SlackClient(config['slack']['api_token'])

    standup_data_file_path = get_standup_file_path(TODAY)

    with open(standup_data_file_path) as standup_data_file:
        standup_data = yaml.safe_load(standup_data_file)

    for channel, standup_data in standup_data.items():
        rendered_text = get_formatted_standup(standup_data)

        if dry_run:
            print(f'#{channel}\n{rendered_text}')
        else:
            slack.api_call(
                'chat.postMessage',
                channel=channel,
                text=rendered_text,
                as_user=True
            )


if __name__ == '__main__':
    cli()
