#!/usr/bin/env python3
from datetime import datetime, date

import click
import click_completion
import os
import pandas as pd
import yaml
from time_tracking_synchronisation.troi_api.projects import get_all_positions
from time_tracking_synchronisation.troi_api.hours import get_billing_hours
from time_tracking_synchronisation.troi_api.api import Client
# Initialize click_completion for bash
click_completion.init()

def load_config():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg['credentials']


import sys


def format_dataframe(df: pd.DataFrame):
    """Pretty print pandas DataFrame."""
    if df.empty:
        click.echo("No data found.")
        return
    try:
        term_width, term_height = os.get_terminal_size()
    except OSError:
        print(df.to_string(index=False))
        return

    avg_col_width = max(df.apply(lambda x: x.astype(str).map(len).max())) + 2  # calculate average column width
    if df.shape[1] * avg_col_width > term_width:
        max_width = term_width
        for col_width in range(max_width, 30, -5):  # reduce width to fit in terminal, down to 30 characters
            pd.set_option('display.max_colwidth', col_width)
            output = df.to_string(index=False)
            if len(output.split('\n')[0]) <= term_width:
                if sys.stdout.isatty():
                    click.echo_via_pager(output)  # use pager to enable scrolling if terminal
                else:
                    print(output)
                break
        else:
            if sys.stdout.isatty():
                click.echo_via_pager(df.to_string(index=False))
            else:
                print(df.to_string(index=False))
    else:
        if sys.stdout.isatty():
            click.echo_via_pager(df.to_string(index=False))
        else:
            print(df.to_string(index=False))


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


if __name__ == '__main__':
    cli()

