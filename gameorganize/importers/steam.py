from gameorganize.db import db
from gameorganize.importers.importer import ImporterBackend
from gameorganize.model.game import GameEntry, Completion

class ImporterSteam():
    def __init__(self, backend : ImporterBackend, steam_id:str, api_key:str):
        self.backend = backend
        self.steam_id = steam_id
        self.api_key = api_key

        self.params_default = {
            "key":self.api_key,
            "steamid":self.steam_id,
            "format":"json",
        }

        self.platform = backend.find_or_create_platform("Steam")

    # Steam API Wrapper functions

    # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_(v0001)
    def get_owned_games(self, include_appinfo=1, include_free=1):
        print(f"Fetching games for user id {self.steam_id}")

        return self.backend._get(
            "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/", 
            {
                "include_gameinfo":include_appinfo,
                "include_played_free_games":include_free,
            }
        )

    # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerAchievements_(v0001)
    def get_player_achievements(self, app_id:str):
        print(f"Fetching player achievements for appid {app_id}")

        return self.backend._get(
            "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/", 
            {
                "appid":app_id,
            }
        )

    def get_player_achievements_bulk(self, app_ids : list[str]):
        cheev_meta = {}

        for app_id in app_ids:
            cheev_meta[app_id] = self.get_player_achievements(app_id)

        return cheev_meta

    def parse_game(self, meta_game : dict):
        return GameEntry(
            name = meta_game.get("name", ""),
            platform = self.platform,
        )

    def parse_achievements(self, game_entry, meta_game : dict, meta_cheev : dict):
        cheev_all = meta_cheev.get("playerstats", {}).get("achievements", [])
        cheev_got = list(filter(lambda a: (a["achieved"] == 1), cheev_all))

        playtime = meta_game.get("playtime_forever",0)

        completion = Completion.Unplayed
        if(playtime > 0):
            completion = Completion.Started
        if(len(cheev_all) > 0 and cheev_got == cheev_all):
            completion = Completion.Completed

        game_entry.cheev = len(cheev_got)
        game_entry.cheev_total = len(cheev_all)
        game_entry.completion = completion

        return game_entry

    def add(self, game : dict):
        new_game = GameEntry(
            name = game.get("name"),
            platform = self.platform,
            user = self.backend.user,
        )

        db.session.add(new_game)

        return new_game

    def add_all(self, meta_owned_games : dict, meta_achievements_bulk : dict = {}):
        all_games = []

        for meta_game in meta_owned_games.get("response", {}).get("games", []):
            game_entry = self.add(meta_game)

            app_id = meta_game.get("appid", 0)
            if(app_id in meta_achievements_bulk):
                meta_cheev = meta_acheivements_bulk[app_id]
                game_entry = self.parse_achievements(game_entry, meta_game, meta_cheev)

            all_games.append(game_entry)

        return all_games
