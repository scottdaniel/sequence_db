# sequence_db

Problem to solve with this software:
* Plain fasta files are bad databases

First ideas:
* Database of genes for secondary bile-acid synthesis (avg. file size = KB's)
* TCGA downloads of cancer genes (avg. file size = 3GB uncompressed)
* Host genomes used for microbiome research (size depends on host)
* More organized KEGG ortholog database (whole peptide database = 4.3GB uncompressed)
* Urease genes (avg. file size = KB's)

What we want to feed into a database:
* Fasta file(s)
* File(s) of metadata (.json, .yaml, or something else)
* OR Sqlite database of metadata

What it might look like in the folder:
```
  my_folder
    |
     \_ my.fasta
    |
     \_ metadata.json OR
    |
     \_ metadata.db
```
Example commands:
* list_sequences [db_name] : spits out the names of sequences
* get_metadata [sequence_name] : gives you metadata for a given sequence
* import_db [fasta_file] [metadata_1] [metadata_2] : prepares the first iteration of the database, timestamps and gives info on where data was downloaded
* update_db [your_db] [other fasta file] [other metadata] : performs a union / updates your_db with new / updated sequences
* update_metadata [your_db] [sequence_name] [updated_data] : change a specific item of metadata
* summarize_db [your_db] : gives statistics like # of sequences, # of metadata items, data created, date downloaded, etc.

Tasks (2022-03-02):
* When importing fasta/metadata, _put_ timestamps in the metadata itself {Kyle's idea}
* _Convert_ current functionality (creating a json of all the databases) into a subcommand 'catalog' {Scott's idea}

## Development

To work on this package, you'll need Python >= 3.7 installed. The
easiest way to manage Python versions is with `conda`. To make a new
environment with Python 3.7 and pytest, use

    conda create -n sequence_db python=3.7 pytest

After the environment is installed, activate it with

    conda activate sequence_db

You should see your prompt change to include `(sequence_db)` at the
beginning.

The next step is to install the `sequence_db` package in development
mode. Working from this directory, use the command

    pip install -e .

To run the tests, use the following command:

    pytest
