import argparse
import datetime
import os
import json
from pathlib import Path
from .db import Database
from .meta import Metadata

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("dbname", help="Name of the database")
    p.add_argument("--import_db", type=argparse.FileType("r"),
        help=(
            "Filepath of database. Example is example_urease.fa"))
    p.add_argument("--import_meta", type=argparse.FileType("r"),
        help=(
            "Filepath of metadata. Example is example_metadata.txt"))
    p.add_argument("--date", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help=(
            "Date when database was downloaded in YYYY-MM-DD format. Default is to use modified date"))
    p.add_argument("--db_fp",
        help=(
            "Place to store the databases and metadata"))
    args = p.parse_args(argv)

    #if (args.import_db and not args.import_meta) or (args.import_meta and not args.import_db):
    #    p.error("Arguments --import_db and --import_meta must occur together")

    if args.date and not args.import_db:
        p.error("You cannot provide a date without a db")

    if args.db_fp is None:
        db_fp = Path(__file__).resolve().parents[2] / 'my_db'
    else:
        db_fp = Path(args.db_fp)

    db_fp.mkdir(parents=True, exist_ok=True)

    #Get the filepath to the db json file
    json_fp = Path(db_fp / 'db.json')

    if args.import_db:
        db_path = Path(args.import_db.name).resolve()

        if args.date is None:
            mod_date = os.path.getmtime(db_path)
            db_date = datetime.datetime.fromtimestamp(mod_date)
        else:
            db_date = args.date

        db = Database(db_path, db_date)
        db.print_headers_n_lengths()

        # put metadata file in my_db if not specified
        if not args.import_meta:
            meta_path = Path(__file__).resolve().parents[2] / 'my_db' / Path(str(args.dbname + "_metadata.tsv"))
            meta = Metadata(meta_path)
            meta.write_meta_new(db)
        else:
            meta_path = Path(args.import_meta.name).resolve()
            meta = Metadata(meta_path)
            meta.read_db(db)

        if not json_fp.exists():
            with json_fp.open(mode='w') as j_write:
                #get JSON items
                db_json = {args.dbname : [db.__dict__] + [meta.__dict__]}
                json.dump(db_json, j_write, indent=4)
        else:
            with json_fp.open(mode='r+') as j_append:
                # First we load existing data into a dict
                j_data = json.load(j_append)
                if args.dbname in j_data:
                    raise Exception("DB already exists. Do you want to update it?")
                else:
                    # Join new_data with file_data
                    j_data[args.dbname] = [db.__dict__] + [meta.__dict__]
                    # Sets file's current position at offset
                    j_append.seek(0)
                    # convert back to json.
                    json.dump(j_data, j_append, indent=4)

    if not json_fp.is_file():
        raise FileNotFoundError("DB JSON does not exist yet. Import a database first")
        
    print("Database is {0}".format(args.dbname))

# Subcommands
def importdb_subcommand(args):
    seqs = parse_fasta(args.input)
    db = Database(args)