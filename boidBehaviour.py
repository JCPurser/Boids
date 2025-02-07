import numpy as np

class BasicBehavior:
    """
    Base class for defining boid behaviors.
    """
    def __init__(self, vector_weights=[2.0, 1.0, 1.0]):
        """
        Sets the weights for the three behaviors: collision avoidance, velocity matching, and flock centering.
        """
        self.vector_weights = vector_weights

    def apply(self):
        """
        Each subclass should implement its own movement rules.
        """
        raise NotImplementedError
    
    def collision_avoidance(self, surrounding, location, min_distance=50):
        """
        Avoid collisions with other boids.
        """
        vector = np.zeros(2, dtype=np.float64)
        for boid in surrounding:
            distance = self.get_distance(location, boid)
            if 0 < distance < min_distance:
                vector += (location - boid.location) / (distance ** 2)
        return vector

    def flock_centering(self, surrounding, location, centering_weight=0.01):
        """
        Move towards the center of the flock.
        """
        if not surrounding:
            return np.zeros(2, dtype=np.float64)
        center_of_mass = np.mean([boid.location for boid in surrounding], axis=0)
        return (center_of_mass - location) * centering_weight

    def velocity_matching(self, surrounding, velocity, matching_weight=0.05):
        """
        Match the velocity of the surrounding boids.
        """
        if not surrounding:
            return np.zeros(2, dtype=np.float64)
        avg_velocity = np.mean([boid.velocity for boid in surrounding], axis=0)
        return (avg_velocity - velocity) * matching_weight

    def get_distance(self, location, boid):
        """
        Get the distance between this boid and another boid.
        """
        return np.linalg.norm(location - boid.location)

    def updateSurrounding(self, location, boids, radius=100):
        """
        Update the list of Boids surrounding this Boid.
        """
        return [boid for boid in boids if boid != self and self.get_distance(location, boid) < radius]

class FlockingBehavior(BasicBehavior):
    """
    Standard flocking behavior: cohesion, alignment, and separation.
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

class DirectionalBehavior(BasicBehavior):
    """
    Surrounding boids are only those within a certain angle of the boid's direction.
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
    
    def updateSurrounding(self, location, boids, radius=100):
        """
        Change this so that there is a restricted fov to 300 degrees and increased detection distance ahead proportional to speed.
        """
        return [boid for boid in boids if boid != self and self.get_distance(location, boid) < radius]