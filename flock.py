#!/usr/bin/env python3

from boid import Boid
import numpy as np

class Flock:
    def __init__(self, name, surface, size=100, colour=(0, 255, 0), behaviour="flocking"):
        """
        Initialize a flock of Boids.
        """
        self.name = name
        self.size = size
        self.colour = colour
        self.surface = surface
        
        locations = self.random_location()
        self.boids = [Boid(boid, self.name, self.surface, colour=self.colour, location=locations[boid], behaviour=behaviour) for boid in range(self.size)]

    def random_location(self):
        """
        Generate random locations for boids using a normal distribution around the screen center.
        """
        screen_width, screen_height = self.surface.get_size()
        center_x, center_y = screen_width // 2, screen_height // 2
        std_dev_x, std_dev_y = screen_width // 8, screen_height // 8
        locations = np.random.normal(loc=[center_x, center_y], scale=[std_dev_x, std_dev_y], size=(self.size, 2))
        locations = np.clip(locations, [0, 0], [screen_width, screen_height])
        return locations.tolist()
    
    def update(self, boids):
        """
        Update the state of the flock.
        """
        for boid in self.boids:
            boid.update(boids)

    def updateSurroundings(self, boids):
        """
        Update the surroundings of each boid in the flock.
        """
        for boid in self.boids:
            boid.updateSurrounding(boids)

    def draw(self):
        """
        Draw the flock to the provided drawing surface.
        """
        for boid in self.boids:
            boid.draw()