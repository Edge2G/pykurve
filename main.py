import pygame as pg
from sys import exit
from random import seed, randint
from math import cos, sin, radians

class Curve:
    def __init__(self):
        self.x_pos = 800
        self.y_pos = 450
        self.prev_x = self.x_pos
        self.prev_y = self.y_pos
        self.head = pg.image.load("graphics/head.png")
        self.invis_trail = pg.image.load("graphics/invis_trail.png")
        self.trail_pos = []
        self.invis_trail_pos = []
        self.trail_px_delay = 8
        self.direction = randint(0, 360)
        self.speed = 4

    def check_dir(self):
        # Direction can only go from 0-360 degrees
        if self.direction > 360:
            self.direction = 0
        if self.direction < 0:
            self.direction = 360

    def move(self):
        # First check direction
        self.check_dir()

        # Actually move
        # Movement is based on (x,y) changes
        # Which is given by sin, cos values of current direction
        # Multiplied by the speed
        self.y_pos += cos(radians(self.direction)) * self.speed
        self.x_pos += sin(radians(self.direction)) * self.speed

def main():
    # DEFS
    W_WIDTH     = 1600
    W_HEIGHT    = 900
    W_TITLE     = "Pykurve"
    FPS         = 60

    # Initialization functions
    seed()
    pg.init()
    game_screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))
    pg.display.set_caption(W_TITLE)
    clock = pg.time.Clock()
    timer_event = pg.USEREVENT+1
    erase_event = pg.USEREVENT+2
    time_delay = 3000
    pg.time.set_timer(timer_event, time_delay)

    # Print game area
    background_surface = pg.Surface((W_WIDTH, W_HEIGHT))
    background_surface.fill((0, 0, 0))
    game_area = pg.Rect(W_WIDTH//3, 10, int(0.66*W_WIDTH), int(0.98*W_HEIGHT))
    pg.draw.rect(background_surface, (100, 100, 100), game_area, 8, 3)
    game_screen.blit(background_surface, (0, 0))

    # Create a curve
    player1 = Curve()
    isPressed_rkey = False
    isPressed_lkey = False
    isDrawing = True
    trail_frame_counter = 0
    frame_delay = 5

    # Game loop
    while(True):
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == timer_event:
                next_invis_trail = randint(1, 4)
                time_delay = next_invis_trail * 1000
                pg.time.set_timer(timer_event, time_delay)
                
                if isDrawing:
                    isDrawing = False
                    invis_trail_duration = randint(FPS*500, FPS*1000)
                else:
                    isDrawing = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    isPressed_lkey = True

                if event.key == pg.K_RIGHT:
                    isPressed_rkey = True

                if event.key == pg.K_SPACE:
                    player1.speed += 1

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    isPressed_lkey = False
                if event.key == pg.K_RIGHT:
                    isPressed_rkey = False


        game_screen.blit(player1.head, (player1.x_pos, player1.y_pos))

        if isDrawing:
            player1.invis_trail_pos = []
            trail_frame_counter = 0
            invis_trail_idx = 0
            player1.trail_pos.append((player1.x_pos, player1.y_pos))
        else:
            trail_frame_counter += 1
            player1.invis_trail_pos.append((player1.x_pos, player1.y_pos))

            if trail_frame_counter >= player1.trail_px_delay:
                erase_coords = player1.invis_trail_pos[invis_trail_idx]
                game_screen.blit(player1.invis_trail, (erase_coords[0], erase_coords[1]))
                invis_trail_idx += 1        

        # Movement handling

        if(isPressed_lkey):
            player1.direction += 3

        if(isPressed_rkey):
            player1.direction -= 3
            
        player1.move()

        pg.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()