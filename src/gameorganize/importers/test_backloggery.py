from backloggery import ImporterBackloggery
from pathlib import Path

basedir = Path(__file__).parent

def test_import():
    importer = ImporterBackloggery()
    data = importer.csv_to_json(basedir / "test/backloggery-library.csv")
    games = importer.parse(data)
    assert(True)
    #print(games)