import pygame

from second_test import Fluid

class Environment():
    def __init__(self) -> None:
        self.fluid_size = 16
        self.scale = 10

        self.FPS = 144  # Frames per second
        self.dt = 1/2  # Time step
        self.width = self.fluid_size * self.scale # Width of the simulation area
        self.height = self.fluid_size * self.scale  # Height of the simulation area

        # Initialize pygame
        pygame.init()
        # Create a pygame window
        self.win = pygame.display.set_mode((self.width, self.height))
        self.win.fill((217, 217, 217))
        self.clock = pygame.time.Clock()
        pygame.display.flip()
        # Set the title of the window
        pygame.display.set_caption("Fluid Simulation")

        self.fluid = Fluid(self.fluid_size, 0.1, 1, self)


    def draw_fluid(self, fluid: Fluid):
        for i in range(fluid.size):
            for j in range(fluid.size):
                x = i * self.scale
                y = j * self.scale
                #d = fluid.density[fluid.IX(i, j)] * 255
                d = fluid.density[j][i] * 255
                if d > 255:
                    d = 255
                pygame.draw.rect(self.win, (d , d , d), (x, y, self.width / fluid.size, self.height / fluid.size))

    def check_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and mouse_pos[0] < self.width and mouse_pos[1] < self.height and mouse_pos[0] > 0 and mouse_pos[1] > 0:
            self.fluid.addDensity(int(mouse_pos[0] * self.fluid.size / self.width), int(mouse_pos[1] * self.fluid.size / self.height), 0.2)
            self.fluid.addVelocity(int(mouse_pos[0] * self.fluid.size / self.width), int(mouse_pos[1] * self.fluid.size / self.height), 10, 10)

    def update(self):
        self.clock.tick(self.FPS)

        self.check_events()
        self.fluid.step()
        self.draw_fluid(self.fluid)

        pygame.display.update()     #update screen
        self.win.fill((217,217,217))     #clear prev frame


def main():
    env = Environment()
    running = True
    while running:
        if pygame.event.get(pygame.QUIT):
            running = False

        env.update()

if __name__ == "__main__":
    main()
