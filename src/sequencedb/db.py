from pathlib import Path

class Database:
    def __init__(self, db_from_fp, date_created):
        self.db_fp = str(db_from_fp)
        self.date_created = date_created

    def get_db_path(self):
        print("DB path is {0}".format(self.db_fp))

    def get_dates(self):
        print("Date created is {0}\nDate modified is {1}".format(self.date_created, self.date_modified))

    # Copied and modified from okfasta
    def get_lengths(self):
        """Parse a FASTA format file.
        Parameters
        ----------
        f : File object or iterator returning lines in FASTA format.
        Returns
        -------
        An iterator of tuples containing two strings
            First string is the sequence description, second is the
            sequence.
        """
        headers_count = 0
        headers_dict = {}
        with Path(self.db_fp).open() as f:
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    desc = line[1:]
                    headers_dict[desc] = 0
                    headers_count += 1
                else:
                    headers_dict[desc] += len(line)
        if len(headers_dict) < headers_count:
            #how should entries be treated? Throwing error at the moment. Can possibly just rename the description
            raise Exception('There are duplicates in the FASTA file')
        return headers_dict