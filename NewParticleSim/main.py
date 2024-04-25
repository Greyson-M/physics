from Environment import Environment

import pygame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyinstrument import Profiler

env = Environment()


def test(partnum):
    OFFSET = 300
    for i in range(partnum):
        for j in range(partnum):
            print (np.array([i*(3 * env.particle_size + 2) + OFFSET, j*(3 * env.particle_size + 2) + OFFSET]))
            env.addMass(env, env.particle_size, 10, np.array([i*(3 * env.particle_size + 2) + OFFSET, j*(3 * env.particle_size + 2) + OFFSET]), ((i*10) % 255, (i*20) % 255, (i*30) % 255))
            print (env.massList[-1].pos)

test(15)

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
                    env.addMass(env, env.particle_size, 10, np.array([pos[0], pos[1]]), ((pos[0] % 255), (pos[1] % 255), (pos[0] + pos[1]) % 255))
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
    profile = False
    
    if profile:
        with Profiler() as p:
            main()

        p.print()
        p.open_in_browser()

    else:
        main()
    
    


