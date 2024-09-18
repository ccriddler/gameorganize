from gameorganize.db import db
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column

class Platform(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

@event.listens_for(Platform.__table__, 'after_create')
def platform_after_create(target, connection, **kw):
    print("Prefilling Platform values")
    default_names = [
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

    for name in default_names:
        db.session.add(Platform(name=name))
    db.session.commit()