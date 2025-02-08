from boid import Boid
import numpy as np
from boidBehaviour import FlockingBehaviour, DirectionalFlocking, StationaryBehaviour, OmniscientFlocking, MigratoryFlocking, EvasionFlocking, CooperativeFlocking

"""
Behavior map for flocking behaviors. Vector weights can be set here
"""
BEHAVIOUR_MAP = {
    "flocking": FlockingBehaviour,
    "directional":  DirectionalFlocking,
    "stationary": StationaryBehaviour,
    "omniscient":   OmniscientFlocking,
    "migratory": MigratoryFlocking,
    "evasion": EvasionFlocking,
    "cooperative": CooperativeFlocking
}
class Flock:
    def __init__(self, sky, coop=0.5, size=100, colour=(0, 255, 0), behaviour="directional", interFlocking=True, hmd=True):
        """
        Initialize a flock of Boids.
        """
        self.interFlocking = interFlocking
        self.hmd = hmd #Hatches and Dispatches working, Matches to be implemented.

        self.behaviour = BEHAVIOUR_MAP.get(behaviour, BEHAVIOUR_MAP["flocking"])()
        locations = self.random_location(sky, size)
        num_cooperative = int(coop * size)
        
        self.boids = []
        for boid in range(size):
            if boid < num_cooperative:
                self.boids.append(Boid(coop=True, colour=colour, location=locations[boid]))
            else:
                self.boids.append(Boid(coop=False, colour=colour, location=locations[boid]))

    def random_location(self, sky, size):
        """
        Generate random locations for boids using a normal distribution around the screen center.
        """
        screen_width, screen_height = sky
        center_x, center_y = screen_width // 2, screen_height // 2
        std_dev_x, std_dev_y = screen_width // 8, screen_height // 8
        locations = np.random.normal(loc=[center_x, center_y], scale=[std_dev_x, std_dev_y], size=(size, 2))
        locations = np.clip(locations, [0, 0], [screen_width, screen_height])
        return locations.tolist()
    
    def update(self, boids, sky):
        """
        Update the state of the flock.
        """
        for boid in self.boids:
            
            if boid.food > 100 and self.hmd:
                self.boids.append(Boid(boid.coop, colour=(0,0,255), location=boid.location, velocity=boid.velocity))
                boid.food = 0
            
            if boid.age > 300 and self.hmd:
                self.boids.remove(boid)
            
            if self.interFlocking:
                    boid.update(self.behaviour, boids, sky)
            else:
                    boid.update(self.behaviour, self.boids, sky)

    def draw(self, surface):
        """
        Draw the flock to the provided drawing surface.
        """
        for boid in self.boids:
            self.behaviour.draw(boid, surface)

    def adjust_speed(self, amount):
            """
            Increase or decrease the speed of all boids in the flock.
            """
            self.behaviour.maxSpeed += amount

    def set_behaviour(self, behaviour):
        """
        Change behavior for the entire flock dynamically.
        """
        if behaviour in BEHAVIOUR_MAP:
            self.behaviour = BEHAVIOUR_MAP[behaviour]()

    def toggle_interflocking(self):
        """
        Toggle inter-flocking behavior.
        """
        self.interFlocking = not self.interFlocking