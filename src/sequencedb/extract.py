import os

def extract(dbname, fasta, meta, date):
    if date and not fasta:
        os.error("You cannot provide a date without a fasta file")