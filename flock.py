#!/usr/bin/env python3

from boid import Boid
import numpy as np

class Flock:
    def __init__(self, name, size=100, colour=(0, 255, 0), surface=None):
        """
        Initialize a flock of Boids.
        """
        self.name = name
        self.size = size
        self.colour = colour
        self.surface = surface

        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = 1300, 700
        
        locations = self.random_location(size)
        self.boids = [Boid(boid, self.name, colour=self.colour, location=locations[boid]) for boid in range(self.size)]

    def random_location(self, size):
        """
        Generate random locations for boids using a normal distribution around the screen center.
        """
        center_x, center_y = self.screen_width // 2, self.screen_height // 2
        std_dev_x, std_dev_y = self.screen_width // 8, self.screen_height // 8
        locations = np.random.normal(loc=[center_x, center_y], scale=[std_dev_x, std_dev_y], size=(size, 2))
        locations = np.clip(locations, [0, 0], [self.screen_width, self.screen_height])
        return locations.tolist()
    
    def update(self, boids):
        """
        Update the state of the flock.
        """
        for boid in self.boids:
            boid.update(boids, self.surface)

    def updateSurroundings(self, boids):
        """
        Update the surroundings of each boid in the flock.
        """
        for boid in self.boids:
            boid.updateSurrounding(boids)

    def draw(self, surface):
        """
        Draw the flock to the provided drawing surface.
        """
        for boid in self.boids:
            boid.draw(surface)