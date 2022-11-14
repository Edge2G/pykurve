import pygame as pg
from sys import exit
from random import seed, randint
from math import sqrt

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
        self.direction = randint(0, 15)
        self.speed = 2

    def inc_direction(self):
        if self.direction == 15:
            self.direction = 0
            return 

        self.direction += 1

    def dec_direction(self):
        if self.direction == 0:
            self.direction = 15
            return

        self.direction -= 1

    def move(self):
        if self.direction == 0:
            self.y_pos -= self.speed
            return
        if self.direction == 1:
            self.y_pos -= 1.73 * self.speed
            self.x_pos += self.speed
            return
        if self.direction == 2:
            self.y_pos -= self.speed
            self.x_pos += self.speed
            return
        if self.direction == 3:
            self.y_pos -= 0.57 * self.speed
            self.x_pos += self.speed
            return
        if self.direction == 4:
            self.x_pos += self.speed
            return
        if self.direction == 5:
            self.y_pos += 0.57 * self.speed
            self.x_pos += self.speed
            return
        if self.direction == 6:
            self.y_pos += self.speed
            self.x_pos += self.speed
            return
        if self.direction == 7:
            self.y_pos += 1.73 * self.speed
            self.x_pos += self.speed
            return
        if self.direction == 8:
            self.y_pos += self.speed
            return
        if self.direction == 9:
            self.y_pos += 1.73 * self.speed
            self.x_pos -= self.speed
            return
        if self.direction == 10:
            self.y_pos += self.speed
            self.x_pos -= self.speed
            return
        if self.direction == 11:
            self.y_pos += 0.57 * self.speed
            self.x_pos -= self.speed
            return
        if self.direction == 12:
            self.x_pos -= self.speed
            return
        if self.direction == 13:
            self.y_pos -= 0.57 * self.speed
            self.x_pos -= self.speed
            return
        if self.direction == 14:
            self.y_pos -= self.speed
            self.x_pos -= self.speed
            return
        if self.direction == 15:
            self.y_pos -= 1.73 * self.speed
            self.x_pos -= self.speed
            return


def main():
    # DEFS
    W_WIDTH     = 1600
    W_HEIGHT    = 900
    W_TITLE     = "Pykurve"
    FPS         = 60

    seed()
    pg.init()
    game_screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))
    pg.display.set_caption(W_TITLE)
    clock = pg.time.Clock()
    timer_event = pg.USEREVENT+1
    erase_event = pg.USEREVENT+2
    time_delay = 3000
    pg.time.set_timer(timer_event, time_delay)

    background_surface = pg.Surface((W_WIDTH, W_HEIGHT))
    background_surface.fill((0, 0, 0))
    game_area = pg.Rect(W_WIDTH//3, 10, int(0.66*W_WIDTH), int(0.98*W_HEIGHT))
    pg.draw.rect(background_surface, (100, 100, 100), game_area, 8, 3)
    game_screen.blit(background_surface, (0, 0))

    player1 = Curve()
    isPressed_rkey = False
    isPressed_lkey = False
    isDrawing = True
    trail_frame_counter = 0
    frame_delay = 5

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

        if(isPressed_lkey):
            frame_delay -= 1
            if frame_delay == 0:
                frame_delay = 5
                player1.dec_direction()

        if(isPressed_rkey):
            frame_delay -= 1
            if frame_delay == 0:
                frame_delay = 5
                player1.inc_direction()
            
        player1.move()

        pg.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()