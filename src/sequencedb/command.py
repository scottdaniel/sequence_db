import argparse
import datetime
import json
from pathlib import Path
from .extract import extract

def extract_subcommand(args):
    print(args)
    extract(args.fasta, args.dbname, args.date_m, args.metadata)

def catalog_subcommand(args):
    print(args)

def main(argv=None):
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(help='Subcommands')

    extract_subparser = subparsers.add_parser("extract",
        help="Extract information from a fasta file and create/update a metadata for each sequence")
    extract_subparser.add_argument("fasta",
        type=argparse.FileType("r"),
        help="Fasta file. Example is example_urease.fa")
    extract_subparser.add_argument("--dbname",
        help="Name of the database, default is the filename without an extension")
    extract_subparser.add_argument("--date_m", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help="Date (YYYY-MM-DD) of when the fasta file was last modified")
    extract_subparser.add_argument("--metadata",
        type=argparse.FileType("r"),
        help="Metadata where each row is a fasta sequence. Example is example_metadata.txt")

    extract_subparser.set_defaults(func=extract_subcommand)

    args = main_parser.parse_args(argv)
    args.func(args)

    if args.db_fp is None:
        db_fp = Path(__file__).resolve().parents[2] / 'my_db'
    else:
        db_fp = Path(args.db_fp)

    db_fp.mkdir(parents=True, exist_ok=True)

    #Get the filepath to the db json file
    json_fp = Path(db_fp / 'db.json')

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
