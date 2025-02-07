from boid import Boid
import numpy as np
from boidBehaviour import FlockingBehaviour, DirectionalFlocking, StationaryBehaviour, OmniscientFlocking

"""
Behavior map for flocking behaviors. Vector weights can be set here
"""
BEHAVIOUR_MAP = {
    "flocking": FlockingBehaviour,
    "directional":  DirectionalFlocking,
    "stationary": StationaryBehaviour,
    "omniscient":   OmniscientFlocking,
}
class Flock:
    def __init__(self, name, surface, size=100, colour=(0, 255, 0), behaviour="flocking", interFlocking=True):
        """
        Initialize a flock of Boids.
        """
        self.name = name
        self.size = size
        self.colour = colour
        self.surface = surface
        self.behaviour = BEHAVIOUR_MAP.get(behaviour, BEHAVIOUR_MAP["flocking"])()
        self.interFlocking = interFlocking

        locations = self.random_location()
        self.boids = [Boid(boid, self.name, self.surface, colour=self.colour, location=locations[boid]) for boid in range(self.size)]

    def set_behaviour(self, behaviour):
        """
        Change behavior for the entire flock dynamically.
        """
        if behaviour in BEHAVIOUR_MAP:
            self.behaviour = BEHAVIOUR_MAP[behaviour]()

    def random_location(self):
        """
        Generate random locations for boids using a normal distribution around the screen center.
        """
        screen_width, screen_height = self.surface.get_size()
        center_x, center_y = screen_width // 2, screen_height // 2
        std_dev_x, std_dev_y = screen_width // 8, screen_height // 8
        locations = np.random.normal(loc=[center_x, center_y], scale=[std_dev_x, std_dev_y], size=(self.size, 2))
        locations = np.clip(locations, [0, 0], [screen_width, screen_height])
        return locations.tolist()
    
    def update(self, boids):
        """
        Update the state of the flock.
        """
        if self.interFlocking:
            for boid in self.boids:
                boid.update(self.behaviour, boids)
        else:
            for boid in self.boids:
                boid.update(self.behaviour, self.boids)

    def draw(self):
        """
        Draw the flock to the provided drawing surface.
        """
        for boid in self.boids:
            boid.draw()

    def adjust_speed(self, amount):
            """
            Increase or decrease the speed of all boids in the flock.
            """
            self.behaviour.maxSpeed += amount