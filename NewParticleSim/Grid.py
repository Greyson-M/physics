import pygame

class Grid():
    
    class Cell:
        def __init__(self, env, x, y) -> None:
            self.env = env
            self.x = x
            self.y = y
            self.color = self.env.BLACK
            self.rect = pygame.Rect(self.x, self.y, self.env.cell_size, self.env.cell_size)

            self.particles = []

        def getIndex(self):
            return (self.x/self.env.cell_size, self.y/ self.env.cell_size)

        def update(self):
            leftover = []
            for p in self.particles:
                if self.rect.collidepoint(p.pos):
                    leftover.append(p)

            self.particles = leftover

            if len(self.particles) > 1:
                self.color = self.env.RED
            else:
                self.color = self.env.BLACK
            

    def __init__(self, env) -> None:
        self.env = env

        self.cells = [[self.Cell(self.env, x, y) for x in range(0, self.env.WIDTH, self.env.cell_size)] for y in range(0, self.env.HEIGHT, self.env.cell_size)]

    def draw(self):
        for row in self.cells:
            for cell in row:
                #print (str(cell.getIndex()) + ": " + str(len(cell.particles)) + " particles")

                pygame.draw.rect(self.env.WIN, cell.color, cell.rect, 1)


                cell.update()

    def getCell(self, pos):
        return self.cells[int(pos[1] / self.env.cell_size)][int(pos[0] / self.env.cell_size)]