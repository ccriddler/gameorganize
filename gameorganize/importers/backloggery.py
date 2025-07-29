from gameorganize.db import db
from gameorganize.importers.importer import ImporterBackend
from gameorganize.model.game import GameEntry, Completion
#from gameorganize.model.platform import Platform, find_or_create_platform
from gameorganize.model.user import User

# Library columns:
#    "Unique Game ID", "Title", "Platform", "Sub-Platform",
#    "Status", "Priority", "Format", "Ownership", "Notes",
#    "Child Of", "Last Updated"

class ImporterBackloggery():
    def __init__(self, backend : ImporterBackend):
        self.backend = backend

    def normalize_completion(self, completion:str):
        if(completion == "Unfinished"):
            return "Started"
        return "Unplayed"

    def parse_platform(self, game : dict):
        return Platform(
            name = game.get("Platform", ""),
            user = self.backend.user,
        )

    def parse_game(self, game : dict):
        completion_name = self.normalize_completion(game.get("Status", "Unplayed"))

        return GameEntry(
            completion = Completion[completion_name],
            name = game.get("Title"),
            notes = game.get("Notes", ""),
            user = self.backend.user,
        )

    def add(self, game : dict):
        platform_name = game.get("Platform", "")
        platform = self.backend.find_platform(platform_name)

        if(not platform):
            platform = self.backend.create_platform(platform_name)

        new_game = self.parse_game(game)
        new_game.platform = platform
        db.session.add(new_game)
        #db.session.commit()

        return new_game

    def add_all(self, all_games : dict):
        new_games = []
        for game in all_games:
            new_games.append(self.add(game))
        return new_games
