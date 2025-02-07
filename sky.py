#!/usr/bin/env python3

import pygame
from flock import Flock
import numpy as np

class Sky:
    def __init__(self):
        """
        Initialize a new Sky instance with flocks.
        """
        pygame.init()
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Boids Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.flocks = []
        self.flocks.append(Flock(0, size=50, surface=self.surface, colour=(0, 255, 0), behaviour="directional", interFlocking=True))
        self.flocks.append(Flock(1, size=50, surface=self.surface, colour=(255, 0, 0), behaviour="directional", interFlocking=False))

        self.boids = [boid for flock in self.flocks for boid in flock.boids]

    def update(self):
        """
        Update each flock in the sky.
        """
        for flock in self.flocks:
            flock.update(self.boids)

    def draw(self):
        """
        Clear the screen and draw each flock along with UI data.
        """
        self.surface.fill((255, 255, 255))

        for flock in self.flocks:
            flock.draw()
        
        self.draw_ui()

        pygame.display.flip()

    def draw_ui(self):
        """
        Draw real-time flock statistics on the screen.
        """
        y_offset = 10
        for i, flock in enumerate(self.flocks):
            avg_speed = sum(np.linalg.norm(boid.velocity) for boid in flock.boids) / len(flock.boids)
            text = f"Flock {i}: {len(flock.boids)} boids | Avg Speed: {avg_speed:.2f} | Behavior: {flock.behaviour.__class__.__name__}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.surface.blit(text_surface, (10, y_offset))
            y_offset += 20

    def run_simulation(self, fps=30):
        """Run the simulation with dynamic user input."""
        running = True
        selected_flock = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Switch flock selection (1-9 keys)
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        selected_flock = event.key - pygame.K_1

                    # Change behavior (F for flocking, D for directional, N for non-flocking)
                    if event.key == pygame.K_f:
                        self.flocks[selected_flock].set_behaviour("flocking")
                    elif event.key == pygame.K_d:
                        self.flocks[selected_flock].set_behaviour("directional")
                    elif event.key == pygame.K_n:
                        self.flocks[selected_flock].set_behaviour("non-flocking")
                    elif event.key == pygame.K_o:
                        self.flocks[selected_flock].set_behaviour("omniscient")

                    # Increase speed
                    elif event.key == pygame.K_UP:
                        for boid in self.flocks[selected_flock].boids:
                            boid.maxSpeed += 1.0

                    # Decrease speed
                    elif event.key == pygame.K_DOWN:
                        for boid in self.flocks[selected_flock].boids:
                            boid.maxSpeed = max(1.0, boid.maxSpeed - 1.0)

                    # Quit simulation
                    elif event.key == pygame.K_q:
                        running = False

            self.update()
            self.draw()
            self.clock.tick(fps)

        pygame.quit()

"""
Creates an instance of Sky and runs the simulation.
"""
if __name__ == "__main__":
    sky = Sky()
    sky.run_simulation()