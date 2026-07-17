import pygame
import random
import os
import json
import time
from game.effects import Spark

ASSET_IMAGE = "assets/puzzle.jpeg"
BEST_SCORES_FILE = "assets/best_scores.json"
BOARD_SIZE = 420          # pixels the puzzle image occupies on screen
BOARD_X, BOARD_Y = 90, 110


class Tile:
    def __init__(self, rect, image_surf, correct_pos, font, number):
        self.rect = rect
        self.image = image_surf
        self.target_rect = rect.copy()
        self.correct_pos = correct_pos     # where this tile SHOULD be when solved
        self.font = font
        self.number = number
        self.is_hovered = False
        self.scale = 1.0
        self._scale_target = 1.0

    def is_correct(self, current_pos):
        return current_pos == self.correct_pos

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self._scale_target = 1.06 if self.is_hovered else 1.0
        self.scale += (self._scale_target - self.scale) * 0.25

        # smooth glide toward target slot (eased movement)
        self.rect.x += (self.target_rect.x - self.rect.x) * 0.28
        self.rect.y += (self.target_rect.y - self.rect.y) * 0.28

    def draw(self, screen, show_numbers=True, correct=False):
        w, h = self.rect.width, self.rect.height
        sw, sh = int(w * self.scale), int(h * self.scale)
        img = pygame.transform.smoothscale(self.image, (sw, sh))
        draw_rect = img.get_rect(center=self.rect.center)
        screen.blit(img, draw_rect)

        border_color = (90, 230, 140) if correct else ((255, 255, 255) if self.is_hovered else (0, 255, 204))
        pygame.draw.rect(screen, border_color, draw_rect, 3, border_radius=8)

        if show_numbers:
            shadow = self.font.render(self.number, True, (0, 0, 0))
            text = self.font.render(self.number, True, (255, 255, 255))
            pos = text.get_rect(center=(draw_rect.centerx + 1, draw_rect.centery + 1))
            screen.blit(shadow, pos)
            screen.blit(text, text.get_rect(center=draw_rect.center))


