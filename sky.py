#!/usr/bin/env python3

import pygame
from flock import Flock

class Sky:
    def __init__(self):
        """
        Initialize a new Sky instance with flocks.
        """
        pygame.init()
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Boids Simulation")
        self.clock = pygame.time.Clock()
        
        self.flocks = []
        self.flocks.append(Flock(0, size=50, surface=self.surface, colour=(0, 255, 0), behaviour="flocking"))
        self.flocks.append(Flock(1, size=50, surface=self.surface, colour=(255, 0, 0), behaviour="flocking"))

        self.boids = [boid for flock in self.flocks for boid in flock.boids]

    def update(self):
        """
        Update each flock in the sky.
        """
        for flock in self.flocks:
            flock.update(self.boids)

    def draw(self):
        """
        Clear the screen and draw each flock.
        """
        self.surface.fill((255, 255, 255))
        for flock in self.flocks:
            flock.draw()
        pygame.display.flip()

    def run_simulation(self, fps=30):
        """
        Runs the simulation until the user closes the window or presses 'E'.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    running = False
            self.update()
            self.draw()
            self.clock.tick(fps)
        pygame.quit()

"""
Creates an instance of Sky and runs the simulation.
"""
if __name__ == "__main__":
    sky = Sky()
    sky.run_simulation()