# Bill Organizer

## Project summary

Bill Organizer is a Python 3 program that pulls data from the Washington State Legislature and shows it in a convenient, easy to understand format that allows tracking, writing notes, and receiving notifications on bill updates.

## Functionality

- View an up to date list of bills
- Create lists of bills to keep yourself organized
- Filter and sort bills using a wide range of options
- Write notes that will be attached to bills
- Get notifications for meetings on selected bills

## Installation

### Prerequisites

<!-- - Docker

- Docker Compose --> <!-- - Any web browser -->
- A preconfigured MariaDB instance
- python 3.10+

### Installation Steps

1. `git clone https://github.com/CSCD488-Winter2024/bill-organizer`
2. `cd bill organizer`
3. Install required files by running: `./codespace-setup-commands.sh` (for ubuntu)
4. Create the credentials used to connect to your database with:
5. Configure the software (see the Configuration section.)

<!-- 5. populate your database with users stuff? by calling `python manage.py ???` //todo -->
5. run the server by calling `python manage.py runserver`

<!-- 3. `echo "DB_STORAGE_DIR: /put/storage/directory/here" > .env`
3. `docker compose up -d`
4. Open `http://localhost:53982` in your web browser. -->

### Configuration

Configuration can be done via either environment variables or a configuration file.

- When using environment variables, the variable name should be formatted as `BILL_ORGANIZER_VARNAME`. Variable names should always be all caps.
- When using a config file, the config file should be named `cfg.yml`, formatted as a `YAML` file, and placed in the config directory. Variable names should always be all lowercase. The config directory is determined via environment variables using the following logic: 
  - `$BILL_ORGANIZER_HOME` if `BILL_ORGANIZER_HOME` is set.
  - Otherwise, `$XDG_CONFIG_HOME/bill-organizer` if `XDG_CONFIG_HOME` is set.
  - Otherwise, `$LOCALAPPDATA/bill-organizer` if `LOCALAPPDATA` is set.
  - Otherwise, `$HOME/.config/bill-organizer`.

The following config varaibles are required:

- `db_user: str`: The username of the sql user you are running the program as
- `db_password: str`: The password of the sql user you are running the program as
- `db_database: str`: Your database name - the sql user you are running the program as must have full read/write access to the database.>
- `db_host: str`: The URL the database can be reached at
- `db_port: int`: The port the database can be reached at
- `name: str`: The name of the program. Should be customized to something unique to you, as this is used to prevent rate limiting by uniquely identifying each instance.

The following config variables are optional:

- `create_db: bool`: If `True`, the software will attempt to create any missing tables in the database. If `False`, the program will raise an exception if any tables are missing. Defaults to `False`.
- `log_level: str`: How detailed to make the logs. Can be `debug`, `info`, `warning`, or `error`. Defaults to `info`.
- `log_format: str`: Format string describing the format of log messages. see [Python docs](https://docs.python.org/3/library/logging.html#logrecord-attributes) for more info. Defaults to `%(asctime)s: %(module)s (%(levelname)s) - %(message)s`
- `log_file: str | list[str]`: When set, logs will be written to the file specified by this variable. Can be a string or a list of path elements. When not set, log info will be printed to stdout.
- `init_time: int`: How far back to go to fetch data on bills if a handler has no bills in the database, in days. Defaults to `365` days.
- `wait_time: int`: How long to wait before starting a handler again, in days. Effectively sets the minimum time until an update can take place, as `recheck_delay` and server uptime both have effects on when handlers will actually start. Defaults to `7` days. **MUST** be less than `init_time`.
- `recheck_delay: int`: How many seconds to wait before checking all handlers. Any handlers that need updates will have updates started.

## Known Problems

This project is in the very early stages of development and very few features are implemented yet.

## Contributing

Bill Organizer is a modular program - new information sources can be added easily. In Bill Organizer, every source of data is called a *handler*. New handlers (e.g. a handler for the Oregon State Legislature) can be contributed by anyone. To create, for example, a handler for the Oregon State Legislature:

1. Fork the repository
2. Create a new branch: `git checkout -b oregon-handler`
3. Create a new `.py` file in the `handlers` folder named after your handler: `oregon_leg.py`
4. In `oregon.py`, import `handler` and create a class that inherits `handler.Handler`
5. Implement `mod.Module`. If you want to create additional files, you can create a folder that shares the same name as your python file (e.g `oregon.py` and `oregon/additional_file.py`) in the `handler` if necessary.
6. In `oregon.py`, instantiate and register your handler: `handler.handlers.append(Oregon())`
7. Commit and submit your pull request

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License Version 3 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License Version 3 for more details.

A copy of the GNU General Public License Version 3 is provided in this repository as the file `LICENSE` - see this file for more details. If `LICENSE` is not available, see [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.html#license-text).