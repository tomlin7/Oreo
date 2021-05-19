import os, json


class OreoConfig:
    def __init__(self):
        self.config = None
        self.load_config()

        try:
            self.theme = "configs/themes/{0}".format(self.config['theme'])
        except:
            self.theme = "configs/themes/default.json"

    def load_config(self):
        with open("configs/config.json", "r") as data:
            self.config = json.load(data)