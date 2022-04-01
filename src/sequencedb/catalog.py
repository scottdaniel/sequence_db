from pathlib import Path
import json

#list of accepted sequence extensions
SEQEXT = ["fa", "fasta", "fna", "faa", "aa", "pep"]

def catalog(dirname, catname):
    #build a list of fastas after walking through directories
    #already checked is_dir in command.py
    #if no fastas found, throw an error
    dirname = Path(dirname).resolve()
    print("Searching through {dirname!s}".format(dirname=dirname))

    catname = Path(dirname, catname + ".json")
    print("Saving catalog of sequences to: {catname!s}".format(catname=catname))

    files_to_extract = []

    for EXT in SEQEXT:
        found_files = sorted(Path(dirname).glob("**/*."+EXT))
        if found_files:
            files_to_extract.append(found_files)
            print("Found these files: {files_to_extract!r}".format(files_to_extract=files_to_extract))

    #extract metadata from each fasta

    #collect metadata and write to json file