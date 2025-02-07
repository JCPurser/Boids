# Boids Simulation

## Overview
This project implements a **Boids Simulation**, a simple agent-based model for simulating flocking behavior as set out by **C. Reynolds** in the 1987 paper **Flocks, Herds, and Schools: A Distributed Behavioral Model** pubsihed in _Computer Graphics_. The simulation uses **Pygame** for rendering and **NumPy** for vector calculations.

## Features
- **Flocking Behavior**: Implements **collision avoidance, velocity matching, and flock centering**.
- **Wall Avoidance**: Boids bounce off screen edges.
- **Random Initialization**: Boids start with randomized positions and velocities centered around the middle of the screen.
- **Behaviour Customisation**: Boid behaviour can be set at the flock level from provided rulesets.

## Installation
### Prerequisites
Ensure you have Python installed along with the required dependencies:
```sh
pip install pygame numpy
```

## Running the Simulation
To run the Boids simulation, execute:
```sh
python sky.py
```

## Code Structure
```
📂 boids-simulation
├── boid.py          # Boid class handling movement & behavior
├── flock.py         # Flock class managing a group of boids
├── sky.py           # Main simulation script using Pygame
├── boidBehaviour.py # Rulesets for boid behaviour
├── README.md        # Project documentation
```

## Controls
- **Press 'E'** to exit the simulation.
