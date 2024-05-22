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
import os
import re

import mariadb
import yaml

# Figure out where config files are
if 'BILL_ORGANIZER_HOME' in os.environ:  # If user set a homedir for us via env, use it
    _cfg_dir = Path(os.environ.get('BILL_ORGANIZER_HOME'))
elif 'XDG_CONFIG_HOME' in os.environ:  # Use xdg spec if not
    _cfg_dir = Path(os.environ.get('XDG_CONFIG_HOME'), 'bill-organizer')
elif 'LOCALAPPDATA' in os.environ:  # For Windows compatability
    _cfg_dir = Path(os.environ.get('LOCALAPPDATA'), 'bill-organizer')
else:  # Fallback to .config in the user's homedir
    _cfg_dir = Path('~', '.config', 'bill-organizer').expanduser()

# Main configuration file
_cfg_file: Path = Path(_cfg_dir, 'cfg.yml')

# Safely open and read the file as yaml
if not _cfg_file.is_file():
    raise FileNotFoundError(f'main configuration file not found: "{_cfg_file}"')
try:
    with open(_cfg_file, 'r') as _file:
        _cfg_data: dict = yaml.safe_load(_file)
except Exception as e:
    e.add_note(f'could not read config file "{_cfg_file.absolute()}" correctly')
    raise e

# Error out if the config file is not a dict (.e.g the file was formatted as a list instead)
if not isinstance(_cfg_data, dict):
    raise TypeError(f'config file "{_cfg_file.absolute()}" is not formatted correctly')


# Load all the needed variables
try:
    base_url: str = _cfg_data['base_url']
    db_user: str = _cfg_data['db_user']
    db_password: str = _cfg_data['db_password']
    db_host: str = _cfg_data['db_host']
    db_port: int = _cfg_data['db_port']
    db_database: str = _cfg_data['db_database']
    create_db: bool = _cfg_data['create_db']
except Exception as e:
    raise KeyError(f'Encountered exception {e} while loading from config file "{_cfg_file.absolute()}" - ')


if not re.match(r'^https?://.+/$', base_url):
    raise ValueError(f'base_url "{base_url}" is not formatted correctly '
                     f'- does is begin with "http://" or "https://", and end with a "/"?')

# Connect to the database
try:
    _pool: mariadb.ConnectionPool = mariadb.ConnectionPool(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_database,
        pool_name='main',
        pool_size=20,
    )
except mariadb.Error as e:
    raise e.add_note('Could not connect to db - is the database accessible, and the information in cfg.yaml correct?')


class Cursor():
    """
    Creates a cursor object. __ONLY__ use with a with statement. When used w/ a with statement, guarantees no race
    conditions with other connections.
    """
    dictionary: bool
    pool: mariadb.ConnectionPool = _pool
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


with Cursor() as _cur:
    _cur.execute("show tables")
    # Determine if any tables are missing
    _required_tables = ['bills', 'lists', 'marks', 'notes']
    _found_tables = [i[0] for i in _cur]
    _missing_tables = [i for i in _required_tables if i not in _found_tables]
    if _missing_tables:
        if _cfg_data['create_db']:  # Create db from sql file if create_db is true
            with open(Path('create-db.sql'), 'r') as _file:
                # cur.execute() only supports one sql statement at a time, so we need to split the file into an array.
                # We use strip() to get rid of tailing newlines that cause entries to appear in the list consisting of
                # only a newline.
                for _i in _file.read().strip().split(';'):
                    if not _i: continue  # skip any empty entries in the list
                    _cur.execute(_i)
        else:  # Else just error out
            raise Exception(f'Missing tables in database: "{", ".join(_missing_tables)}"')


# Cleanup
del _cfg_data, _cfg_file, _cfg_dir, _missing_tables, _required_tables, _found_tables, _cur, _i, _pool
