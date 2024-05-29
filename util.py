import cfg
import tempfile
import csv
import enum
import os
tempdir = './frontend/billorganizer_frontend/bill_app/static/tmp/'
os.makedirs(os.path.dirname(tempdir), exist_ok=True)
tempfile.tempdir = tempdir


# Operations allowed when processing queries
class Ops(enum.Enum):
    EQUAL = "="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="


class Join(enum.Enum):
    AND = "&"
    OR = "|"


class Pars(enum.Enum):
    BEGIN = "("
    END = ")"


# Build a list of columns in the database to use when parsing queries
with cfg.Cursor(dictionary=True) as cur:
    desc: dict[str, str] = {}

    cur.execute(f'select * from bills limit 0')
    for i in cur.description:
        desc[i[0]] = 'bills'

    for table in ['sponsors', 'lists', 'marks', 'notes']:
        cur.execute(f'select * from {table} limit 0')
        for i in cur.description:
            desc[f'{table}.{i[0]}'] = table




def export(list_id: str, query = None, query_vars = tuple()) -> str:
    """
    Dumps the contents of the bills table into a csv-formatted file, and returns the file name.
    :param list_id: the uuid of the list to export. if NONE, export all bills.
    :return str: The name of the file.
    """
    with cfg.Cursor() as cur:
        if query == None:
            if list_id is None:
                cur.execute(r"""
                    select * from bills
                        join sponsors on bills.biennium = sponsors.biennium and bills.sponsor_id = sponsors.id
                """)
            else:
                cur.execute(r"""
                    select * from marks 
                        join bills on marks.biennium = bills.biennium and marks.bill_id = bills.bill_id 
                        join sponsors on bills.biennium = sponsors.biennium and bills.sponsor_id = sponsors.id 
                        where marks.list = '?'
                """, tuple(list_id))
        else:
            cur.execute(query,data=query_vars)

        # csv.writer requires a file-like object, so we create a temporary file to hold the csv data
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as file:

            writer = csv.writer(file)

            # Grab the names of the bill table columns to use as headers
            writer.writerow([i[0] for i in cur.description])
            for i in cur.fetchall():
                writer.writerow(i)

            return file.name


def search(query: str, author: int = None, dictionary: bool = True) -> list[tuple | dict]:
    stack = []
    # Parse the query line into a list of actions
    clr = lambda: stack.append(int(buf) if buf.isdigit() else buf)
    buf = ''
    i = 0
    while i < len(query) and i != -1:
        char = query[i]
        buf = buf.strip()  # Trim any excess spaces

        match char:

            case ' ':  # Ignore spaces
                i += 1
                continue

            case '\'' | '"':  # If the current character is a " or ', assume it's raw and skip processing until we hit the same character again
                pos = query.find(char, i + 1)
                if pos == -1:
                    raise UserWarning(f"string not terminated - could not find ending {char}")
                else:  # If there is a terminating character, push the whole segment between the terminators to the stack and jump to after the last terminator
                    stack.append(buf + query[i:pos])
                    i = pos + 1
                    buf = ''
                    continue

            case '<' | '>':  # Handle greter/less than ops
                if buf:
                    clr()
                    buf = ''

                if i + 1 < len(query) and query[i + 1] == '=':  # Check if next character is an equal sign. If it is, we need to bump I to the next char and add the = when running char through Ops
                    stack.append(Ops(char + '='))
                    i += 1  # Increment I by one to skip the equals
                else:
                    stack.append(Ops(char))

            case '&' | '|':
                if buf:
                    clr()
                    buf = ''
                stack.append(Join(char))

            case '=':
                if buf:
                    clr()
                    buf = ''
                stack.append(Ops(char))

            case '(' | ')':
                if buf:
                    clr()
                    buf = ''
                stack.append(Pars(char))

            case _:  # default case
                buf += char

        i += 1

    if buf:
        clr()

    # Compose the list of actions into a sql statement

    statement = 'select * from bills '  # the select and from part of the statement, including joins
    where = 'where ( '  # the where part of the statement
    i = 0
    tables = ['bills']  # What tables are already in the statement
    args = []  # Arguments to be passed to the database
    par_count = 0  # Used to track how many parenthesis deep we are so we know if any are unterminated

    def inc(err: str | None = 'Encountered unexpected end of query'):
        nonlocal i, item
        i += 1
        if i >= len(stack):
            if err is None: return
            raise UserWarning(err)
        item = stack[i]

    while i < len(stack):
        item = stack[i]

        while item == Pars.BEGIN:  # Handle any beginning parentheses
            par_count += 1
            where += '( '
            inc('Unterminated "("')

        if isinstance(item, Ops):  # If first item is an operator, error out
            raise UserWarning(f'Cannot use a "{item.value}" here')

        if item not in desc:  # Check if the column exists in the database
            raise UserWarning(f'"{item}" is not a valid column')

        table = desc[item]  # Get the table the column belongs to

        if table not in tables:  # If this table isn't already in the query, join it w/ bills
            tables.append(table)
            match table:
                case 'sponsors':
                    statement += 'join sponsors on bills.biennium = sponsors.biennium and bills.sponsor_id = sponsors.id '
                case 'marks' | 'lists':
                    statement += 'join marks on bills.biennium = marks.biennium and bills.bill_id = marks.bill_id join lists on marks.list = lists.id '
                case 'notes':
                    statement += 'join notes on bills.biennium = notes.biennium and bills.bill_id = notes.bill_id '
                case _:
                    raise UserWarning(f'"{table}" is not a valid table')

        where += f'bills.{item} ' if table == 'bills' else f'{item} '
        inc(f'Query unfinished')

        if not isinstance(item, Ops):
            raise UserWarning(f'"{item}" is not a valid operatiion')

        where += f'{item.value} '
        inc(f'Query unfinished')

        if isinstance(item, Ops | Pars | Join):
            raise UserWarning(f'"{item}" - operations are not allowed here')

        where += "? "
        args.append(item)

        inc(None)
        if isinstance(item, Join):
            where += f' {"and" if item is item.AND else "or"} '
            inc(None)

    where += ') '  # Close off the where

    for i in ['lists', 'notes']:
        if i in tables:
            if author is None:
                raise UserWarning(f'You are not logged in, and cannot access list, note, or mark data')
            where += f'and {i}.author = {author}'

    statement += where

    with cfg.Cursor(dictionary=dictionary) as cur:
        try:
            cur.execute(statement, tuple(args))
            return cur.fetchall()
        except Exception as e:
            raise UserWarning(f'Could not properly parse query.')
