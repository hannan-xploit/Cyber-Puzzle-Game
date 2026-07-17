import pygame, random, math


class Bubble:
    """A slow rising background bubble - gives the 'underwater adventure' feel."""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.reset(first=True)

    def reset(self, first=False):
        self.x = random.randint(0, self.w)
        self.y = random.randint(0, self.h) if first else self.h + random.randint(10, 60)
        self.r = random.randint(2, 7)
        self.speed = random.uniform(0.4, 1.6)
        self.wobble = random.uniform(0, math.pi * 2)
        self.alpha = random.randint(60, 150)

    def update(self):
        self.y -= self.speed
        self.wobble += 0.05
        self.x += math.sin(self.wobble) * 0.6
        if self.y < -10:
            self.reset()

    def draw(self, screen):
        s = pygame.Surface((self.r * 2 + 4, self.r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(s, (200, 240, 255, self.alpha), (self.r + 2, self.r + 2), self.r, 1)
        screen.blit(s, (self.x - self.r - 2, self.y - self.r - 2))


class Spark:
    """Small burst particle used when a tile snaps into its correct spot."""
    def __init__(self, x, y):
        self.x, self.y = x, y
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.5)
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
        self.life = 26
        self.max_life = self.life
        self.color = random.choice([(255, 221, 87), (255, 255, 255), (120, 220, 255)])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08
        self.life -= 1

    def dead(self):
        return self.life <= 0

    def draw(self, screen):
        if self.life <= 0:
            return
        alpha = max(0, int(255 * (self.life / self.max_life)))
        r = max(1, int(4 * (self.life / self.max_life)))
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (r, r), r)
        screen.blit(s, (self.x - r, self.y - r))


class Confetti:
    """Celebration particle for the win screen - gold coin / gem style."""
    def __init__(self, w):
        self.x = random.randint(0, w)
        self.y = random.randint(-400, -10)
        self.speed = random.uniform(2, 5)
        self.size = random.randint(4, 9)
        self.color = random.choice([(255, 215, 80), (255, 235, 140), (220, 60, 90),
                                     (60, 180, 220), (255, 255, 255)])
        self.spin = random.uniform(0, 360)
        self.spin_speed = random.uniform(-6, 6)
        self.sway = random.uniform(0, math.pi * 2)

    def update(self, h):
        self.y += self.speed
        self.sway += 0.08
        self.x += math.sin(self.sway) * 1.2
        self.spin += self.spin_speed
        if self.y > h + 20:
            self.y = random.randint(-40, -10)
            self.x = random.randint(0, 600)

    def draw(self, screen):
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.size * 2, self.size))
        rotated = pygame.transform.rotate(surf, self.spin)
        screen.blit(rotated, (self.x, self.y))
