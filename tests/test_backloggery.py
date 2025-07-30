from gameorganize.importers.backloggery import ImporterBackloggery
from pathlib import Path
import json
import pytest

basedir = Path(__file__).parent

def test_add_game(sample_backend, db_session):
    importer = ImporterBackloggery(sample_backend)

    csv_path = basedir / "data/backloggery-library.csv"
    data = importer.backend.csv2json(csv_path)

    # Add first game
    new_game = importer.add(data[0])

    assert(new_game.name == "Celeste Classic")
    assert(new_game in sample_backend.user.games)
    assert(len(sample_backend.user.games) == 1)

def test_add_all_games(sample_backend, db_session):
    importer = ImporterBackloggery(sample_backend)

    csv_path = basedir / "data/backloggery-library.csv"
    data = importer.backend.csv2json(csv_path)

    all_games = importer.add_all(data)

    db_session.commit()

    # all games were added successfully
    assert(len(sample_backend.user.games) == len(all_games))
