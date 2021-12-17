import argparse

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("dbname", help="Name of the database")
    args = p.parse_args(argv)
    print("Database is {0}".format(args.dbname))
