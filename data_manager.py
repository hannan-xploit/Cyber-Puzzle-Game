import json
import os

class DataManager:
    """Handles JSON save files for progress and user profile."""
    def __init__(self, filepath="save/data.json"):
        self.filepath = filepath
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filepath):
            return {"level": 1, "coins": 0, "stars": {}, "xp": 0}
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def save_game(self, level, coins, stars, xp):
        self.data.update({"level": level, "coins": coins, "stars": stars, "xp": xp})
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)