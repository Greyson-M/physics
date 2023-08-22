from Environment import Environment

import pygame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread

env = Environment()


def test():
    env.addMass(env, 10, 1, np.array([env.WIDTH/2, env.HEIGHT/2]), env.RED)

def main():
    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                if not env.hovering:
                    pos = pygame.mouse.get_pos()
                    env.addMass(env, env.particle_size, 1, np.array([pos[0], pos[1]]), ((pos[0] % 255), (pos[1] % 255), (pos[0] + pos[1]) % 255))


        env.update()
        
def plot():
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    def animate(xs, ys):
        xs.append(env.clock.get_time())
        ys.append(env.E_disp)

        xs = xs[-20:]
        ys = ys[-20:]

        ax.clear()
        ax.plot(xs, ys)

        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.ylabel('Energy')

    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    plt.show()

if __name__ == "__main__":
    main()
    
    

