# Boids Simulation

## Overview
This project implements a **Boids Simulation**, a simple agent-based model for simulating flocking behavior as set out by C. Reynolds in the 1987 paper **Flocks, Herds, and Schools: A Distributed Behavioral Model** as published in _Computer Graphics_. The simulation uses **Pygame** for rendering and **NumPy** for vector calculations.

## Features
- **Flocking Behavior**: Implements **collision avoidance, velocity matching, and flock centering**.
- **Wall Avoidance**: Boids bounce off screen edges.
- **Random Initialization**: Boids start with randomized positions and velocities centered around the middle of the screen.
- **Behaviour Customisation**: Boid behaviour can be set at the flock level from provided rulesets.
    - **Basic Flocking**: As set out in the 1987 paper.
    - **Non-Flocking**: No motion, as a control.
    - **Directional Flocking**: Additional flocking rules implemented for surrounding boid detection to be modified as suggested in 1987 paper.
    - **Omniscient Flocking**: Flocking rules but with each boid knowing every boid location.
    - **Migratory Flocking**: Unimplemented.
    - **Evasive Flocking**: Unimplemented.

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
- **Number Keys**: Select the flock to be altered.
- **q**: Exit the simulation.
- **f, n, d, o**: Flocking modes basic, non-flocking, directional, and omniscient respectivly.
- **Up and Down**: Increase and decrease flock speed.

## To Do
- Populate templates for Migration and Evasion.
- Add in greater UI interactability.
- Integrate collaboration.
    - Consider, everytime two meet they undergo some resource interaction depending on C/D. See how ratio of C/D boids change over time.
- Permit greater ranges of speed, prevent renormalising to 5.
- Make different types of rules for how walls work.
