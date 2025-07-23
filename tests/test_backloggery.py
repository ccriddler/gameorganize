from gameorganize.importers.backloggery import ImporterBackloggery
from gameorganize.importers.importer import ImporterBackend
from gameorganize.model.user import User
from pathlib import Path

basedir = Path(__file__).parent

import json

def test_add_game(db_session):
    """Test backloggery CSV import"""
    user = User(
        username="goodname",
        password="GoodPassword",
    )

    db_session.add(user)
    db_session.commit()

    backend = ImporterBackend(user)
    importer = ImporterBackloggery(backend)

    csv_path = basedir / "data/backloggery-library.csv"
    data = importer.backend.csv2json(csv_path)

    # Add first game
    new_game = importer.add(data[0])

    assert(new_game.name == "Celeste Classic")
    assert(new_game in user.games)
    assert(len(user.games) == 1)

def test_add_all_games(db_session):
    """Test backloggery CSV import"""
    user = User(
        username="goodname",
        password="GoodPassword",
    )

    db_session.add(user)
    db_session.commit()

    backend = ImporterBackend(user)
    importer = ImporterBackloggery(backend)

    csv_path = basedir / "data/backloggery-library.csv"
    data = importer.backend.csv2json(csv_path)

    all_games = importer.add_all(data)

    # all games were added successfully
    assert(len(user.games) == len(all_games))
