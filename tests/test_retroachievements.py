from gameorganize.importers.retroachievements import ImporterRA
from gameorganize.importers.importer import ImporterBackend
from gameorganize.model.user import User
from gameorganize.model.game import Completion
from pathlib import Path
import json
import pytest

basedir = Path(__file__).parent

@pytest.fixture()
def sample_user(db_session):
    user = User(
        username="goodname",
        password="GoodPassword",
    )

    db_session.add(user)
    db_session.commit()

    return user

@pytest.fixture()
def sample_backend(sample_user):
    return ImporterBackend(sample_user)

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(sample_backend, db_session, apiId, apiKey):
    assert(apiId != None)
    assert(apiKey != None)

    importer = ImporterRA(
        backend=sample_backend, 
        username=apiId, 
        api_key=apiKey
    )
    fdata = importer.get_user_completion_progress()

    # Dump
    with open(basedir / "data/retroachievements_dump.json", "w") as buf:
        json.dump(fdata, buf)

def test_add(sample_backend, db_session):
    importer = ImporterRA(
        backend=sample_backend, 
        username=None, 
        api_key=None
    )

    with open(basedir / "data/retroachievements_example.json", "r") as buf:
        data = json.loads(buf.read())

        new_game = importer.add(data.get("Results")[0])

        assert(new_game.name == "Pikmin")
        assert(new_game.platform.name == "GameCube")
        assert(new_game.completion == Completion.Completed)


def test_add_all(sample_backend, db_session):
    importer = ImporterRA(
        backend=sample_backend, 
        username=None, 
        api_key=None
    )

    with open(basedir / "data/retroachievements.json", "r") as buf:
        data = json.loads(buf.read())

        games = importer.add_all(data)

        assert(len(data.get("Results")) == len(games))
