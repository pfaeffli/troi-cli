# Troi CLI Tool

This CLI tool helps manage billing entries and retrieve project positions from the Troi service. Below are the available
commands and their usage:

## Installation

Ensure you have Python 3.x installed. Install necessary packages:

```sh
pip install click click-completion PyYAML pandas
```

## Configuration

Create a `config.yaml` file in the same directory as your script with the following content:

```yaml
credentials:
  url: "https://api.troi.example.com"
  username: "your_username"
  api_token: "your_api_token"
  task_id: 123  # default value (optional)
  user_id: 456  # default value (optional)
  client_id: 3  # default value (optional)
```

## Usage

### Get All Positions

Retrieve all project positions:

```sh
./troi_cli.py all_positions
```

### Get Billing Hours

Retrieve billing hours for a specific project and date range:

```sh
./troi_cli.py billing_hours <project_id> [<date_from>]
                      [--date_to <date_to>]
                      [--client_id <client_id>]
                      [--user_id <user_id>]
                      [--position_id <position_id>]
```

#### Arguments:

- `<project_id>`: ID of the project (required).
- `<date_from>`: Start date for billing hours in `YYYY-MM-DD` format (optional, default is today's date).

#### Options:

- `--date_to`: End date for billing hours in `YYYY-MM-DD` format (optional).
- `--client_id`: ID of the client (optional, default is `3`).
- `--user_id`: ID of the user (optional).
- `--position_id`: ID of the position (optional).

### Update Billing Entry

Update a billing entry:

```sh
./troi_cli.py update_entry <record_id> <hours> <tags>...
                      [-d <date_from>]
                      [-t <task_id>]
                      [-u <user_id>]
                      [-c <client_id>]
                      [-m <remark>]
```

#### Arguments:

- `<record_id>`: ID of the record to update (required).
- `<hours>`: Number of hours billed (required).
- `<tags>`: List of tags associated with the entry (required).

#### Options:

- `-d, --date_from`: Start date for billing hours in `YYYY-MM-DD` format (optional, default is today's date).
- `-t, --task_id`: ID of the task (optional, will use default value from `config.yaml` if not provided).
- `-u, --user_id`: ID of the user (optional, will use default value from `config.yaml` if not provided).
- `-c, --client_id`: ID of the client (optional, default is `3`).
- `-m, --remark`: Annotation remark (optional).

### Example

```sh
# Get all positions
./troi_cli.py all_positions

# Get billing hours
./troi_cli.py billing_hours 101 --date_from 2023-01-01 --date_to 2023-01-31

# Update a billing entry
./troi_cli.py update_entry 1 3.5 development -d 2023-01-01 -t 1001 -u 2002 -c 3001 -m "Finished development task"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.