class Grid:
    def __init__(self, font, level="Easy"):
        self.font = font
        self.level = level
        self.grid_size = {"Easy": 3, "Medium": 4, "Hard": 5}[level]
        self.load_image()
        self.show_numbers = True
        self.hint_pos = None
        self.hint_timer = 0
        self.sparks = []
        self.start_time = time.time()
        self.elapsed = 0
        self.reset_positions()

    # ---------------------------------------------------------- assets
    def load_image(self):
        if os.path.exists(ASSET_IMAGE):
            raw = pygame.image.load(ASSET_IMAGE).convert()
        else:
            raw = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
            raw.fill((20, 20, 40))
        self.full_image = pygame.transform.smoothscale(raw, (BOARD_SIZE, BOARD_SIZE))

    # ---------------------------------------------------------- setup
    def reset_positions(self):
        self.tiles = {}
        size = self.grid_size
        self.empty_pos = (size - 1, size - 1)
        w, h = BOARD_SIZE // size, BOARD_SIZE // size
        for row in range(size):
            for col in range(size):
                if row == size - 1 and col == size - 1:
                    continue
                rect = pygame.Rect(BOARD_X + col * w, BOARD_Y + row * h, w - 3, h - 3)
                sub = self.full_image.subsurface((col * w, row * h, w, h))
                self.tiles[(row, col)] = Tile(rect, sub, (row, col), self.font, str(row * size + col + 1))
        self.strokes = 0
        self.won = False
        self.start_time = time.time()
        self.elapsed = 0

    def tile_size(self):
        return BOARD_SIZE // self.grid_size

    def slot_rect(self, pos):
        w = self.tile_size()
        return pygame.Rect(BOARD_X + pos[1] * w, BOARD_Y + pos[0] * w, w - 3, w - 3)

    # ---------------------------------------------------------- shuffle
    def shuffle_grid(self):
        self.reset_positions()
        last_move = None
        for _ in range(self.grid_size * self.grid_size * 25):
            neighbors = [p for p in self.tiles
                         if abs(p[0] - self.empty_pos[0]) + abs(p[1] - self.empty_pos[1]) == 1]
            if last_move in neighbors and len(neighbors) > 1:
                neighbors.remove(last_move)  # avoid instantly undoing the previous move
            move = random.choice(neighbors)
            tile = self.tiles.pop(move)
            tile.target_rect = self.slot_rect(self.empty_pos)
            tile.rect = tile.target_rect.copy()
            self.tiles[self.empty_pos] = tile
            last_move = self.empty_pos
            self.empty_pos = move
        self.strokes = 0
        self.won = False
        self.start_time = time.time()

    # ---------------------------------------------------------- input
    def handle_click(self, pos):
        if self.won:
            return
        for p, tile in list(self.tiles.items()):
            if tile.rect.collidepoint(pos) and abs(p[0] - self.empty_pos[0]) + abs(p[1] - self.empty_pos[1]) == 1:
                tile.target_rect = self.slot_rect(self.empty_pos)
                self.tiles[self.empty_pos] = tile
                del self.tiles[p]
                new_pos = self.empty_pos
                self.empty_pos = p
                self.strokes += 1

                # sparkle burst if the tile landed on its correct spot
                if tile.is_correct(new_pos):
                    cx, cy = tile.target_rect.center
                    self.sparks += [Spark(cx, cy) for _ in range(10)]

                self.check_win()
                break

    def move_tile_at(self, pos):
        """Programmatic move used by hint/auto-play (same rule as a click)."""
        self.handle_click(self.tiles[pos].rect.center) if pos in self.tiles else None

    # ---------------------------------------------------------- hint
    def find_hint(self):
        """Suggest a neighbour of the empty slot whose move reduces total
        'distance from solved' the most - a simple, honest hint, not a full solver."""
        best, best_score = None, -1
        for p in self.tiles:
            if abs(p[0] - self.empty_pos[0]) + abs(p[1] - self.empty_pos[1]) != 1:
                continue
            tile = self.tiles[p]
            before = abs(p[0] - tile.correct_pos[0]) + abs(p[1] - tile.correct_pos[1])
            after = abs(self.empty_pos[0] - tile.correct_pos[0]) + abs(self.empty_pos[1] - tile.correct_pos[1])
            score = before - after
            if score > best_score:
                best_score, best = score, p
        return best

    def show_hint(self):
        self.hint_pos = self.find_hint()
        self.hint_timer = 90  # frames the highlight stays visible

    # ---------------------------------------------------------- win logic
    def check_win(self):
        if len(self.tiles) != self.grid_size * self.grid_size - 1:
            return
        for pos, tile in self.tiles.items():
            if pos != tile.correct_pos:
                return
        self.won = True
        self.save_best_score()

    def save_best_score(self):
        try:
            data = {}
            if os.path.exists(BEST_SCORES_FILE):
                with open(BEST_SCORES_FILE) as f:
                    data = json.load(f)
            entry = data.get(self.level, {"moves": None, "time": None})
            improved = False
            if entry["moves"] is None or self.strokes < entry["moves"]:
                entry["moves"] = self.strokes
                improved = True
            if entry["time"] is None or self.elapsed < entry["time"]:
                entry["time"] = round(self.elapsed, 1)
                improved = True
            data[self.level] = entry
            os.makedirs(os.path.dirname(BEST_SCORES_FILE), exist_ok=True)
            with open(BEST_SCORES_FILE, "w") as f:
                json.dump(data, f)
            self.new_record = improved
        except OSError:
            self.new_record = False

    def get_best_score(self):
        if os.path.exists(BEST_SCORES_FILE):
            try:
                with open(BEST_SCORES_FILE) as f:
                    data = json.load(f)
                return data.get(self.level)
            except (OSError, json.JSONDecodeError):
                return None
        return None

    # ---------------------------------------------------------- frame update
    def update(self, mouse_pos):
        if not self.won:
            self.elapsed = time.time() - self.start_time
        for tile in self.tiles.values():
            tile.update(mouse_pos)
        if self.hint_timer > 0:
            self.hint_timer -= 1
        else:
            self.hint_pos = None
        for s in self.sparks:
            s.update()
        self.sparks = [s for s in self.sparks if not s.dead()]

    def draw(self, screen):
        # frame around the whole board
        frame = pygame.Rect(BOARD_X - 6, BOARD_Y - 6, BOARD_SIZE + 12, BOARD_SIZE + 12)
        pygame.draw.rect(screen, (0, 255, 204), frame, 2, border_radius=12)

        for pos, tile in self.tiles.items():
            correct = tile.is_correct(pos)
            tile.draw(screen, self.show_numbers, correct)

        if self.hint_pos and self.hint_pos in self.tiles:
            r = self.tiles[self.hint_pos].rect.inflate(6, 6)
            pygame.draw.rect(screen, (255, 221, 87), r, 3, border_radius=10)

        for s in self.sparks:
            s.draw(screen)
