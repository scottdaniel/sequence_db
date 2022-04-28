from pathlib import Path

class Metadata:

    def __init__(self, meta_path):
        self.meta_fp = str(meta_path)
        self.mandatory_fields = [
            "fasta_header", "length", "md5sum", "date_modified"
        ]
        self.optional_fields = []

    def write_meta_new(self, db):
        sequence_lengths = db.parse_fasta()
        with open(self.meta_fp, "w") as f:
            f.write('\t'.join(self.mandatory_fields))
            for key in sequence_lengths.keys():
                f.write("\n")
                f.write(key + "\t" +
                        str(sequence_lengths[key]) + "\t" +
                        str(db.file_hash.hexdigest()) + "\t" +
                        str(db.date_modified) + "\t")

    def check_meta(self, db):
        sequence_lengths = db.parse_fasta()
        header_index = 0
        with open(self.meta_fp, "r") as read_h, open(self.meta_fp + "_tmp", "w") as write_h:
            for rows in self.parse_meta(read_h):
                #if the checksum in metdata sheet is the same as the checksum of the fasta file, just exit
                if rows['md5sum'] == db.file_hash.hexdigest():
                    print("FASTA file unchanged. Nothing to do")
                    Path(self.meta_fp + "_tmp").unlink()
                    exit(0)

                #print header
                if header_index == 0:
                    headers = [l for l in list(rows.keys())]
                    #get the names of optional columns in metadata
                    self.optional_fields = list(set(headers).difference(self.mandatory_fields))

                    #write the header as the keys in the dictionary
                    write_header = self.mandatory_fields[0] + "\t" + \
                                   "\t".join(self.optional_fields + self.mandatory_fields[1:]) + \
                                   "\n"
                    write_h.write(write_header)
                    header_index+=1

                #if fasta header in metadata is not in fasta file, remove it
                if rows['fasta_header'] not in sequence_lengths:
                    continue

                #if date column exists, check the date and only update the this date if the sequence changes (by length)
                #this part not tested
                date2write = str(db.date_modified)
                if 'date_modified' in rows:
                    if rows['length'] == str(sequence_lengths[rows['fasta_header']]):
                        date2write = rows['date_modified']

                write_row = rows['fasta_header'] + "\t"*(len(self.optional_fields) > 0)+ \
                            "\t".join([rows[o] for o in self.optional_fields]) + "\t" + \
                            str(sequence_lengths[rows['fasta_header']]) + "\t" + \
                            str(db.file_hash.hexdigest()) + "\t" + \
                            date2write + "\n"

                #write metadata rows out
                write_h.write(write_row)

                #remove sequence from sequence_lengths
                sequence_lengths.pop(rows['fasta_header'])

            #write new sequences in sequence_lengths to the metadata
            if sequence_lengths != {}:
                for id in sequence_lengths:
                    write_new_seq = id + "\t"*(len(self.optional_fields) + 1) + \
                                    str(sequence_lengths[id]) + "\t" + \
                                    str(db.file_hash.hexdigest()) + "\t" + \
                                    str(db.date_modified) + "\n"
                    write_h.write(write_new_seq)
        #rename tmp file
        Path(self.meta_fp + "_tmp").rename(self.meta_fp)

    #parse metadata if given
    def parse_meta(self, f):
        header_index = 0
        header_fields = []
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#") or (line == ""):
                continue
            tabs = line.split("\t")
            #get the header
            if header_index == 0:
                header_fields = [case.lower() for case in tabs]
                header_index+=1
            else:
                vals = dict(zip(header_fields, tabs))
                yield vals