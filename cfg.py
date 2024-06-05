"""
initializes various bits and sets up needed variables
:var str base_url: The url that the program will be accessed from (e.g. https://example.com/).
    Can be localhost and/or include a port (e.g. http://example.com:8080/).
    Must have a trailing slash and a scheme (either http or https).
:var mariadb.Connection conn: The connection to the database. Note that, unless necessary, this should NOT be used
    to create a cursor. Instead, use the already created cursor 'cur'.
:var mariadb.Cursor cur: The cursor that is used to execute sql statements on the database.
    remember to commit with conn after executing statements.
"""

from pathlib import Path
from typing import Any
import os
import re
import logging

import mariadb
import yaml

# Figure out where config files are
if 'BILL_ORGANIZER_HOME' in os.environ:  # If user set a homedir for us via env, use it
    cfg_dir = Path(os.environ.get('BILL_ORGANIZER_HOME'))
elif 'XDG_CONFIG_HOME' in os.environ:  # Use xdg spec if not
    cfg_dir = Path(os.environ.get('XDG_CONFIG_HOME'), 'bill-organizer')
elif 'LOCALAPPDATA' in os.environ:  # For Windows compatability
    cfg_dir = Path(os.environ.get('LOCALAPPDATA'), 'bill-organizer')
else:  # Fallback to .config in the user's homedir
    cfg_dir = Path('~', '.config', 'bill-organizer').expanduser()

# Main configuration file
cfg_file: Path = Path(cfg_dir, 'cfg.yml')

# Safely open and read the file as yaml
if not cfg_file.is_file():
    raise FileNotFoundError(f'main configuration file not found: "{cfg_file}"')
try:
    with open(cfg_file, 'r') as file:
        cfg_data: dict = yaml.safe_load(file)
except Exception as e:
    e.add_note(f'could not read config file "{cfg_file.absolute()}" correctly')
    raise e

# Error out if the config file is not a dict (.e.g the file was formatted as a list instead)
if not isinstance(cfg_data, dict):
    raise TypeError(f'config file "{cfg_file.absolute()}" is not formatted correctly')

debug_vals = []


def fetch_var(var_name: str, throw: bool=True, default: Any=None):
    """
    Fetches the value of a config key from the environment variables if set, otherwise the config file.
    :param var_name: The value associated with the config key. For environment variables, will have 'BILL_ORGANIZER_'
        prepended and converted to uppercase.
    :param throw: Whether to throw an exception if a key is not found. Defaults to True.
    :param default: If throw is False, tha value to return if a key is not found.
    :return: The value of the config key if found or default if not.
    """
    if (val := os.environ.get(f'BILL_ORGANIZER_{var_name}'.upper())) is not None:  # Use env variable if it exists
        debug_vals.append(f'loaded "{var_name}" from environment variable with value "{val}"')
        return val
    if (val := cfg_data.get(var_name)) is not None:  # Else grab from config file
        debug_vals.append(f'loaded "{var_name}" from config file "{cfg_file}" with value "{val}"')
        return val
    if not throw:
        debug_vals.append(f'could not find "{var_name}" in config file or environment variables, using default "{default}"')
        return default
    raise KeyError(f'variable "{var_name}" not found in config file or environment variables')


# Load all the needed variables
db_user: str = fetch_var('db_user')
db_password: str = fetch_var('db_password')
db_host: str = fetch_var('db_host')
db_port: int = fetch_var('db_port')
db_database: str = fetch_var('db_database')
create_db: bool = fetch_var('create_db')
program_name: str = fetch_var('name')
log_level: str = fetch_var('log_level', False, 'debug')
log_format: str | list = fetch_var('log_format', False, '%(asctime)s: %(module)s (%(levelname)s) - %(message)s')
log_file: str = fetch_var('log_file', False)
init_time: int = fetch_var('init_time', False, 365)
wait_time: int = fetch_var('wait_time', False, 7)
recheck_delay: int = fetch_var('recheck_delay', False, 10)

# If log_file is a list, convert it to a path.
if isinstance(log_file, list):
    log_file: Path = Path(log_file)

log = logging.getLogger()
if log_file:
    logging.basicConfig(level=getattr(logging, log_level.upper()), format=log_format, filename=log_file)
else:
    logging.basicConfig(level=getattr(logging, log_level.upper()), format=log_format)

log.debug(f'configuration directory set to "{cfg_dir}"')
for i in debug_vals:
    log.debug(i)
log.info('initialized variables')
log.info('Connecting to database')

# Connect to the database
try:
    pool: mariadb.ConnectionPool = mariadb.ConnectionPool(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_database,
        pool_name='main',
        pool_size=20,
        autocommit=True
    )
except mariadb.Error as e:
    raise e.add_note('Could not connect to db - is the database accessible, and the information in cfg.yaml correct?')


class Cursor:
    """
    Creates a cursor object. __ONLY__ use with a with statement. When used w/ a with statement, guarantees no race
    conditions with other connections.
    """
    dictionary: bool
    pool: mariadb.ConnectionPool = pool
    conn: mariadb.Connection

    def __init__(self, dictionary: bool = False):
        """

        :param dictionary: Set to true to have the cursor return dictionary objects with column names as keys
        instead of returning tuples.
        """
        self.dictionary = dictionary

    def __enter__(self) -> mariadb.Cursor:
        self.conn = self.pool.get_connection()
        return self.conn.cursor(dictionary=self.dictionary)

    def __exit__(self, _, __, ___):
        self.conn.close()


log.info('verifying database configuration')

with Cursor() as cur:
    cur.execute("show tables")
    # Determine if any tables are missing
    required_tables = ['bills', 'lists', 'marks', 'notes']
    found_tables = [i[0] for i in cur]
    missing_tables = [i for i in required_tables if i not in found_tables]
    if missing_tables:
        if cfg_data['create_db']:  # Create db from sql file if create_db is true
            with open(Path('create-db.sql'), 'r') as file:
                # cur.execute() only supports one sql statement at a time, so we need to split the file into an array.
                # We use strip() to get rid of tailing newlines that cause entries to appear in the list consisting of
                # only a newline.
                for _i in file.read().strip().split(';'):
                    if not _i: continue  # skip any empty entries in the list
                    cur.execute(_i)
        else:  # Else just error out
            raise Exception(f'Missing tables in database: "{", ".join(missing_tables)}"')



# Cleanup
del cfg_data, cfg_file, missing_tables, required_tables, found_tables, cur, pool, fetch_var, file, log_file, log_level, log_format, debug_vals

log.info('configuration complete, entering main loop')
