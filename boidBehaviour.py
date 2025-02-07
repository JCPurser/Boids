import numpy as np
import pygame
class BasicBehaviour:
    """
    Base class for defining boid behaviours.
    """
    def __init__(self, vector_weights=[2.0, 1.0, 1.0]):
        """
        Sets the weights for the three behaviours: collision avoidance, velocity matching, and flock centering.
        """
        self.vector_weights = vector_weights
        self.maxSpeed = 5.0

    def apply(self):
        """
        Each subclass should implement its own movement rules.
        """
        raise NotImplementedError
    
    def collision_avoidance(self, surrounding, location, min_distance=50):
        """Avoid collisions with other boids within the directional field of view."""
        vector = np.zeros(2, dtype=np.float64)
        for boid in surrounding:
            distance = np.linalg.norm(location - boid.location)
            if 0 < distance < min_distance:
                vector += (location - boid.location) / (distance ** 2)
        return vector

    def velocity_matching(self, surrounding, velocity, matching_weight=0.05):
        """Match the velocity of the visible boids."""
        if not surrounding:
            return np.zeros(2, dtype=np.float64)
        avg_velocity = np.mean([boid.velocity for boid in surrounding], axis=0)
        return (avg_velocity - velocity) * matching_weight
    
    def flock_centering(self, surrounding, location, centering_weight=0.01):
        """Move towards the center of the visible flock."""
        if not surrounding:
            return np.zeros(2, dtype=np.float64)
        center_of_mass = np.mean([boid.location for boid in surrounding], axis=0)
        return (center_of_mass - location) * centering_weight

    def draw(self, boid, surface):
        """
        Draw the Boid oriented according to its velocity.
        """
        angle = np.arctan2(boid.velocity[1], boid.velocity[0])

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
        translated_points = rotated_points + boid.location
        pygame.draw.polygon(surface, boid.colour, translated_points.astype(int))

    def updateLocation(self, location, velocity, sky):
        """
        Update the location of the Boid based on its current location and velocity.
        """ 
        location += velocity

        screen_width, screen_height = sky

        # Reflect velocity if hitting walls
        if not (0 <= location[0] <= screen_width):
            velocity[0] *= -1
        if not (0 <= location[1] <= screen_height):
            velocity[1] *= -1

        return location, velocity
    
    def updateVelocity(self, surrounding, location, velocity):
        """
        Update the velocity of the Boid based on the flock's behavior.
        """
        velocity += self.apply(surrounding, location, velocity)
        velocity = self.normaliseVelocity(velocity, self.maxSpeed)

        return velocity
    
    def normaliseVelocity(self, vector, scalingFactor=1.0):
        """
        Normalize a velocity vector to a fixed speed.
        """
        magnitude = np.linalg.norm(vector)
        if magnitude == 0:
            return np.zeros(2, dtype=np.float64)
        return (vector / magnitude) * scalingFactor

    def updateSurrounding(self, location, boids, radius=100):
        """
        Update the list of Boids surrounding this Boid.
        """
        return [boid for boid in boids if boid != self and np.linalg.norm(location - boid.location) < radius]
    
    def updateFood(self, surrounding):
        """
        Update the food level of the Boid.
        """
        
        return np.random.randint(2)

class FlockingBehaviour(BasicBehaviour):
    """
    Standard flocking behaviour: cohesion, alignment, and separation.
    """
    def apply(self, surrounding, location, velocity):
        """
        Apply the three rules of flocking.
        """
        collision_avoidance = self.collision_avoidance(surrounding, location)
        velocity_matching = self.velocity_matching(surrounding, velocity)
        flock_centering = self.flock_centering(surrounding, location)
        
        return (
            self.vector_weights[0] * collision_avoidance +
            self.vector_weights[1] * velocity_matching +
            self.vector_weights[2] * flock_centering
        )

class DirectionalFlocking(FlockingBehaviour):
    """
    Flocking behavior where awareness is limited to a forward-facing field of view.
    """
    def apply(self, surrounding, location, velocity, base_view_distance=50, max_view_distance=200):
        """Apply flocking rules based only on boids in the directional field of view."""
        
        # Compute dynamic view distance based on speed
        speed = np.linalg.norm(velocity)
        view_distance = np.clip(base_view_distance + speed * 5, base_view_distance, max_view_distance)

        # Filter surrounding boids based on field of view
        filtered_boids = self.filter_by_field_of_view(surrounding, location, velocity, view_distance)
        
        # Apply standard flocking rules to filtered boids
        collision_avoidance = self.collision_avoidance(filtered_boids, location)
        velocity_matching = self.velocity_matching(filtered_boids, velocity)
        flock_centering = self.flock_centering(filtered_boids, location)
        
        return (
            self.vector_weights[0] * collision_avoidance +
            self.vector_weights[1] * velocity_matching +
            self.vector_weights[2] * flock_centering
        )

    def filter_by_field_of_view(self, surrounding, location, velocity, view_distance, field_of_view_angle= np.radians(150)):
        """
        Filters boids that are within the 300° field of view and dynamic range.
        """
        filtered_boids = []
        speed = np.linalg.norm(velocity)

        if speed == 0:
            velocity_direction = np.array([0.0, 1.0])  # Default direction (up)
        else:
            velocity_direction = velocity / speed

        for boid in surrounding:
            to_boid = boid.location - location
            distance = np.linalg.norm(to_boid)
            
            if 0 < distance < view_distance:
                to_boid_normalized = to_boid / distance
                dot_product = np.dot(velocity_direction, to_boid_normalized)

                # Angle between velocity direction and neighbor
                angle = np.arccos(np.clip(dot_product, -1.0, 1.0))

                if abs(angle) < field_of_view_angle:
                    filtered_boids.append(boid)

        return filtered_boids
    
class StationaryBehaviour(BasicBehaviour):
    """
    Non-flocking behaviour: Boids do not move.
    """
    def apply(self, surrounding, location, velocity):
        """
        Returns an empty vector.
        """
        return velocity * -1

class OmniscientFlocking(FlockingBehaviour):
    """
    Omniscient behaviour: Boids know the location of all other boids.
    """
    def updateSurrounding(self, location, boids):
        """
        Returns all boids.
        """
        return [boid for boid in boids if boid != self]

class MigratoryFlocking(FlockingBehaviour):
    """
    Migratory behaviour: Boids move towards a fixed location.
    """
    pass

class EvasionFlocking(FlockingBehaviour):
    """
    Evasion behaviour: Boids attempt to avoid obstacles.
    """
    pass

class CooperativeFlocking(FlockingBehaviour):
    """
    Cooperative behaviour: Boids work together to reproduce.
    """
    def draw(self, boid, surface):
        """
        Draw the Boid oriented according to its velocity.
        """
        angle = np.arctan2(boid.velocity[1], boid.velocity[0])

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

        if boid.coop:
            colour = (0, 255, 0)
        else:
            colour = (255, 0, 0)

        # Translate to boid's position
        translated_points = rotated_points + boid.location
        pygame.draw.polygon(surface, colour, translated_points.astype(int))

    def updateFood(self, surrounding):
        """
        Update the food level of the Boid. With sharing.
        """
        return np.random.randint(2)
