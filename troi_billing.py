#!/usr/bin/env python3
import os
import sys
from datetime import datetime

import click
import click_completion
import pandas as pd
import yaml
from troi.troi_api.api import Client
from troi.troi_api.hours import add_billing_entry, update_billing_entry, get_billing_hours
from troi.troi_api.projects import get_all_positions

# Initialize click_completion for bash
click_completion.init()

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "troi_billing", "config.yaml")
DEFAULT_CLIENT_ID = 3
DEFAULT_DATE_FORMAT = "%Y-%m-%d"


def load_config():
    with open(CONFIG_FILE, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg['credentials']


def get_client(credentials):
    return Client(credentials['url'], credentials['username'], credentials['api_token'])


def current_date():
    return datetime.now().strftime(DEFAULT_DATE_FORMAT)


def _get_terminal_size():
    try:
        terminal_width, terminal_height = os.get_terminal_size()
    except OSError:
        return None
    return terminal_width, terminal_height


def _display_output(output):
    if sys.stdout.isatty():
        click.echo_via_pager(output)
    else:
        print(output)


def format_dataframe(df: pd.DataFrame):
    if df.empty:
        click.echo("No data found.")
        return

    terminal_size = _get_terminal_size()
    if terminal_size is None:
        print(df.to_string(index=False))
        return

    terminal_width, _ = terminal_size
    column_width = max(df.apply(lambda x: x.astype(str).map(len).max())) + 2
    if df.shape[1] * column_width > terminal_width:
        for col_width in range(terminal_width, 30, -5):
            pd.set_option('display.max_colwidth', col_width)
            if len(df.to_string(index=False).split('\n')[0]) <= terminal_width:
                _display_output(df.to_string(index=False))
                return
        _display_output(df.to_string(index=False))
    else:
        _display_output(df.to_string(index=False))


@click.group()
def cli():
    pass


@cli.command()
def install_completion():
    """Install bash completion for this CLI."""
    click.echo('Installing bash completion...')
    click_completion.install()
    click.echo('Bash completion installed. Please reload your shell or run `source ~/.bashrc`.')


@cli.command()
def all_positions():
    """Get all positions."""
    credentials = load_config()
    client = get_client(credentials)
    positions_df = get_all_positions(client)
    format_dataframe(positions_df)


@cli.command()
@click.argument('project_id', type=int)
@click.argument('date_from', type=click.DateTime(formats=[DEFAULT_DATE_FORMAT]), default=current_date, required=False)
@click.option('--date_to', type=click.DateTime(formats=[DEFAULT_DATE_FORMAT]), default=None,
              help="End date for billing hours")
@click.option('--client_id', type=int, default=DEFAULT_CLIENT_ID, help="Client ID (default is 3)")
@click.option('--user_id', type=int, default=None, help="User ID")
@click.option('--position_id', type=int, default=None, help="Position ID")
def billing_hours(project_id, date_from, date_to, client_id, user_id, position_id):
    """Get billing hours."""
    credentials = load_config()
    client = get_client(credentials)
    billing_hours_df = get_billing_hours(client, project_id, date_from, date_to, client_id, user_id, position_id)
    format_dataframe(billing_hours_df)


@cli.command()
@click.argument('hours', type=float)
@click.argument('tags', nargs=-1, type=str)
@click.option('-d', '--date_from', type=click.DateTime(formats=[DEFAULT_DATE_FORMAT]), default=current_date,
              required=False, help="Start date for billing hours")
@click.option('-t', '--task_id', type=int, help="Task ID")
@click.option('-u', '--user_id', type=int, help="User ID")
@click.option('-c', '--client_id', type=int, help="Client ID")
@click.option('-m', '--remark', type=str, help="Annotation remark")
def add_entry(date_from, hours, tags, task_id, user_id, client_id, remark):
    """Add a billing entry."""
    credentials = load_config()
    task_id = task_id or credentials.get('task_id')
    user_id = user_id or credentials.get('user_id')
    client_id = client_id or credentials.get('client_id', DEFAULT_CLIENT_ID)
    if task_id is None or user_id is None:
        click.echo("Error: Task ID and User ID must be provided.")
        raise click.Abort()

    billing_date = date_from.date() if date_from is not None else current_date()
    client = get_client(credentials)

    try:
        add_billing_entry(client, task_id, billing_date, hours, user_id, tags, remark, client_id)
    except Exception as e:
        click.echo(f"Error: {e}")
    else:
        click.echo("Billing entry added successfully.")


@cli.command()
@click.argument('record_id', type=int)
@click.argument('hours', type=float)
@click.argument('tags', nargs=-1, type=str)
@click.option('-d', '--date_from', type=click.DateTime(formats=[DEFAULT_DATE_FORMAT]), default=current_date,
              required=False, help="Start date for billing hours")
@click.option('-t', '--task_id', type=int, help="Task ID")
@click.option('-u', '--user_id', type=int, help="User ID")
@click.option('-c', '--client_id', type=int, help="Client ID")
@click.option('-m', '--remark', type=str, help="Annotation remark")
def update_entry(date_from, hours, tags, task_id, user_id, client_id, record_id, remark):
    """Update a billing entry."""
    credentials = load_config()
    task_id = task_id or credentials.get('task_id')
    user_id = user_id or credentials.get('user_id')
    client_id = client_id or credentials.get('client_id', DEFAULT_CLIENT_ID)
    if task_id is None or user_id is None or record_id is None:
        click.echo("Error: Task ID, User ID, and Record ID must be provided.")
        raise click.Abort()

    billing_date = date_from.date() if date_from is not None else current_date()
    client = get_client(credentials)

    try:
        update_billing_entry(client, task_id, billing_date, hours, user_id, record_id, tags, annotation=remark)
    except Exception as e:
        click.echo(f"Error: {e}")
    else:
        click.echo("Billing entry updated successfully.")


if __name__ == '__main__':
    cli(prog_name="troi-billing")
