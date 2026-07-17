class LevelManager:
    """Manages level loading and progression."""
    def __init__(self):
        self.levels = [] # List of level configs
        self.current_level_idx = 0

    def get_current_level_data(self):
        return self.levels[self.current_level_idx]

    def unlock_next(self):
        self.current_level_idx += 1