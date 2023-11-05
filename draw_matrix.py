import pygame
from matrix_manager import Simulation
print()

class DrawMatrix:
    def __init__(self,screen, width=200, height=200, padding=20, amount=20):
        self.amount = amount
        self.width = width - padding * 3 
        self.height = height - padding * 3
        self.board_width = (width / 100 ) * 70 
        self.infos_width = width - self.board_width
        self.padding = padding
        self.screen = screen
        self.black = (50,150,100)
        self.white = (50,50,50)
        self.red = (255,0,0) # resources
        self.blue = (0,0,255) # excavator
        self.green = (0,255,0) # buyer 
        self.font =  pygame.font.SysFont('Times new roman', 30)
        
        self.matrix = Simulation(amount)
        self.tile_width_size = self.board_width // self.amount
        self.tile_height_size = self.height // self.amount

    def render_board(self):
        for i in range(self.amount):
            for j in range(self.amount):
                x = self.padding + i * self.tile_width_size
                y = self.padding + j * self.tile_height_size
                rectangle = pygame.Rect(x, y, self.tile_width_size - 5, self.tile_height_size - 5)
                color = self.black if (i + j) % 2 == 0 else self.white
                pygame.draw.rect(self.screen, color, rectangle)
        for i,array in enumerate(self.matrix.matrix):
            for j,tile in enumerate(array):
                if tile == 1:
                    x = self.padding + j * self.tile_width_size
                    y = self.padding + i * self.tile_height_size
                    rectangle = pygame.Rect(x, y, self.tile_width_size - 5, self.tile_height_size - 5)
                    color = self.red
                    pygame.draw.rect(self.screen, color, rectangle)
                if tile == 2:
                    x = self.padding + j * self.tile_width_size
                    y = self.padding + i * self.tile_height_size
                    rectangle = pygame.Rect(x, y, self.tile_width_size - 5, self.tile_height_size - 5)
                    color = self.green
                    pygame.draw.rect(self.screen, color, rectangle)
                if tile >= 3:
                    x = self.padding + j * self.tile_width_size
                    y = self.padding + i * self.tile_height_size
                    rectangle = pygame.Rect(x, y, self.tile_width_size - 5, self.tile_height_size - 5)
                    color = self.blue
                    pygame.draw.rect(self.screen, color, rectangle)   

    def render_infos(self):
        rectangle = pygame.Rect(self.board_width + self.padding + 10,self.padding, self.infos_width - self.padding * 2, self.height + self.padding * 5)
        color = self.black 
        pygame.draw.rect(self.screen, color, rectangle)
        
        x = self.padding + self.board_width + 15 
        y = self.padding + 10
        rectangle = pygame.Rect(x, y, self.infos_width - self.padding * 2 - 10 , self.tile_height_size + 20)
        color = self.red
        pygame.draw.rect(self.screen, color, rectangle) 
        str_to_render = ' Resources : ' + str(len(self.matrix.resource_array)) 
        text_surface = self.font.render(str_to_render, True, self.white)
        self.screen.blit(text_surface, (x, y ))

        y += 50
        rectangle = pygame.Rect(x, y, self.infos_width - self.padding * 2 - 10 , self.tile_height_size + 20)
        color = self.blue
        pygame.draw.rect(self.screen, color, rectangle) 
        str_to_render = 'Ex : ' + str(len(self.matrix.excavator_array)) + '  Fuel: ' + str(self.matrix.fuel_cost)
        text_surface = self.font.render(str_to_render, True,  (255,255,255))
        self.screen.blit(text_surface, (x, y))

        # excavator showing 

        for i, excavator in enumerate(self.matrix.excavator_array):
            y += 50
            rectangle = pygame.Rect(x, y, self.infos_width - self.padding * 2 - 10 , self.tile_height_size + 20)
            color = self.blue
            pygame.draw.rect(self.screen, color, rectangle) 
            str_to_render = str(excavator.coordinates) + ' ' + str(excavator.money)
            text_surface = self.font.render(str_to_render, True, (255,255,255))
            self.screen.blit(text_surface, (x, y))


        y += 50
        rectangle = pygame.Rect(x, y, self.infos_width - self.padding * 2 - 10 , self.tile_height_size + 20)
        color = self.green
        pygame.draw.rect(self.screen, color, rectangle) 
        str_to_render = ' Total Buyer : ' + str(len(self.matrix.buyer_array))
        text_surface = self.font.render(str_to_render, True, self.white)
        self.screen.blit(text_surface, (x, y))
        for i, excavator in enumerate(self.matrix.buyer_array):
            y += 50
            rectangle = pygame.Rect(x, y, self.infos_width - self.padding * 2 - 10 , self.tile_height_size + 20)
            color = self.green
            pygame.draw.rect(self.screen, color, rectangle) 
            str_to_render = str(excavator.coordinates) + ' ' + str(excavator.price)
            text_surface = self.font.render(str_to_render, True, self.white)
            self.screen.blit(text_surface, (x, y ))

    def render_start_button(self):
        x = 100
        y = self.padding + self.height + 10
        rectangle = pygame.Rect(50 ,self.padding + self.height, self.infos_width - self.padding * 4, 50)
        color = self.black 
        pygame.draw.rect(self.screen, color, rectangle)
        str_to_render = 'Start '
        text_surface = self.font.render(str_to_render, True, self.white)
        self.screen.blit(text_surface, (x, y ))

    def render(self):
        self.render_board()
        self.render_infos()
        self.render_start_button()

def main():

    WIDTH = 1200
    HEIGHT = 800
    padding = 50
    amount = 40

    running = True
    start = False

    pygame.font.init() 

    clock = pygame.time.Clock()
    framerate = 1
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    matrix = DrawMatrix(screen,WIDTH,HEIGHT,padding=padding,amount=amount)
    matrix.matrix.print_grid()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print('tick numeber ', matrix.matrix.tick_counter )
                matrix.matrix.tick()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 50 < x < 210 and 701 < y < 750:
                    if start:
                        start = False
                    else:
                        start = True

        screen.fill((200, 200, 200))
        matrix.render()
        pygame.display.update()
        if start:
            matrix.matrix.tick()
        clock.tick(framerate)


main()