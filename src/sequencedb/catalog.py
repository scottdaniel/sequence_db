from pathlib import Path
import json

def catalog(dirname, catname):
    #build a list of fastas after walking through directories
    #already checked is_dir in command.py
    #if no fastas found, throw an error
    print("Searching through {dirname!r}".format(dirname=dirname))

    #extract metadata from each fasta

    #collect metadata and write to json file