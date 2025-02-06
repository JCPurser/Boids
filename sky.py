#!/usr/bin/env python3

import pygame
from flock import Flock

class Sky:
    def __init__(self, flocks=1, width=1300, height=700):
        """
        Initialize a new Sky instance with flocks.
        """
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boids Simulation")
        self.clock = pygame.time.Clock()
        
        self.flocks = [Flock(flock, surface=self.surface) for flock in range(flocks)]
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
            flock.draw(self.surface)
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