import os
from pathlib import Path
import datetime
from .db import Database
from .meta import Metadata

def extract(dbname, fasta, meta, date):
    if not fasta:
        raise Exception("You need to provide a fasta file")

    fasta_path = Path(fasta.name).resolve()

    if date is None:
        create_date = os.path.getctime(fasta_path)
        db_date = datetime.datetime.fromtimestamp(create_date)
    else:
        db_date = date

    db = Database(fasta_path, db_date)

    # put metadata file in my_db if not specified
    if not args.import_meta:
        meta_path = Path(__file__).resolve().parents[2] / 'my_db' / Path(str(args.dbname + "_metadata.tsv"))
        meta = Metadata(meta_path)
        meta.write_meta_new(db)
    else:
        meta_path = Path(args.import_meta.name).resolve()
        meta = Metadata(meta_path)
        meta.read_db(db)