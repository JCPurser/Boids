#!/usr/bin/env python3

import pygame
import numpy as np
from boidBehaviour import FlockingBehaviour, DirectionalBehaviour, NonFlockingBehaviour

BEHAVIOUR_MAP = {
    "flocking": FlockingBehaviour,
    "directional": DirectionalBehaviour,
    "non-flocking": NonFlockingBehaviour
}

class Boid:
    def __init__(self, name, flock, surface, colour=(0, 255, 0), location=(0, 0), velocity=(0,0), maxSpeed=5.0, behaviour="flocking"):
        """
        Initialize a new Boid instance.
        """
        self.name = name
        self.flock = flock
        self.surface = surface

        self.colour = colour

        self.location = np.array(location, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

        self.maxSpeed = maxSpeed

        self.behaviour = BEHAVIOUR_MAP.get(behaviour, FlockingBehaviour)()

        self.surrounding = []

    def update(self, boids):
        """
        Update the state of the Boid.
        """
        self.surrounding = self.behaviour.updateSurrounding(self.location, boids)
        self.updateLocation()
        self.updateVelocity()
        
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
    
    def updateVelocity(self):
        """
        Update the velocity of the Boid based on surrounding Boids.
        """
        self.velocity += self.behaviour.apply(self.surrounding, self.location, self.velocity)
        self.velocity = self.normalise(self.velocity)
    
    def normalise(self, vector):
        """
        Normalize a velocity vector to a fixed speed.
        """
        magnitude = np.linalg.norm(vector)
        if magnitude == 0:  # Prevent division by zero
            return np.zeros(2, dtype=np.float64)
        return (vector / magnitude) * self.maxSpeed
  
    def get_distance(self, boid):
        """
        Get the distance between this boid and another boid.
        """
        return np.linalg.norm(self.location - boid.location)

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