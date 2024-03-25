import pygame
import numpy as np
from settings import *

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
pygame.display.set_caption("Fluid Simulation")
clock = pygame.time.Clock()


# Initialize the fluid velocity and density
velocity = np.zeros((WIDTH, HEIGHT, 2))
density = np.zeros((WIDTH, HEIGHT))
curl_field = np.zeros((WIDTH, HEIGHT))
boundaries = np.zeros((WIDTH, HEIGHT))
pressure = np.zeros((WIDTH, HEIGHT))

#boundaries[10:20, 10:20] = 1  # Add a 10x10 boundary at (10, 10)

for i in range(WIDTH):
    for j in range(HEIGHT):

        dist_from_center = np.sqrt(((i - (WIDTH - 20) / 2) ** 2)/2 + ((j - HEIGHT / 2) ** 2)*2)

        if i == 0 or i == WIDTH - 1 or j == 0 or j == HEIGHT - 1:
            boundaries[i][j] = 1

        if dist_from_center < 30/CELL_SIZE:
            boundaries[i][j] = 1

        if j == HEIGHT - 50//CELL_SIZE:
            gap = i - (WIDTH//2)
            if abs(gap) > 15//CELL_SIZE:
                boundaries[i][j] = 1

def add_density(x, y, amount):
    density[int(x)][int(y)] += amount

def add_velocity(x, y, amount_x, amount_y):
    GRAVITY = 0.1 * DT
    velocity[int(x)][int(y)][0] += amount_x
    velocity[int(x)][int(y)][1] += amount_y # + GRAVITY

def set_velocity(x, y, amount_x, amount_y):
    velocity[int(x)][int(y)][0] = amount_x
    velocity[int(x)][int(y)][1] = amount_y

def curl(u, v):
    for i in range(1, WIDTH - 1):
        for j in range(1, HEIGHT - 1):
            curl_field[i][j] = (v[i+1][j] - v[i-1][j]) - (u[i][j+1] - u[i][j-1])

def diffuse(b, x, diff):
    a = DT * diff * (WIDTH - 2) * (HEIGHT - 2)
    for k in range(20):
        for i in range(1, WIDTH - 1):
            for j in range(1, HEIGHT - 1):
                if boundaries[i][j] == 0:
                    x[i][j] = (b[i][j] + a*(x[i-1][j] + x[i+1][j] + x[i][j-1] + x[i][j+1])) / (1 + 4*a)

def compute_divergence(velocity):
    divergence = np.zeros((WIDTH, HEIGHT))

    for i in range(1, WIDTH - 1):
        for j in range(1, HEIGHT - 1):
            if boundaries[i][j] == 0:
                divergence[i][j] = 0.5 * ((velocity[i+1][j][0] if boundaries[i+1][j] == 0 else 0 -
                                           velocity[i-1][j][0] if boundaries[i-1][j] == 0 else 0) +
                                          (velocity[i][j+1][1] if boundaries[i][j+1] == 0 else 0 -
                                           velocity[i][j-1][1] if boundaries[i][j-1] == 0 else 0))

    return divergence

def pressure_solver(pressure, divergence):
    for _ in range(20):  # Number of solver iterations
        for i in range(1, WIDTH - 1):
            for j in range(1, HEIGHT - 1):
                if boundaries[i][j] == 0:
                    pressure[i][j] = ((pressure[i-1][j] if boundaries[i-1][j] == 0 else 0 +
                                        pressure[i+1][j] if boundaries[i+1][j] == 0 else 0 +
                                        pressure[i][j-1] if boundaries[i][j-1] == 0 else 0 +
                                        pressure[i][j+1] if boundaries[i][j+1] == 0 else 0 -
                                        divergence[i][j]) / 4)

def project(velocity, pressure):
    h = 1.0/WIDTH
    divergence = compute_divergence(velocity)

    pressure_solver(pressure, divergence)

    for i in range(1, WIDTH - 1):
        for j in range(1, HEIGHT - 1):
            if boundaries[i][j] == 0:
                velocity[i][j][0] -= 0.5 * ((pressure[i+1][j] if boundaries[i+1][j] == 0 else 0 -
                                              pressure[i-1][j] if boundaries[i-1][j] == 0 else 0) / h)
                velocity[i][j][1] -= 0.5 * ((pressure[i][j+1] if boundaries[i][j+1] == 0 else 0 -
                                              pressure[i][j-1] if boundaries[i][j-1] == 0 else 0) / h)

def advect(b, x, u, v, dt):
    for i in range(1, WIDTH - 1):
        for j in range(1, HEIGHT - 1):
            if boundaries[i][j] == 0:
                x0 = i - dt * WIDTH * u[i][j]
                y0 = j - dt * HEIGHT * v[i][j]
                x0 = max(1.5, min(WIDTH - 1.5, x0))
                y0 = max(1.5, min(HEIGHT - 1.5, y0))
                i0 = max(1, min(WIDTH - 2, int(x0)))
                i1 = max(1, min(WIDTH - 2, i0 + 1))
                j0 = max(1, min(HEIGHT - 2, int(y0)))
                j1 = max(1, min(HEIGHT - 2, j0 + 1))
                s1 = x0 - i0
                s0 = 1 - s1
                t1 = y0 - j0
                t0 = 1 - t1
                x[i][j] = s0 * (t0 * b[i0][j0] + t1 * b[i0][j1]) + s1 * (t0 * b[i1][j0] + t1 * b[i1][j1])

def draw():
    #curl(velocity[:,:,0], velocity[:,:,1])

    for i in range(WIDTH):
        for j in range(HEIGHT):

            curl_color = min(255, int(abs(curl_field[i][j]) * 255))
            density_color = min(255, max(0, int(density[i][j])))
            velocity_color = min(255, int(abs(velocity[i][j][0]) * 255))
            #velocity_color = 0
            
            color = (density_color, curl_color, velocity_color)
            
            directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]

            for d in directions:
                if i + d[0] < WIDTH and j + d[1] < HEIGHT and i + d[0] > 0 and j + d[1] > 0:
                    if boundaries[i + d[0]][j + d[1]] == 1:
                        color = (120, 120, 120)

            if boundaries[i][j] == 1:
                color = (255, 255, 255)

            #print (color)
            pygame.draw.rect(screen, color, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # for i in range(WIDTH):
    #     for j in range(HEIGHT):
    #         color = min(255, max(0, int(density[i][j])))
    #         pygame.draw.rect(screen, (color, color, color), pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))


den_hist = []
vel_hist = []

FRAMES = 60

for i in range(HEIGHT):
            
    for j in range(WIDTH):
        #add_velocity(j, i, 0, 0)

        offest = abs(i - HEIGHT // 2)
        #offest = abs(j - WIDTH // 2)
        add_velocity(j, i, 0.1, 0)
        
        if offest < 10/CELL_SIZE:
            #add_density(j, HEIGHT-1, 7000)
            add_density(1, i, 7000)
            #pass
        

def main():
    running = True

    z = 0

    while running and z < FRAMES:
        den_hist.append(np.copy(density))
        vel_hist.append(np.copy(velocity))
        
        print (z)
        z += 1

        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1:
                    if (x > 1 and x < WIDTH * CELL_SIZE - 1 and y > 1 and y < HEIGHT * CELL_SIZE - 1):
                        add_density(x // CELL_SIZE, y // CELL_SIZE, 10000)
                        add_velocity(x // CELL_SIZE, y // CELL_SIZE, 1, 1)

                if event.button == 3:
                    if (x > 1 and x < WIDTH * CELL_SIZE - 1 and y > 1 and y < HEIGHT * CELL_SIZE - 1):
                        add_velocity(x // CELL_SIZE, y // CELL_SIZE, 10, 1)

        curr_fps = clock.get_fps()
        pygame.display.set_caption(f"{curr_fps}")


        for i in range(HEIGHT):
            
            for j in range(WIDTH):
                #add_velocity(j, i, 0, 0)

                offest = abs(i - HEIGHT // 2)
                #offest = abs(j - WIDTH // 2)

                if offest < 10/CELL_SIZE:
                    #add_density(j, HEIGHT-1, 7000)
                    # add_density(1, i, 7000)
                    pass
                
                #set_velocity(j, i, 3/abs(j+1), 0)
                # add_velocity(j, i, 0.1, 0)

                #set_velocity(j, HEIGHT-1, 0, -20)
                #set_velocity(1, i, 10, 0)

            #add_density(1, i, 700)
            #set_velocity(1, i, 25, 0)
            # add_velocity(1, i, 1, 0)

        diffuse(density, density, 0.001)
        diffuse(velocity[:,:,0], velocity[:,:,0], 0.01)
        diffuse(velocity[:,:,1], velocity[:,:,1], 0.01)

        advect(density, density, velocity[:,:,0], velocity[:,:,1], DT)
        advect(velocity[:,:,0], velocity[:,:,0], velocity[:,:,0], velocity[:,:,1], DT)
        advect(velocity[:,:,1], velocity[:,:,1], velocity[:,:,0], velocity[:,:,1], DT)
        project(velocity, pressure)

        screen.fill((0, 0, 0))
        draw()
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()

    with open("den.npy", "wb") as f:
        np.save(f, np.array(den_hist))
    with open("vel.npy", "wb") as f:
        np.save(f, np.array(vel_hist))
    with open("bound.npy", "wb") as f:
        np.save(f, np.array(boundaries))
    