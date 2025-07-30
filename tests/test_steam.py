from gameorganize.importers.steam import ImporterSteam
from gameorganize.model.game import Completion
from pathlib import Path
import json
import pytest

basedir = Path(__file__).parent

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(apiId, apiKey):
    importer = ImporterSteam(apiId, apiKey)
    
    fdata = importer.fetch()
    assert (fdata is not None)

    print(f"Fetched data for {len(fdata)} games")
    with open(basedir / "data/steam.json", "w") as buf:
        json.dump(fdata, buf)

@pytest.mark.skip(reason="reduce server stress")
def test_fetch_stats(apiId, apiKey):
    importer = ImporterSteam(apiId, apiKey)

    stats = importer.fetch_stats(215670)
    assert (stats.get("achievements", []) is not None)

    #print(stats)

def test_add_achievements(sample_backend, db_session):
    importer = ImporterSteam(
        backend=sample_backend, 
        steam_id=None, 
        api_key=None
    )    

    #completion_null = importer.get_completion(0, {})
    #assert completion_null[0] == Completion.Unplayed

    with open(basedir / "data/steam-cheev-started.json", "r") as buf:
        meta_game = {"name":"Counter Strike: Source", "playtime_forever":1}
        game_entry = importer.parse_game(meta_game)

        meta_cheev = json.loads(buf.read())

        game_entry = importer.parse_achievements(game_entry, meta_game, meta_cheev)

        assert(game_entry.completion == Completion.Started)

    with open(basedir / "data/steam-cheev-completed.json", "r") as buf:
        meta_game = {"name":"Terraria", "playtime_forever":99}
        game_entry = importer.parse_game(meta_game)

        meta_cheev = json.loads(buf.read())

        game_entry = importer.parse_achievements(game_entry, meta_game, meta_cheev)

        assert(game_entry.completion == Completion.Completed)

def test_parse_owned(sample_backend, db_session):
    importer = ImporterSteam(
        backend=sample_backend, 
        steam_id=None, 
        api_key=None
    )

    with open(basedir / "data/steam-owned-games.json", "r") as buf:
        meta_owned_games = json.loads(buf.read())
        games = importer.add_all(meta_owned_games)
        db_session.commit()

    assert(len(sample_backend.user.games) == len(games))
