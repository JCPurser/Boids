import numpy as np

class BasicBehavior:
    """Base class for defining boid behaviors."""

    def __init__(self, vector_weights=[2.0, 1.0, 1.0]):
        self.vector_weights = vector_weights

    def apply(self):
        """Each subclass should implement its own movement rules."""
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

class FlockingBehavior(BasicBehavior):
    """Standard flocking behavior: cohesion, alignment, and separation."""
    def apply(self, surrounding, location, velocity):
        collision_avoidance = self.collision_avoidance(surrounding, location)
        velocity_matching = self.velocity_matching(surrounding, velocity)
        flock_centering = self.flock_centering(surrounding, location)
        
        return (
            self.vector_weights[0] * collision_avoidance +
            self.vector_weights[1] * velocity_matching +
            self.vector_weights[2] * flock_centering
        )

class ChaoticBehavior(BasicBehavior):
    """Chaotic movement: randomized movement in all directions."""
    def apply(self, boid):
        return np.random.uniform(-1, 1, 2) * 3  # More erratic movement

class SwarmingBehavior(BasicBehavior):
    """Boids aggressively move toward nearby boids (strong cohesion)."""
    def apply(self, boid):
        return boid.flock_centering() * 2.0  # Amplify cohesion force

class AvoidantBehavior(BasicBehavior):
    """Boids strongly avoid others, leading to more dispersed movement."""
    def apply(self, boid):
        return boid.collision_avoidance() * 3.0  # Amplify avoidance force

class CuriousBehavior(BasicBehavior):
    """Boids seek out other groups instead of avoiding them."""
    def apply(self, boid):
        return -boid.collision_avoidance() * 1.5  # Inverse avoidance for curiosity
