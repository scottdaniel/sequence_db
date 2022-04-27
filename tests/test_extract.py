from pathlib import Path
from sequencedb import extract
import pytest

#grab the fasta file from sample_fastas
example_fp = Path(__file__).resolve().parents[1] / 'example' / 'sample_fastas'
test_files = [str(f.name) for f in example_fp.iterdir() if f.is_file()]

def make_new_meta(fasta_file):
      #make tmp directory
      tmp_dir = example_fp / 'tmp'
      tmp_dir.mkdir(parents=True, exist_ok=True)
      tmp_fasta_fp = tmp_dir / fasta_file
      #make new fasta file in tmp directory
      with open(example_fp / fasta_file, "r") as f:
            tmp_fasta_fp.write_text(f.read(), encoding="utf-8")
      example_r = open(tmp_fasta_fp, "r")
      extract.extract(example_r, None, None, None)

def test_new_meta():
      for test_fasta in test_files:
            make_new_meta(test_fasta)
            #these test fasta files should have a .fasta extension
            new_meta_fp = example_fp / 'tmp' / (test_fasta[:-6] + '_metadata.tsv')
            assert new_meta_fp.exists
      
def test_catch_exception():
      for test_fasta in test_files:
            existing_metaname = test_fasta[:-6] + '_metadata.tsv'
            with pytest.raises(Exception) as exc_info:
                  make_new_meta(test_fasta)
            assert str(exc_info.value) == '\nThe metadata file ' + existing_metaname + ' already exists.\n' + 'You can use the --metadata flag to update the existing metadata'

def test_finish():
      tmp_fp = example_fp / 'tmp'
      for child in [f for f in tmp_fp.iterdir() if f.is_file()]:
            child.unlink()
      tmp_fp.rmdir()