from gameorganize.importers.retroachievements import ImporterRA
from gameorganize.importers.importer import ImporterBackend
from gameorganize.model.user import User
from gameorganize.model.game import Completion
from pathlib import Path
import json
import pytest

basedir = Path(__file__).parent

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(apiId, apiKey):
    importer = ImporterRA(username=apiId, api_key=apiKey)
    fdata = importer.fetch()
    print(f"Fetched data for {len(fdata)} games")
    with open("data/retroachievements.json", "w") as buf:
        json.dump(fdata, buf)

def test_add(db_session):
    user = User(
        username="goodname",
        password="GoodPassword",
    )

    db_session.add(user)
    db_session.commit()

    backend = ImporterBackend(user)
    importer = ImporterRA(backend, None, None)

    with open(basedir / "data/retroachievements.json", "r") as buf:
        data = json.loads(buf.read())

        new_game = importer.add(data.get("Results")[0])

        assert(new_game.name == "Pikmin")
        assert(new_game.platform.name == "GameCube")
        assert(new_game.completion == Completion.Started)


def test_add_all(db_session):
    user = User(
        username="goodname",
        password="GoodPassword",
    )

    db_session.add(user)
    db_session.commit()

    backend = ImporterBackend(user)
    importer = ImporterRA(backend, None, None)
    with open(basedir / "data/retroachievements.json", "r") as buf:
        data = json.loads(buf.read())

        games = importer.add_all(data)

        assert(len(data.get("Results")) == len(games))
