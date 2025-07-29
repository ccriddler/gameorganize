from gameorganize.model.user import User
import pytest

def test_pass_hash(db_session):
    user1 = User(
        username="samename",
        password="GoodPassword",
    )

    assert(user1.check_password_matches("GoodPassword"))

def test_dupe_user(db_session):
    user1 = User(
        username="samename",
        password="GoodPassword",
    )

    user2 = User(
        username="samename",
        password="OtherPassword",
    )

    db_session.add(user1)
    db_session.add(user2)
    with pytest.raises(Exception) as e:
        db_session.commit()
    db_session.rollback()

def test_lotta_users(db_session):
    for i in range(0, 100):
        new_user = User(
            username=f"samename{i}",
            password="GoodPassword",
        )
        db_session.add(new_user)
    db_session.commit()
    db_session.rollback()

def test_bad_password(db_session):
    with pytest.raises(Exception) as e:
        bad_user = User(
            username="badbaduser",
            password="pass",
        )
