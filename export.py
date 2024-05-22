import cfg
import tempfile
import csv


def get_file() -> str:
    """
    Dumps the contents of the bills table into a csv-formatted string.
    :return str: a string containing the contents of the bills table.
    """
    with cfg.Cursor() as cur:
        cur.execute('select * from bills')

        # csv.writer requires a file-like object, so we create a temporary file to hold the csv data
        with tempfile.TemporaryFile(mode='w+') as file:
            writer = csv.writer(file)

            # Grab the names of the bill table columns to use as headers
            writer.writerow([i[0] for i in cur.description])
            for i in cur.fetchall():
                writer.writerow(i)

            # Reset the file cursor to the beginning of the file so we can read the whole thing
            file.seek(0)
            return file.read()
