from pathlib import Path

class Database:
    def __init__(self, db_from_fp, date):
        self.db_fp = str(db_from_fp)
        self.date_downloaded = date.strftime('%Y-%m-%d')
        self.seq_len = self.parse_fasta(self.db_fp)
        #self.copy_db(db_from_fp, dest)

    def get_db_path(self):
        print("DB path is {0}".format(self.db_fp))

    def get_date(self):
        print("Date is {0}".format(self.date_downloaded))

    def print_headers_n_lengths(self):
        print("Sequence lengths are {0}".format(self.seq_len))

     #copy db to a location
 #   def copy_db(self, db_from_fp, dest):
        #also change the timestamps?
 #       shutil.copy2(db_from_fp, dest)
 #       shutil.copy2(meta_from_fp, dest)


    # Copied and modified from okfasta
    def parse_fasta(self, s):
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
        with Path(s).open() as f:
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