import logging
from pathlib import Path
import json
from re import search

def query(name, catalog):
    json_fp = Path(catalog.name)

    if not json_fp.exists:
        raise Exception("Catalog {catalog!s} does not exist".format(catalog=json_fp))

    logging.debug("Reading this catalog: {json_fp!s}".format(json_fp=json_fp))

    catalog_json = {} #empty dictionary to hold catalog

    with json_fp.open() as f:
        catalog_json = json.load(f)

        logging.debug("First entry of catalog:\
            {first_entry!s}".format(first_entry=next(iter(catalog_json.items()))))
        
        # Filters dictionary by regex matching name
        newDict = dict(filter(lambda elem: search(name, elem[0]), catalog_json.items()))

        print('I found these : ')
        print(newDict)
