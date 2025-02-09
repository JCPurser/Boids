import numpy as np

class Boid:
    def __init__(self, coop=True, colour=(0, 255, 0), location=(0, 0), velocity=(0,0)):
        """
        Initialize a new Boid instance.
        """
        self.coop = coop
        self.colour = colour

        self.maxSpeed = 5.0
        self.vector_weights = [2.0, 1.0, 1.0]

        self.location = np.array(location, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)

        self.surrounding = []
        self.food = 0
        self.age = 0

    def update(self, boids, sky):
        """
        Update the state of the Boid using the flock's behavior.
        """
        self.updateSurrounding(boids)
        self.updateVelocity()
        self.updateLocation(sky)
        self.updateFood()
        self.updateAge()

    def updateSurrounding(self, boids):
        """
        Update the list of Boids surrounding this Boid.
        """
        raise NotImplementedError
    
    def updateVelocity(self):
        """
        Update the velocity of the Boid based on the flock's behavior.
        """
        raise NotImplementedError
    
    def updateLocation(self, sky):
        """
        Update the location of the Boid based on its current location and velocity.
        """
        raise NotImplementedError
    
    def updateFood(self):
        """
        Update the food level of the Boid.
        """
        raise NotImplementedError

    def updateAge(self):
        """
        Update the age of the Boid.
        """
        raise NotImplementedError
    
class BasicBoid(Boid):
    def apply(self):
        """
        Apply the three rules of flocking.
        """
        collision_avoidance = self.collision_avoidance()
        velocity_matching = self.velocity_matching()
        flock_centering = self.flock_centering()
        
        return (
            self.vector_weights[0] * collision_avoidance +
            self.vector_weights[1] * velocity_matching +
            self.vector_weights[2] * flock_centering
        )
    
    def collision_avoidance(self, min_distance=50):
        """
        Avoid collisions with other boids within the directional field of view.
        """
        vector = np.zeros(2, dtype=np.float64)
        for boid in self.surrounding:
            distance = np.linalg.norm(self.location - boid.location)
            if 0 < distance < min_distance:
                vector += (self.location - boid.location) / (distance ** 2)
        return vector

    def velocity_matching(self, matching_weight=0.05):
        """
        Match the velocity of the visible boids.
        """
        if not self.surrounding:
            return np.zeros(2, dtype=np.float64)
        avg_velocity = np.mean([boid.velocity for boid in self.surrounding], axis=0)
        return (avg_velocity - self.velocity) * matching_weight
    
    def flock_centering(self, centering_weight=0.01):
        """
        Move towards the center of the visible flock.
        """
        if not self.surrounding:
            return np.zeros(2, dtype=np.float64)
        center_of_mass = np.mean([boid.location for boid in self.surrounding], axis=0)
        return (center_of_mass - self.location) * centering_weight

    def updateLocation(self, sky):
        """
        Update the location of the Boid based on its current location and velocity.
        """ 
        self.location += self.velocity
        screen_width, screen_height = sky

        if not (0 <= self.location[0] <= screen_width): self.velocity[0] *= -1
        if not (0 <= self.location[1] <= screen_height): self.velocity[1] *= -1
    
    def updateVelocity(self):
        """
        Update the velocity of the Boid based on the flock's behavior.
        """
        self.velocity += self.apply()
        self.velocity = (self.velocity / (np.linalg.norm(self.velocity) + 0.0001)) * self.maxSpeed

    def updateSurrounding(self, boids, radius=100):
        """
        Update the list of Boids surrounding this Boid.
        """
        self.surrounding = [boid for boid in boids if boid != self and np.linalg.norm(self.location - boid.location) < radius]
    
    def updateFood(self):
        """
        Update the food level of the Boid.
        """
        self.food += np.random.randint(2)

    def updateAge(self):
        """
        Update the age of the Boid.
        """
        self.age += 1

class StationaryBoid(BasicBoid):
    """
    Non-flocking behaviour: Boids do not move.
    """
    def update(self, boids, sky):
        """
        Update the state of the Boid using the flock's behavior.
        """
        self.updateSurrounding(boids)
        self.updateLocation(sky)
        self.updateFood()
        self.updateAge()
    
class DirectionalBoid(BasicBoid):
    """
    Flocking behavior where awareness is limited to a forward-facing field of view.
    """
    def apply(self, base_view_distance=50, max_view_distance=200):
        """Apply flocking rules based only on boids in the directional field of view."""
        
        # Compute dynamic view distance based on speed
        speed = np.linalg.norm(self.velocity)
        view_distance = np.clip(base_view_distance + speed * 5, base_view_distance, max_view_distance)

        # Filter surrounding boids based on field of view
        self.filter_by_field_of_view(view_distance)
        
        # Apply standard flocking rules to filtered boids
        collision_avoidance = self.collision_avoidance()
        velocity_matching = self.velocity_matching()
        flock_centering = self.flock_centering()
        
        return (
            self.vector_weights[0] * collision_avoidance +
            self.vector_weights[1] * velocity_matching +
            self.vector_weights[2] * flock_centering
        )

    def filter_by_field_of_view(self, view_distance, field_of_view_angle= np.radians(150)):
        """
        Filters boids that are within the 300° field of view and dynamic range.
        """
        filtered_boids = []
        speed = np.linalg.norm(self.velocity)

        if speed == 0:
            velocity_direction = np.array([0.0, 1.0])  # Default direction (up)
        else:
            velocity_direction = self.velocity / speed

        for boid in self.surrounding:
            to_boid = boid.location - self.location
            distance = np.linalg.norm(to_boid)
            
            if 0 < distance < view_distance:
                to_boid_normalized = to_boid / distance
                dot_product = np.dot(velocity_direction, to_boid_normalized)

                # Angle between velocity direction and neighbor
                angle = np.arccos(np.clip(dot_product, -1.0, 1.0))

                if abs(angle) < field_of_view_angle:
                    filtered_boids.append(boid)

        self.surrounding = filtered_boids

class OmniscientBoid(BasicBoid):
    """
    Omniscient behaviour: Boids know the location of all other boids.
    """
    def updateSurrounding(self, boids):
        """
        Returns all boids.
        """
        self.surrounding = [boid for boid in boids if boid != self]

class MigratoryBoid(BasicBoid):
    """
    Migratory behaviour: Boids move towards a fixed location.
    """
    pass

class EvasiveBoid(BasicBoid):
    """
    Evasion behaviour: Boids attempt to avoid obstacles.
    """
    pass

class CooperativeBoid(BasicBoid):
    """
    Cooperative behaviour: Boids work together to reproduce.
    """
    def updateFood(self):
        """
        Update the food level of the Boid. With sharing.
        """
        food = np.random.randint(2)
        if self.coop and food:
            shared = False
            for boid in self.surrounding:
                if boid.coop and not shared:
                    boid.food += 0.5
                    food = 0.5
                    shared = True
        self.food += food