from boid import BasicBoid, DirectionalBoid, StationaryBoid, OmniscientBoid, MigratoryBoid, EvasiveBoid, CooperativeBoid, StationaryCoop, RandomCoop
import numpy as np

"""
Behavior map for flocking behaviors.
"""
BOID_MAP = {
    "basic": BasicBoid,
    "directional": DirectionalBoid,
    "stationary": StationaryCoop,
    "omniscient": OmniscientBoid,
    "migratory": MigratoryBoid,
    "evasive": EvasiveBoid,
    "cooperative": CooperativeBoid,
    "random": RandomCoop
}
class Flock:
    def __init__(self, sky=(1000,1000), coop=0.5, size=100, colour=(0, 255, 0), boid_type="basic"):
        """
        Initialize a flock of Boids.
        """
        self.interFlocking = False
        self.life_cycle = True
        self.boid_type = boid_type

        locations = self.random_location(sky, size)
        
        self.boids = []
        num_cooperative = int(coop * size)
        for boid in range(size):
            if boid < num_cooperative:
                self.boids.append(BOID_MAP.get(boid_type, BOID_MAP["basic"])(coop=True, colour=colour, location=locations[boid]))
            else:
                self.boids.append(BOID_MAP.get(boid_type, BOID_MAP["basic"])(coop=False, colour=colour, location=locations[boid]))

    def update(self, boids, sky):
        """
        Update the state of the flock.
        """
        for boid in self.boids:             
            if self.interFlocking: boid.update(boids, sky)
            else: boid.update(self.boids, sky)

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

    def adjust_speed(self, amount):
            """
            Increase or decrease the speed of all boids in the flock.
            """
            for boid in self.boids:
                boid.maxSpeed += amount

    def toggle_interflocking(self):
        """
        Toggle inter-flocking behavior.
        """
        self.interFlocking = not self.interFlocking