import cfg
import tempfile
import csv


def export(list_id: str) -> str:
    """
    Dumps the contents of the bills table into a csv-formatted file, and returns the file name.
    :param list_id: the uuid of the list to export. if NONE, export all bills.
    :return str: The name of the file.
    """
    with cfg.Cursor() as cur:
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

        # csv.writer requires a file-like object, so we create a temporary file to hold the csv data
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, delete_on_close=False) as file:
            writer = csv.writer(file)

            # Grab the names of the bill table columns to use as headers
            writer.writerow([i[0] for i in cur.description])
            for i in cur.fetchall():
                writer.writerow(i)

            return file.name
