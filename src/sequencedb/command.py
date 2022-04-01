import argparse
import datetime
import sys
from pathlib import Path
from .extract import extract
from .catalog import catalog

def extract_subcommand(args):
    print(args)
    extract(args.fasta, args.dbname, args.date_m, args.metadata)

def catalog_subcommand(args):
    print(args)
    catalog(args.dirname, args.catname)

def dir_path(path):
    if Path.is_dir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def main(argv=None):
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(help='Subcommands')

    extract_subparser = subparsers.add_parser(
        "extract", help="Extract information from a fasta file and creates metadata for it.")

    extract_subparser.add_argument("--dbname", help="Name of the database, default is the filename\
        without an extension")
    extract_subparser.add_argument("--fasta", type=argparse.FileType("r"),
        help=(
            "Filepath of fasta. Example is example_urease.fa"))
    extract_subparser.add_argument("--meta", type=argparse.FileType("r"),
        help=(
            "Filepath of metadata. Example is example_metadata.txt"))
    extract_subparser.add_argument("--date", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        help=(
            "Date when database was downloaded in YYYY-MM-DD format. Default is to use created date"))

    extract_subparser.set_defaults(func=extract_subcommand)

    catalog_subparser = subparsers.add_parser(
        "catalog", help="Searches through subdirectories for fasta sequences,\
            then builds a catalog of these with associated metadata"
    )

    catalog_subparser.add_argument("--dirname", type=dir_path,
    help="Directory where catalog will search for fasta files",
    default=Path.cwd())

    catalog_subparser.add_argument("--catname",
    help="Name of the catalog. json extensions will automatically be added",
    default="sequence_catalog")

    catalog_subparser.set_defaults(func=catalog_subcommand)

    #where the subcommand is detected
    args = main_parser.parse_args(argv)
    
    # print usage if user only enters the program name
    if len(sys.argv) < 2:
        main_parser.print_usage()
        sys.exit(1)

    #where the args are passed to the subcommand
    args.func(args)
