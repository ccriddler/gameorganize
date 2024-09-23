from gameorganize.model.game import GameEntry, Completion, Priority, Ownership
from gameorganize.model.platform import Platform
from gameorganize.db import db
from flask_setup import test_app, client, runner

def test_entries(client):
    """Add some test games, check if they go into the DB okay"""
    p1 = Platform(
        name="TestPlatform",
    )

    g1 = GameEntry(
        name="Oddworld: Abe's Oddysee", 
        platform=p1,
        completion=Completion.Beaten, 
        ownership=Ownership.Digital, 
        priority=Priority.Normal, 
        notes="I really liked this game",
    )

    g2 = GameEntry(
        name="Pikmin 2", 
        platform=p1,
        completion=Completion.Started, 
        priority=Priority.Low, 
    )

    g3 = GameEntry(
        name="Kingdom Hearts", 
        platform=p1,
        completion=Completion.Completed, 
        priority=Priority.Replay, 
        cheev=100, 
        cheev_total=100
    )

    db.session.add(p1)
    db.session.add(g1)
    db.session.add(g2)
    db.session.add(g3)
    db.session.commit()

    all_games=db.session.query(GameEntry)

    assert(g1 in all_games)
    assert(g2 in all_games)
    assert(g3 in all_games)

    db.session.delete(p1)
    db.session.commit()

    all_games=db.session.query(GameEntry)
    assert(not g1 in all_games)
    assert(not g2 in all_games)
    assert(not g3 in all_games)