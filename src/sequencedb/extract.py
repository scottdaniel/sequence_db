from pathlib import Path
import datetime
from .db import Database
from .meta import Metadata

def extract(fasta, dbname, date_m, metadata):
    #get file paths
    fasta_Path = Path(fasta.name)
    fasta_fp = fasta_Path.resolve()

    #set name of db
    if not dbname:
        dbname=Path(fasta.name).stem

    #get modified date of file
    if not date_m:
        mod_date_float = fasta_Path.stat().st_mtime
        date_modify = datetime.date.fromtimestamp(mod_date_float)

    db = Database(dbname, fasta_fp, date_modify)

    #create new metadata if not given; otherwise, check given metadata for any updates
    if not metadata:
        meta_path = fasta_fp.parents[0] / Path(str(dbname + "_metadata.tsv"))
        meta = Metadata(meta_path)
        meta.write_meta_new(db)
    else:
        meta_path = Path(metadata.name).resolve()
        meta = Metadata(meta_path)
        meta.check_meta(db)
    
    return db
