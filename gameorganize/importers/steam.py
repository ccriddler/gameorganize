from gameorganize.model.game import GameEntry, Completion
#from gameorganize.model.platform import Platform, find_or_create_platform
from gameorganize.importers.importer import ImporterBackend

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

        self.platform = backend.find_platform("Steam") #find_or_create_platform("Steam")

    # API data -> Database objects
    def _parse_game(self, meta_game : dict, meta_cheev : dict = {}):
        game_entry = GameEntry(
            name = meta_game.get("name", ""),
            platform = self.platform,
            ownership = Ownership.Digital,
        )

        if(meta_cheev):
            cheev_all = meta_cheev.get("playerstats", {}).get("achievements", [])
            cheev_got = list(filter(lambda a: (a["achieved"] == 1), cheev_all)) ,

            playtime = meta_game.get("playtime_forever",0),

            completion = Completion.Unplayed
            if(playtime > 0):
                completion = Completion.Started
            if(len(cheev) > 0 and cheev_got == cheev):
                completion = Completion.Completed

            game_entry.cheev = len(cheev_got)
            game_entry.cheev_total = len(cheev_all)
            game_entry.completion = completion

        return game_entry

    # Steam API Wrapper functions

    # https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_(v0001)
    def get_owned_games(self, include_appinfo=1, include_ftp=1):
        print(f"Fetching games for user id {self.steam_id}")

        return self.backend._get(
            "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/", 
            {
                "include_gameinfo":include_appinfo,
                "include_played_free_games":include_ftp,
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

    # Combine get reuests for achievements + owned games
    def get_owned_games_and_achievements(self):
        meta_all = self.get_owned_games()

        cheev_dict = {}

        # Fetch achievement data, inject into big game list
        for game in meta_all.get("response", {}).get("games", []):
            appid = game.get("appid", 0)
            cheev = self.get_player_achievements(appid)
            cheev_dict[appid] = cheev

        meta_all["response"]["achievements"] = cheev_dict

        return meta_all

    def parse_owned_games(self, meta : dict):
        meta_game_all = meta.get("response", {}).get("games", [])
        meta_cheev_all = meta.get("response", {}).get("achievements", {})

        all_games = []

        for meta_game in meta_game_all:
            appid = meta_game.get("appid", 0)
            game_entry = self._parse_game(meta_game, meta_cheev_all.get(appid, {}))
            all_games.append(game_entry)

        return all_games
