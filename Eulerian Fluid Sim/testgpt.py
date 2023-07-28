import numpy as np
import pygame

# Constants
width = 600  # Width of the simulation grid
height = 600  # Height of the simulation grid
dt = 0.1  # Time step size
viscosity = 0.1  # Viscosity of the fluid
num_steps = 100  # Number of simulation steps

# Initialize velocity and density grids
u = np.zeros((width, height))  # X-component of velocity
v = np.zeros((width, height))  # Y-component of velocity
density = np.zeros((width, height))  # Fluid density

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate velocity divergence
    divergence = np.zeros((width, height))
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            divergence[i, j] = ((u[i + 1, j] - u[i - 1, j]) +
                               (v[i, j + 1] - v[i, j - 1])) / 2

    # Calculate pressure from velocity divergence
    pressure = np.zeros((width, height))
    for _ in range(20):  # Iterative method to solve pressure Poisson equation
        pressure[1:-1, 1:-1] = ((pressure[:-2, 1:-1] +
                                 pressure[2:, 1:-1] +
                                 pressure[1:-1, :-2] +
                                 pressure[1:-1, 2:]) -
                                divergence[1:-1, 1:-1] * dt**2) / 4

    # Update velocity using pressure gradient
    u[1:-1, 1:-1] -= (pressure[2:, 1:-1] - pressure[:-2, 1:-1]) / (2 * dt)
    v[1:-1, 1:-1] -= (pressure[1:-1, 2:] - pressure[1:-1, :-2]) / (2 * dt)

    # Update velocity due to viscosity
    u[1:-1, 1:-1] += (viscosity * ((u[2:, 1:-1] - 2 * u[1:-1, 1:-1] + u[:-2, 1:-1]) +
                                   (u[1:-1, 2:] - 2 * u[1:-1, 1:-1] + u[1:-1, :-2]))) * dt
    v[1:-1, 1:-1] += (viscosity * ((v[2:, 1:-1] - 2 * v[1:-1, 1:-1] + v[:-2, 1:-1]) +
                                   (v[1:-1, 2:] - 2 * v[1:-1, 1:-1] + v[1:-1, :-2]))) * dt

    # Apply boundary conditions
    u[:, 0] = u[:, 1]  # Bottom boundary
    u[:, -1] = u[:, -2]  # Top boundary
    u[0, :] = u[1, :]  # Left boundary
    u[-1, :] = u[-2, :]  # Right boundary

    v[:, 0] = v[:, 1]  # Bottom boundary

    # Render fluid simulation
    screen.fill((0, 0, 0))  # Clear the screen

    # Draw velocity field
    for i in range(width):
        for j in range(height):
            x = i
            y = j
            dx = u[i, j] * 10  # Scale the velocity for visualization
            dy = v[i, j] * 10  # Scale the velocity for visualization
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x + dx, y + dy), 1)

    pygame.display.flip()
    clock.tick(30)  # Limit the frame rate

pygame.quit()
