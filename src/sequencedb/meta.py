from pathlib import Path

class Metadata:
    fields = [
        "fasta_header", "Length", "Date_modified"
    ]

    def __init__(self, meta_path):
        self.meta_fp = str(meta_path)

    def get_meta_path(self):
        print("Meta path is {0}".format(self.meta_fp))

    def read_meta(self):
        db_seq_len = self.parse_meta(self.meta_fp)
        print("Sequence lengths are {0}".format(db_seq_len))

    def write_meta_new(self, db):
        with open(self.meta_fp, "w") as f:
            f.write('\t'.join(Metadata.fields) + '\n')
            for key in db.seq_len.keys():
                f.write(key + "\t" + str(db.seq_len[key]) + "\t" + db.date_downloaded)
                f.write("\n")

    #parse metadata if given
    # @classmethod
    # def parse_meta(cls, f):
    #     for line in f:
    #         line = line.rstrip("\n")
    #         if line.startswith("#") or (line == ""):
    #             continue
    #         toks = line.split("\t")
    #         vals = dict(zip(cls.fields, toks))
    #         if vals["ftp_path"] == "na":
    #             continue
    #         yield cls(**vals)