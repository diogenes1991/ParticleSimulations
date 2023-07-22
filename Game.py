import pygame
import sys
import random
import math

# Pygame setup
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Particle Simulation on a Torus")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Particle class
class Particle:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.x %= screen_width
        self.y %= screen_height

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 3)

# Function to create random particles on the torus
def create_particles(num_particles):
    particles = []
    for _ in range(num_particles):
        x = random.uniform(0, screen_width)
        y = random.uniform(0, screen_height)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        particles.append(Particle(x, y, angle, speed))
    return particles

# Function to calculate the distance between two particles on the torus
def torus_distance(p1, p2):
    dx = abs(p1.x - p2.x)
    dy = abs(p1.y - p2.y)
    dx = min(dx, screen_width - dx)
    dy = min(dy, screen_height - dy)
    return math.sqrt(dx**2 + dy**2)

# Main function
def main():
    num_particles = 100
    particles = create_particles(num_particles)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        for particle in particles:
            particle.move()
            particle.draw()

        # Apply interactions between particles
        for i in range(num_particles):
            for j in range(i + 1, num_particles):
                distance = torus_distance(particles[i], particles[j])
                if distance < 50:  # You can adjust this distance threshold to control interaction range
                    # Some interaction logic can be applied here if needed
                    pass

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()