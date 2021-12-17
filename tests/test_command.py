import sequencedb.command

def test_main(capsys):
    sequencedb.command.main(["my-db"])
    captured = capsys.readouterr()
    assert captured.out == "Database is my-db\n"
