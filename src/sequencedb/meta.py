from pathlib import Path

class Metadata:

    def __init__(self, meta_path):
        self.meta_fp = str(meta_path)
        self.mandatory_fields = [
            "fasta_header", "length", "date_created", "date_modified"
        ]

    def get_meta_path(self):
        print("Meta path is {0}".format(self.meta_fp))

    def print_meta(self):
        meta_print = self.parse_meta(self.meta_fp)
        print("Sequence lengths are {0}".format(meta_print))

    def write_meta_new(self, db):
        sequence_lengths = db.get_lengths()
        with open(self.meta_fp, "w") as f:
            f.write('\t'.join(self.mandatory_fields))
            for key in sequence_lengths.keys():
                f.write("\n")
                f.write(key + "\t" +
                        str(sequence_lengths[key]))# + "\t" +
#                        db.date_created + "\t" +
#                        db.date_modified)

    def check_n_write_meta(self):
        with open(self.meta_fp) as f:
            for header in self.parse_meta(f):
                print(header)
                #self.assemblies[assembly.accession] = assembly
        #return self.assemblies

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
                header_index+=1
                yield vals