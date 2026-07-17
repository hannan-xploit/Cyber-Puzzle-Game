import pygame
import random

class Particle:
    """Ek single particle ka logic (position, velocity, lifetime)."""
    def __init__(self, x, y, color, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity # pygame.math.Vector2
        self.lifetime = 1.0 # Seconds
        self.size = random.randint(2, 5)

    def update(self, dt):
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt
        self.lifetime -= dt
        self.size = max(0, self.size - dt * 5)

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class ParticleSystem:
    """Particles ka group jo explosions aur sparkles generate karta hai."""
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10):
        for _ in range(count):
            # Velocity random direction mein
            vel = pygame.math.Vector2(random.uniform(-100, 100), random.uniform(-100, 100))
            self.particles.append(Particle(x, y, color, vel))

    def update(self, dt):
        for p in self.particles[:]:
            p.update(dt)
            if p.lifetime <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)