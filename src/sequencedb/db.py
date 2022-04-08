from pathlib import Path
import hashlib

class Database:
    def __init__(self, dbname, db_filepath, date_modified):
        self.db_name = str(dbname)
        self.db_fp = str(db_filepath)
        self.date_modified = date_modified
        #set file_hash only when parse_fasta is called
        self.file_hash = hashlib.md5()

    #Read fasta and return a dictionary and md5sum
    def parse_fasta(self):
        headers_count = 0
        headers_dict = {}
        with Path(self.db_fp).open() as f:
            for line in f:
                #update md5sum for each line
                self.file_hash.update(line.encode('UTF-8'))
                line = line.strip()
                if line.startswith(">"):
                    desc = line[1:]
                    headers_dict[desc] = 0
                    headers_count += 1
                else:
                    #throw error if first line does not start with ">"
                    if headers_count == 0:
                        raise Exception('The first line of your FASTA file does not being with ">"')
                    headers_dict[desc] += len(line)
        if len(headers_dict) < headers_count:
            #Throw an error if there is a duplicate entry
            raise Exception('There are duplicates in the FASTA file')
        return headers_dict

    #convert everything to strings for storage in json or sqlite
    def stringify(self):
        db_name = self.db_name
        db_fp = self.db_fp
        date_modified = str(self.date_modified)
        file_hash = str(self.file_hash.hexdigest())
        return db_name, db_fp, date_modified, file_hash