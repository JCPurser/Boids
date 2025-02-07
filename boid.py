#!/usr/bin/env python3

import pygame
import numpy as np

class Boid:
    def __init__(self, name, flock, location=(0, 0), colour=(0, 255, 0)):
        """
        Initialize a new Boid instance.
        """
        self.name = name
        self.flock = flock
        self.location = np.array(location, dtype=np.float64)
        self.colour = colour
        self.velocity = np.zeros(2, dtype=np.float64)
        self.surrounding = []
    
    def update(self, boids, surface):
        """
        Update the state of the Boid.
        """
        self.updateSurrounding(boids)
        self.updateLocation(surface)
        self.updateVelocity()
        
    def updateLocation(self, surface=None):
        """
        Update the location of the Boid based on its current location and velocity.
        """ 
        self.location += self.velocity

        if surface:
            screen_width, screen_height = surface.get_size()
        else:
            screen_width, screen_height = 1300, 700

        # Reflect velocity if hitting walls
        if not (0 <= self.location[0] <= screen_width):
            self.velocity[0] *= -1
        if not (0 <= self.location[1] <= screen_height):
            self.velocity[1] *= -1
    
    def updateVelocity(self, vectorWeights=[2.0, 1.0, 1.0]):
        """
        Update the velocity of the Boid based on surrounding Boids.
        """
        collisionAvoidanceVector = self.collision_avoidance()
        velocityMatchingVector = self.velocity_matching()
        flockCenteringVector = self.flock_centering()

        self.velocity += (
            vectorWeights[0] * collisionAvoidanceVector +
            vectorWeights[1] * velocityMatchingVector +
            vectorWeights[2] * flockCenteringVector
        )

        self.velocity = self.normalise(self.velocity)

    def updateSurrounding(self, boids, radius=100):
        """
        Update the list of Boids surrounding this Boid.
        """
        self.surrounding = [boid for boid in boids if boid != self and self.get_distance(boid) < radius]
   
    def collision_avoidance(self, min_distance=50):
        """
        Avoid collisions with other boids.
        """
        vector = np.zeros(2, dtype=np.float64)
        for boid in self.surrounding:
            distance = self.get_distance(boid)
            if 0 < distance < min_distance:
                vector += (self.location - boid.location) / (distance ** 2)
        return vector

    def flock_centering(self, centering_weight=0.01):
        """
        Move towards the center of the flock.
        """
        if not self.surrounding:
            return np.zeros(2, dtype=np.float64)
        center_of_mass = np.mean([boid.location for boid in self.surrounding], axis=0)
        return (center_of_mass - self.location) * centering_weight

    def velocity_matching(self, matching_weight=0.05):
        """
        Match the velocity of the surrounding boids.
        """
        if not self.surrounding:
            return np.zeros(2, dtype=np.float64)
        avg_velocity = np.mean([boid.velocity for boid in self.surrounding], axis=0)
        return (avg_velocity - self.velocity) * matching_weight
    
    def normalise(self, vector, max_speed=5.0):
        """
        Normalize a velocity vector to a fixed speed.
        """
        magnitude = np.linalg.norm(vector)
        if magnitude == 0:  # Prevent division by zero
            return np.zeros(2, dtype=np.float64)
        return (vector / magnitude) * max_speed
  
    def get_distance(self, boid):
        """
        Get the distance between this boid and another boid.
        """
        return np.linalg.norm(self.location - boid.location)

    def draw(self, surface):
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
        pygame.draw.polygon(surface, self.colour, translated_points.astype(int))