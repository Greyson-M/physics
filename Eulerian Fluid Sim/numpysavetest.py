import numpy as np
import pygame
from settings import *



# Create the Pygame window
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
pygame.display.set_caption("Fluid Simulation")
clock = pygame.time.Clock()


boundaries = np.load("bound.npy")
den_hist = np.load("den.npy")
vel_hist = np.load("vel.npy")
print (den_hist.shape)
print (vel_hist.shape)
curl_hist = []

def calculate_curl():

    def curl(u, v):
        curl_field = np.zeros((WIDTH, HEIGHT))

        for i in range(1, WIDTH - 1):
            for j in range(1, HEIGHT - 1):
                curl_field[i][j] = (v[i+1][j] - v[i-1][j]) - (u[i][j+1] - u[i][j-1])

        return curl_field

    for i in range(len(vel_hist)):

        curr_vels = vel_hist[i]
        

        curl_hist.append(np.copy(curl(curr_vels[:,:,0], curr_vels[:,:,1])))


class Controls:
    def __init__(self):
        self.vel_color = True
        self.den_color = True
        self.curl_color = True


def draw(density, velocity, curl_field):

    for i in range(WIDTH):
        for j in range(HEIGHT):

            curl_color = min(255, int(abs(curl_field[i][j]) * 255))
            density_color = min(255, max(0, int(density[i][j])))
            velocity_color = min(255, int(abs(velocity[i][j][0]) * 255))
            
            if C.vel_color == False:
                velocity_color = 0
            if C.den_color == False:
                density_color = 0
            if C.curl_color == False:
                curl_color = 0

            #velocity_color = 0
            #curl_color = 0
            #density_color = 0
            
            color = (density_color, curl_color, velocity_color)
            if boundaries[i][j] == 1:
                color = (255, 255, 255)

            #print (color)
            pygame.draw.rect(screen, color, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))



C = Controls()

def main():
    running = True

    while running:
        i = 0
        while i < len(den_hist)-1 and running:
        
            clock.tick(FPS)

            i += 1
            den = den_hist[i]
            vel = vel_hist[i]
            curl_field = curl_hist[i]

            pygame.event.pump()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        C.vel_color = not C.vel_color
                    if event.key == pygame.K_2:
                        C.den_color = not C.den_color
                    if event.key == pygame.K_3:
                        C.curl_color = not C.curl_color

            curr_fps = clock.get_fps()
            pygame.display.set_caption(f"{curr_fps}")

            screen.fill((0, 0, 0))
            draw(den, vel, curl_field)
            pygame.display.flip()


    # i = 0

    # running = True

    # while i < len(den_hist)-1 and running:
    
    #     clock.tick(FPS)

    #     i += 1
    #     den = den_hist[i]
    #     vel = vel_hist[i]
    #     curl_field = curl_hist[i]

    #     pygame.event.pump()
    #     clock.tick(FPS)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    #     curr_fps = clock.get_fps()
    #     pygame.display.set_caption(f"{curr_fps}")

    #     screen.fill((0, 0, 0))
    #     draw(den, vel, curl_field)
    #     pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":

    calculate_curl()

    print (np.array(curl_hist).shape)

    main()