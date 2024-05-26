import cfg
import tempfile
import csv


async def get_file(list_id: str) -> str:
    """
    Dumps the contents of the bills table into a csv-formatted file, and returns the file name.
    :param list_id: the uuid of the list to export. if NONE, export all bills.
    :return str: The name of the file.
    """
    with cfg.Cursor() as cur:
        if list_id is None:
            cur.execute('SELECT * FROM bills')
        else:
            cur.execute('select bills.* from marks join bills on marks.bill_id = bills.bill_id where marks.list = ?', list_id)

        # csv.writer requires a file-like object, so we create a temporary file to hold the csv data
        with tempfile.TemporaryFile(mode='w+', delete=False, delete_on_close=False) as file:
            writer = csv.writer(file)

            # Grab the names of the bill table columns to use as headers
            writer.writerow([i[0] for i in cur.description])
            for i in cur.fetchall():
                writer.writerow(i)

            return file.name
