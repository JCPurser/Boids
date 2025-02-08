import pygame
import numpy as np

class Boid:
    def __init__(self, coop=True, colour=(0, 255, 0), location=(0, 0), velocity=(0,0)):
        """
        Initialize a new Boid instance.
        """
        self.coop = coop

        self.colour = colour
        self.location = np.array(location, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

        self.surrounding = []
        self.food = 0
        self.age = 0

    def update(self, behaviour, boids, sky):
        """
        Update the state of the Boid using the flock's behavior.
        """
        self.age += 1

        self.surrounding = behaviour.updateSurrounding(self.location, boids)
        self.velocity = behaviour.updateVelocity(self.surrounding, self.location, self.velocity)
        self.location, self.velocity = behaviour.updateLocation(self.location, self.velocity, sky)
        self.food += behaviour.updateFood(self.surrounding)