from gameorganize.db import db
from gameorganize.model.game import GameEntry
from sqlalchemy import event, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

DEFAULT_PLATFORMS = [
    'Arcade',
    'Neo Geo',
    'Nintendo 3DS',
    'Nintendo 64',
    'Nintendo DS',
    'Nintendo Entertainment System',
    'Nintendo GameCube',
    'Nintendo Gameboy Advance', 
    'Nintendo Gameboy', 
    'Nintendo SNES', 
    'Nintendo Switch',
    'PC',
    'Playstation 2',
    'Playstation 3',
    'Playstation 4',
    'Playstation',
    'Scumm VM',
    'Sega Dreamcast', 
    'Sega Genesis', 
    'Sega Saturn', 
    'Xbox 360', 
    'Xbox One', 
    'Xbox', 
]
class Platform(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    games = relationship(GameEntry, backref='platform')

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='platform_unique_constraint'),
    )

#@event.listens_for(Platform.__table__, 'after_create')
#def platform_after_create(target, connection, **kw):
#    print("Prefilling Platform values")
#
#    for name in DEFAULT_PLATFORMS:
#        db.session.add(Platform(name=name))
#    db.session.commit()
