import pygame
import numpy as np

class Boid:
    def __init__(self, surface, cooperation, colour=(0, 255, 0), location=(0, 0), velocity=(0,0)):
        """
        Initialize a new Boid instance.
        """
        self.surface = surface
        self.cooperation = cooperation

        self.colour = colour
        self.location = np.array(location, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

        self.surrounding = []
        self.reproduction = 0
        self.age = 0

    def update(self, behaviour, boids):
        """
        Update the state of the Boid using the flock's behavior.
        """
        self.reproduction += 1
        self.age += 1

        self.surrounding = behaviour.updateSurrounding(self.location, boids)
        self.updateLocation()
        self.updateVelocity(behaviour)

    def updateLocation(self, behaviour):
        """
        Update the location of the Boid based on its current location and velocity.
        """ 
        self.location += self.velocity

        screen_width, screen_height = self.surface.get_size()

        # Reflect velocity if hitting walls
        if not (0 <= self.location[0] <= screen_width):
            self.velocity[0] *= -1
        if not (0 <= self.location[1] <= screen_height):
            self.velocity[1] *= -1
    
    def updateVelocity(self, behaviour):
        """
        Update the velocity of the Boid based on the flock's behavior.
        """
        self.velocity += behaviour.apply(self.surrounding, self.location, self.velocity)
        self.velocity = self.normaliseVelocity(behaviour)
    
    def normaliseVelocity(self, behaviour):
        """
        Normalize a velocity vector to a fixed speed.
        """
        magnitude = np.linalg.norm(self.velocity)
        if magnitude == 0:  # Prevent division by zero
            return np.zeros(2, dtype=np.float64)
        return (self.velocity / magnitude) * behaviour.maxSpeed