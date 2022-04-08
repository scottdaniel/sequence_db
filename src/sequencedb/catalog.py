import logging
from pathlib import Path
import json
from .extract import extract
from itertools import chain

#list of accepted sequence extensions
SEQEXT = ["fa", "fasta", "fna", "faa", "aa", "pep"]

def catalog(dirname, catname):
    #builds a list of fastas after walking through directories
    #using extract() to get pertinent information
    #dumps information into a json
    #already checked is_dir for dirname in command.py

    dirname = Path(dirname).resolve()
    logging.debug("Searching through {dirname!s}".format(dirname=dirname))

    json_fp = Path(dirname, catname + ".json")
    logging.debug("Saving catalog of sequences to: {json_fp!s}".format(json_fp=json_fp))

    #empty list for fasta file names
    files_to_extract = []

    #find sequence files and put into list of lists
    for EXT in SEQEXT:
        found_files = sorted(Path(dirname).glob("**/*."+EXT))
        if found_files:
            files_to_extract.append(found_files)
    
    #if no fastas found, throw an error
    if not files_to_extract:
        raise Exception("Could not find any files with the extensions: {SEQEXT}".format(SEQEXT=SEQEXT))

    logging.debug("Found these files: {files_to_extract!r}".format(files_to_extract=files_to_extract))

    #empty dictionary to hold fasta information
    catalog = {}
    
    #check if catalog already exists
    #TODO: allow for overwriting of catalog
    if not json_fp.exists():
        with json_fp.open(mode='w') as j_write:
            #iterate through the list of lists
            for posix_path in chain.from_iterable(files_to_extract):
                #open file (needed for extract function)
                file = open(posix_path)
                print("Working on: {file!r}".format(file=file.name))
                #use stringify method of db class (otherwise json.dump chokes on date and md5 hashes)
                db_tuple = extract(fasta=file, dbname="", date_m="", metadata="").stringify()
                logging.debug(db_tuple)
                #create a dictionary from tuple because that is what json wants
                db_dict = {db_tuple[0] : {"dbname" : db_tuple[1], "data_modified" : db_tuple[2], "md5sum" : db_tuple[3]}}
                #add to dictionary
                catalog.update(db_dict)
            if catalog:
                #if catalog actually contains data, dump into json file
                json.dump(catalog, j_write, indent=4)
                print("Dictionary of sequences written to: {json}.".format(json=str(json_fp)))
                print("Catalog found {length} sequences to write information about.".format(length=len(catalog)))
    else:
        raise Exception("Sequence catalog: {catalog!r} already exists.\n\
            Cowardly refusing to overwrite.".format(catalog=str(json_fp)))