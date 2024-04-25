import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Create the 2D array
u = np.ones((ROWS, COLS))
v = np.ones((ROWS, COLS))

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

dt = 0.01  # time step
dx = 2 / (ROWS - 1)  # spatial step in the x direction
dy = 2 / (COLS - 1)  # spatial step in the y direction

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the fluid velocities
    u[1:-1, 1:-1] = u[1:-1, 1:-1] - dt / dx * u[1:-1, 1:-1] * (u[1:-1, 1:-1] - u[1:-1, 0:-2]) - dt / dy * v[1:-1, 1:-1] * (u[1:-1, 1:-1] - u[0:-2, 1:-1])
    v[1:-1, 1:-1] = v[1:-1, 1:-1] - dt / dx * u[1:-1, 1:-1] * (v[1:-1, 1:-1] - v[1:-1, 0:-2]) - dt / dy * v[1:-1, 1:-1] * (v[1:-1, 1:-1] - v[0:-2, 1:-1])

    # Draw each cell
    for i in range(ROWS):
        for j in range(COLS):
            color = int((u[i, j] + v[i, j]) / 2 * 255)
            pygame.draw.rect(screen, (color, color, color), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.update()

pygame.quit()