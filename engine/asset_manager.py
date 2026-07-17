import pygame

class AssetManager:
    def __init__(self):
        self.fonts = {}

    def load_font(self, name, path, size):
        try:
            self.fonts[name] = pygame.font.Font(path, size)
        except Exception as e:
            print(f"Font Error: {e}")
            self.fonts[name] = pygame.font.SysFont("Arial", size)

    def get_font(self, name):
        return self.fonts.get(name)