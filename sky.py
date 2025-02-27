#!/usr/bin/env python3

import pygame
from flock import Flock
import numpy as np
import matplotlib.pyplot as plt
class Sky:
    def __init__(self, render=True):
        """
        Initialize a new Sky instance with flocks.
        """
        self.render = render
        self.steps = 200
        self.history = []
        if render:
            pygame.init()
            self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.set_caption("Boids Simulation")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 24)

        self.flocks = []
        self.flocks.append(Flock(coop=0.5, size=50, colour=(0, 255, 0), boid_type="random"))

        self.drawCoop = True

        self.boids = [boid for flock in self.flocks for boid in flock.boids]       

    def update(self):
        """
        Update each flock in the sky.
        """
        if self.render:
            for flock in self.flocks:
                flock.update(self.boids, self.surface.get_size())
        else:
            for flock in self.flocks:
                flock.update(self.boids, (1000, 1000))

        self.boids = [boid for flock in self.flocks for boid in flock.boids]

    def draw(self):
        """
        Clear the screen and draw each flock along with UI data.
        """
        self.surface.fill((255, 255, 255))

        for boid in self.boids:
            self.draw_boid(boid)
        
        self.draw_ui()

        pygame.display.flip()

    def draw_boid(self, boid):
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

        if self.drawCoop:
            if boid.coop:
                colour = (0, 255, 0)
            else:
                colour = (255, 0, 0)
        else:
            colour = boid.colour

        # Translate to boid's position
        translated_points = rotated_points + boid.location
        pygame.draw.polygon(self.surface, colour, translated_points.astype(int))

    def draw_ui(self):
        """
        Draw real-time flock statistics on the screen.
        """
        y_offset = 10
        for i, flock in enumerate(self.flocks):
            if len(flock.boids) != 0:
                avg_speed = sum(np.linalg.norm(boid.velocity) for boid in flock.boids) / len(flock.boids)
                text = f"Flock {i}: {len(flock.boids)} boids | Avg Speed: {avg_speed:.2f} | Behavior: {flock.boid_type} | Interflocking: {flock.interFlocking}"
            else:
                text = f"Flock {i}: Dead"
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.surface.blit(text_surface, (10, y_offset))
            y_offset += 20                

    def run_simulation(self, fps=30):
        """Run the simulation with dynamic user input."""
        if self.render:
            running = True
            selected_flock = 0

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if pygame.K_0 <= event.key <= pygame.K_9:
                            selected_flock = event.key - pygame.K_0

                        elif event.key == pygame.K_UP:
                            self.apply_to_flocks(selected_flock, "adjust_speed", amount=1.0)

                        elif event.key == pygame.K_DOWN:
                            self.apply_to_flocks(selected_flock, "adjust_speed", amount=-1.0)

                        elif event.key == pygame.K_q:
                            running = False

                        elif event.key == pygame.K_i:
                            self.apply_to_flocks(selected_flock, "toggle_interflocking")
                        elif event.key == pygame.K_c:
                            self.drawCoop = not self.drawCoop

                coop_count = sum(1 for boid in self.boids if boid.coop)
                defect_count = len(self.boids) - coop_count
                self.history.append((coop_count, defect_count))
                self.update()
                self.draw()
                self.clock.tick(fps)

            pygame.quit()
        else:
            for _ in range(self.steps):
                coop_count = sum(1 for boid in self.boids if boid.coop)
                defect_count = len(self.boids) - coop_count
                self.history.append((coop_count, defect_count))
                self.update()


    def apply_to_flocks(self, flock_index, action, *args, **kwargs):
        """
        Apply a function to either all flocks or just the selected flock.
        """
        if flock_index == 0:
            for flock in self.flocks:
                getattr(flock, action)(*args, **kwargs)
        elif 1 <= flock_index <= len(self.flocks):
            getattr(self.flocks[flock_index - 1], action)(*args, **kwargs)

    def plot_results(self):
            """
            Plot the number of cooperators vs defectors over time.
            """
            coop_counts, defect_counts = zip(*self.history)
            plt.figure()
            plt.plot(coop_counts, label="Cooperators", color="green")
            plt.plot(defect_counts, label="Defectors", color="red")
            plt.xlabel("Time Step")
            plt.ylabel("Count")
            plt.legend()
            plt.title("Strategy Evolution in Boids Simulation")
            plt.show()
"""
Creates an instance of Sky and runs the simulation.
"""
if __name__ == "__main__":
    sky = Sky(render=True)
    sky.run_simulation()
    sky.plot_results()