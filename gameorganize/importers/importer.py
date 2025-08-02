import csv
import requests

from gameorganize.model.user import User
from gameorganize.model.platform import Platform
from gameorganize.db import db

class ImporterBackend():
    def __init__(self, user : User):
        self.user = user
        self.params_default = {}
        self.platform_memo = {}

    def csv2json(self, path):
        jsonArray = []
        
        #read csv file
        with open(path, encoding='utf-8') as csvf: 
            #load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf) 

            #convert each csv row into python dict
            for row in csvReader: 
                #add this python dict to json array
                jsonArray.append(row)

        return jsonArray

    def find_or_create_platform(self, platform_name):
        platform = self.find_platform(platform_name)

        if(not platform):
            platform = self.create_platform(platform_name)

        return platform

    def find_platform(self, platform_name : str):
        # Risky speedup
        if(not platform_name in self.platform_memo):
            platform = db.session.query(Platform).where(
                Platform.user_id == self.user.id and
                Platform.name == platform_name
            ).first()

            if(not platform):
                return None

            self.platform_memo[platform_name] = platform

        return self.platform_memo[platform_name]

    def create_platform(self, platform_name):
        platform = Platform(
            name = platform_name,
            user_id = self.user.id
        )

        db.session.add(platform)
        db.session.commit()
        return platform

    # Run get request, passing default params + custom params
    def _get(self, url : str, params : dict = {}) -> dict:
        r = requests.get(url, params=self.params_default | params)

        if(r.status_code != 200):
            raise Exception(f"Error fetching data, {r.status_code}: {r.reason}")

        return r.json()
