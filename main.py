import pygame, sys, random, math
from engine.scene_manager import SceneManager, WIN
from game.effects import Bubble, Confetti

WIDTH, HEIGHT = 600, 650


class Fish:
    COLORS = [(0, 255, 255), (255, 160, 60), (255, 210, 90), (120, 200, 255)]

    def __init__(self):
        self.pos = [random.randint(0, WIDTH), random.randint(80, HEIGHT - 40)]
        self.vel = [random.uniform(0.5, 2), 0]
        self.size = random.randint(2, 4)
        self.color = random.choice(self.COLORS)
        self.bob = random.uniform(0, math.pi * 2)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0] %= WIDTH
        self.bob += 0.05
        self.pos[1] += math.sin(self.bob) * 0.3

    def draw(self, screen):
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(screen, self.color, (x, y), self.size)
        tail_dir = -1 if self.vel[0] > 0 else 1
        pygame.draw.polygon(screen, self.color, [
            (x + tail_dir * self.size, y),
            (x + tail_dir * (self.size + 4), y - 3),
            (x + tail_dir * (self.size + 4), y + 3),
        ])


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sunken Treasure - Puzzle Adventure")
        self.clock = pygame.time.Clock()

        font = pygame.font.SysFont("Arial", 24, bold=True)
        self.manager = SceneManager(font)

        self.fishes = [Fish() for _ in range(10)]
        self.bubbles = [Bubble(WIDTH, HEIGHT) for _ in range(22)]
        self.confetti = [Confetti(WIDTH) for _ in range(40)]

    # ------------------------------------------------------------ bg
    def draw_ocean_background(self):
        top = (8, 40, 75)
        bottom = (2, 10, 25)
        for y in range(0, HEIGHT, 4):
            t = y / HEIGHT
            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, WIDTH, 4))

        for b in self.bubbles:
            b.update()
            b.draw(self.screen)

        for f in self.fishes:
            f.update()
            f.draw(self.screen)

    # ------------------------------------------------------------ loop
    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.manager.handle_event(event)

            self.draw_ocean_background()

            if self.manager.state == WIN:
                for c in self.confetti:
                    c.update(HEIGHT)
                    c.draw(self.screen)

            self.manager.draw(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
