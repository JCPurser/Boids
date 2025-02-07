import pygame
import numpy as np

class Boid:
    def __init__(self, name, flock, surface, cooperation, colour=(0, 255, 0), location=(0, 0), velocity=(0,0)):
        """
        Initialize a new Boid instance.
        """
        self.name = name
        self.flock = flock
        self.surface = surface
        self.cooperation = cooperation

        self.colour = colour
        self.location = np.array(location, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

        self.surrounding = []

    def update(self, behaviour, boids):
        """
        Update the state of the Boid using the flock's behavior.
        """
        self.surrounding = behaviour.updateSurrounding(self.location, boids)
        self.updateLocation()
        self.updateVelocity(behaviour)

    def updateLocation(self):
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

    def draw(self):
        """
        Draw the Boid oriented according to its velocity.
        """
        angle = np.arctan2(self.velocity[1], self.velocity[0])

        length = 10
        points = np.array([
            [length, 0],
            [-length * 0.5, length * 0.5],
            [-length * 0.5, -length * 0.5]
        ])

        # Rotate points
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        rotated_points = np.dot(points, rotation_matrix.T)

        # Translate to boid's position
        translated_points = rotated_points + self.location
        pygame.draw.polygon(self.surface, self.colour, translated_points.astype(int))