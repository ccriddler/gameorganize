from gameorganize.model.game import GameEntry, Completion
from gameorganize.model.platform import Platform#, find_or_create_platform
from gameorganize.importers.importer import ImporterBackend
from gameorganize.db import db

class ImporterRA():
    def __init__(self, backend : ImporterBackend, username:str, api_key:str):
        self.backend = backend
        self.username = username
        self.api_key = api_key

        self.params_default = {
            "z": self.username, 
            "y": self.api_key, 
            "u": self.username 
        }

    def parse_completion(self, game : dict):
        completion_award = game.get("HighestAwardKind")

        if(completion_award):
            if("beaten" in completion_award):
                return Completion.Beaten
            if("mastered" in completion_award):
                return Completion.Completed

        return Completion.Started

    def parse_platform(self, game : dict):
        return Platform(
            name = game.get("ConsoleName"),
            user = self.backend.user
        )

    def parse_game(self, game : dict):
        return GameEntry(
            name = game.get("Title"),
            completion = self.parse_completion(game),
            cheev = game.get("NumAwarded", 0),
            cheev_total = game.get("MaxPossible", 0),
            user = self.backend.user,
        )

    def get_user_completion_progress(self):
        return self.backend._get("https://retroachievements.org/API/API_GetUserCompletionProgress.php")

    def add(self, game : dict):
        platform = self.backend.find_or_create_platform(game.get("ConsoleName", ""))

        new_game = self.parse_game(game)
        new_game.platform = platform
        db.session.add(new_game)
        db.session.commit()

        return new_game

    def add_all(self, meta : dict):
        all_games = []

        for game_meta in meta.get("Results", []):
            new_game = self.add(game_meta)
            all_games.append(new_game)
        
        return all_games
