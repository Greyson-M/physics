import pygame
from Grid import Grid

class Environment():
    def __init__(self) -> None:
        #load
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 144

        pygame.init()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WIN.fill((217, 217, 217))

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.clock = pygame.time.Clock()

        self.frame_count = 0

        self.grid = Grid(self, 2, draw_lines=False)


    def update(self):
        self.WIN.fill((217, 217, 217))
        self.frame_count += 1

        
        
        self.grid.update()

        self.grid.draw()

        pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")

        self.clock.tick(self.FPS)
        pygame.display.update()