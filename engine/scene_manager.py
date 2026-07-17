import pygame
from game.puzzle_logic import Grid

MENU, PLAYING, WIN = "menu", "playing", "win"

TEAL = (0, 255, 204)
TEAL_DARK = (0, 200, 150)
GOLD = (255, 221, 87)
WHITE = (255, 255, 255)


class Button:
    """Rounded button with hover-glow and a small press animation."""
    def __init__(self, rect, label, base_color=TEAL, hover_color=TEAL_DARK, text_color=(0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.press = 0
        self.selected = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.press > 0:
            self.press -= 1

    def clicked(self, pos):
        hit = self.rect.collidepoint(pos)
        if hit:
            self.press = 8
        return hit

    def draw(self, screen, font):
        shrink = 3 if self.press > 0 else 0
        r = self.rect.inflate(-shrink, -shrink)
        color = self.hover_color if getattr(self, "hovered", False) else self.base_color
        if self.selected:
            glow = r.inflate(8, 8)
            pygame.draw.rect(screen, GOLD, glow, 3, border_radius=14)
        pygame.draw.rect(screen, color, r, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), r, 2, border_radius=10)
        text = font.render(self.label, True, self.text_color)
        screen.blit(text, text.get_rect(center=r.center))


class SceneManager:
    def __init__(self, font):
        self.font = font
        self.small = pygame.font.SysFont("Arial", 16, bold=True)
        self.title_font = pygame.font.SysFont("Georgia", 46, bold=True)
        self.big_font = pygame.font.SysFont("Georgia", 34, bold=True)

        self.state = MENU
        self.level = "Medium"
        self.grid = Grid(font, self.level)

        # ---- menu buttons ----
        self.menu_buttons = {
            "Easy": Button((210, 300, 180, 55), "Easy"),
            "Medium": Button((210, 370, 180, 55), "Medium"),
            "Hard": Button((210, 440, 180, 55), "Hard"),
            "Play": Button((210, 520, 180, 60), "Play ▶", base_color=GOLD, hover_color=(255, 200, 40)),
        }
        self.menu_buttons[self.level].selected = True

        # ---- in-game buttons ----
        self.game_buttons = {
            "Shuffle": Button((30, 555, 110, 42), "Shuffle"),
            "Hint": Button((150, 555, 90, 42), "Hint", base_color=GOLD, hover_color=(255, 200, 40)),
            "Numbers": Button((250, 555, 110, 42), "Hide #s"),
            "Undo": Button((370, 555, 110, 42), "Undo ↶"),
            "Menu": Button((490, 555, 90, 42), "Menu", base_color=(230, 90, 90), hover_color=(200, 60, 60)),
        }

        # ---- win screen buttons ----
        self.win_buttons = {
            "Again": Button((150, 560, 140, 50), "Play Again", base_color=GOLD, hover_color=(255, 200, 40)),
            "Menu": Button((350, 560, 120, 50), "Menu"),
        }

    # -------------------------------------------------------------- input
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if self.state == MENU:
            for name, btn in self.menu_buttons.items():
                if btn.clicked(event.pos):
                    if name in ("Easy", "Medium", "Hard"):
                        self.level = name
                        for n2, b2 in self.menu_buttons.items():
                            b2.selected = (n2 == name)
                    elif name == "Play":
                        self.grid = Grid(self.font, self.level)
                        self.grid.shuffle_grid()
                        self.state = PLAYING

        elif self.state == PLAYING:
            for name, btn in self.game_buttons.items():
                if btn.clicked(event.pos):
                    if name == "Shuffle":
                        self.grid.shuffle_grid()
                    elif name == "Hint":
                        self.grid.show_hint()
                    elif name == "Numbers":
                        self.grid.show_numbers = not self.grid.show_numbers
                        btn.label = "Hide #s" if self.grid.show_numbers else "Show #s"
                    elif name == "Undo":
                        self.grid.undo()
                    elif name == "Menu":
                        self.state = MENU
                    return  # don't also register a tile click
            self.grid.handle_click(event.pos)
            if self.grid.won:
                self.state = WIN

        elif self.state == WIN:
            for name, btn in self.win_buttons.items():
                if btn.clicked(event.pos):
                    if name == "Again":
                        self.grid = Grid(self.font, self.level)
                        self.grid.shuffle_grid()
                        self.state = PLAYING
                    elif name == "Menu":
                        self.state = MENU

    # -------------------------------------------------------------- draw
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.state == MENU:
            self._draw_menu(screen, mouse_pos)
        elif self.state == PLAYING:
            self._draw_playing(screen, mouse_pos)
        elif self.state == WIN:
            self._draw_win(screen, mouse_pos)

    def _draw_menu(self, screen, mouse_pos):
        title = self.title_font.render("SUNKEN TREASURE", True, GOLD)
        shadow = self.title_font.render("SUNKEN TREASURE", True, (0, 0, 0))
        screen.blit(shadow, shadow.get_rect(center=(302, 122)))
        screen.blit(title, title.get_rect(center=(300, 120)))
        sub = self.small.render("A Sliding Puzzle Adventure", True, TEAL)
        screen.blit(sub, sub.get_rect(center=(300, 160)))

        credit = self.small.render("Developed by Hannan Ashraf - Cyber Security Student", True, WHITE)
        screen.blit(credit, credit.get_rect(center=(300, 185)))

        label = self.font.render("Choose difficulty:", True, WHITE)
        screen.blit(label, (210, 265))

        for btn in self.menu_buttons.values():
            btn.update(mouse_pos)
            btn.draw(screen, self.font)

    def _draw_playing(self, screen, mouse_pos):
        self.grid.update(mouse_pos)
        self.grid.draw(screen)

        for btn in self.game_buttons.values():
            btn.update(mouse_pos)
            btn.draw(screen, self.small)

        stats = self.font.render(
            f"Time: {int(self.grid.elapsed)}s   |   Moves: {self.grid.strokes}   |   {self.level}",
            True, WHITE)
        screen.blit(stats, (30, 15))

    def _draw_win(self, screen, mouse_pos):
        img = pygame.transform.smoothscale(self.grid.full_image, (340, 340))
        rect = img.get_rect(center=(300, 260))
        pygame.draw.rect(screen, GOLD, rect.inflate(10, 10), 4, border_radius=10)
        screen.blit(img, rect)

        title = self.big_font.render("Treasure Found!", True, GOLD)
        shadow = self.big_font.render("Treasure Found!", True, (0, 0, 0))
        screen.blit(shadow, shadow.get_rect(center=(302, 452)))
        screen.blit(title, title.get_rect(center=(300, 450)))

        stats = self.font.render(
            f"{self.level}  •  {self.grid.strokes} moves  •  {int(self.grid.elapsed)}s",
            True, WHITE)
        screen.blit(stats, stats.get_rect(center=(300, 490)))

        if getattr(self.grid, "new_record", False):
            rec = self.small.render("★ New Best Score! ★", True, GOLD)
            screen.blit(rec, rec.get_rect(center=(300, 515)))

        for btn in self.win_buttons.values():
            btn.update(mouse_pos)
            btn.draw(screen, self.font)