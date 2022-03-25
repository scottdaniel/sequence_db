import os
from pathlib import Path
import datetime
from .db import Database
from .meta import Metadata

def extract(dbname, fasta, meta, date):
    if date and not fasta:
        os.error("You cannot provide a date without a fasta file")

    if fasta:
        fasta_path = Path(fasta.name).resolve()

    if date is None:
        create_date = os.path.getctime(fasta_path)
        db_date = datetime.datetime.fromtimestamp(create_date)
    else:
        db_date = date

    db = Database(fasta_path, db_date)