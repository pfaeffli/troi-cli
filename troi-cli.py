#!/usr/bin/env python3
from datetime import datetime

import click_completion
import yaml

from time_tracking_synchronisation.troi_api.api import Client
from time_tracking_synchronisation.troi_api.hours import add_billing_entry
from time_tracking_synchronisation.troi_api.hours import get_billing_hours
from time_tracking_synchronisation.troi_api.projects import get_all_positions

# Initialize click_completion for bash
click_completion.init()


def load_config():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg['credentials']


import pandas as pd
import os
import sys
import click


def _get_terminal_size():
    """Retrieve the terminal size or return default size on error."""
    try:
        terminal_width, terminal_height = os.get_terminal_size()
    except OSError:
        return None
    return terminal_width, terminal_height


def _display_output(output: str):
    """Display the DataFrame output with proper handling for terminal and non-terminal environments."""
    if sys.stdout.isatty():
        click.echo_via_pager(output)
    print(output)



def format_dataframe(df: pd.DataFrame):
    """Pretty print pandas DataFrame."""
    if df.empty:
        click.echo("No data found.")
        return

    terminal_size = _get_terminal_size()
    if terminal_size is None:
        print(df.to_string(index=False))
        return

    terminal_width, _ = terminal_size
    column_width = max(df.apply(lambda x: x.astype(str).map(len).max())) + 2  # calculate maximum column width

    if df.shape[1] * column_width > terminal_width:
        for col_width in range(terminal_width, 30, -5):  # reduce width to fit in terminal, down to 30 characters
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
def all_positions():
    """Get all positions."""
    credentials = load_config()
    client = Client(credentials['url'], credentials['username'], credentials['api_token'])
    positions_df = get_all_positions(client)
    format_dataframe(positions_df)


@cli.command()
@click.argument('project_id', type=int)
@click.argument('date_from', type=click.DateTime(), default=lambda: datetime.now(), required=False)
@click.option('--date_to', type=click.DateTime(), default=None, help="End date for billing hours")
@click.option('--client_id', type=int, default=3, help="Client ID (default is 3)")
@click.option('--user_id', type=int, default=None, help="User ID")
@click.option('--position_id', type=int, default=None, help="Position ID")
def billing_hours(project_id, date_from, date_to, client_id, user_id, position_id):
    """Get billing hours."""
    credentials = load_config()
    client = Client(credentials['url'], credentials['username'], credentials['api_token'])
    billing_hours_df = get_billing_hours(
        client=client,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to,
        client_id=client_id,
        user_id=user_id,
        position_id=position_id,
    )
    format_dataframe(billing_hours_df)


@cli.command()
@click.argument('hours', type=float)
@click.argument('tags', nargs=-1, type=str)
@click.option('-d', '--date_from', type=click.DateTime(), default=lambda: datetime.now(), required=False,
              help="Start date for billing hours")
@click.option('-t', '--task_id', type=int, help="Task ID")
@click.option('-u', '--user_id', type=int, help="User ID")
@click.option('-c', '--client_id', type=int, help="Client ID")
@click.option('-m', '--remark', type=str, help="Annotation remark")
def add_entry(date_from, hours, tags, task_id, user_id, client_id, remark):
    """Add a billing entry."""
    credentials = load_config()

    # Use default values from config if not provided
    task_id = task_id or credentials.get('task_id')
    user_id = user_id or credentials.get('user_id')
    client_id = client_id or credentials.get('client_id', 3)

    # Parse date
    if date_from is None:
        billing_date = datetime.now()
    else:
        billing_date = date_from.date()

    client = Client(credentials['url'], credentials['username'], credentials['api_token'])

    try:
        add_billing_entry(
            client=client,
            date=billing_date,
            hours=hours,
            tags=tags,
            task_id=task_id,
            user_id=user_id,
            client_id=client_id,
            annotation=remark)
    except Exception as e:
        click.echo(f"Error: {e}")
    else:
        click.echo("Billing entry added successfully.")


if __name__ == '__main__':
    cli()
