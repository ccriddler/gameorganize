from gameorganize.db import db
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

class Completion(enum.Enum):
    Null = -1
    Unplayed = 0
    Started = 1
    Beaten = 2
    Completed = 3
    Endless = 4

    @classmethod
    def choices(_class):
        return [(choice.name, choice.value) for choice in _class]

class Ownership(enum.Enum):
    Physical = 0
    Digital = 1
    FormerlyOwned = 2
    Subscription = 3
    Wishlist = 4

    @classmethod
    def choices(_class):
        return [(choice.name, choice.value) for choice in _class]

class Priority(enum.Enum):
    Abandoned = -1
    Paused = 1
    Low = 2
    Normal = 3
    High = 4
    NowPlaying = 5
    Replay = 6

    @classmethod
    def choices(_class):
        return [(choice.name, choice.value) for choice in _class]

class GameEntry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platform.id", ondelete='SET NULL'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    completion: Mapped[Completion] = mapped_column(default=Completion.Unplayed)
    ownership: Mapped[Ownership] = mapped_column(default=Ownership.Physical)
    priority: Mapped[Priority] = mapped_column(default=Priority.Normal)
    cheev: Mapped[int] = mapped_column(default=0)
    cheev_total: Mapped[int] = mapped_column(default=0)
    notes:Mapped[str] = mapped_column(default="")

    def __repr__(self):
        return f'<Game {self.name} @ {self.platform} [{self.completion.name}]>'
