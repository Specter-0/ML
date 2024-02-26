import pygame as pg
import random
from objects import bird

class Pipe(pg.sprite.Sprite):
    def __init__(self, WIDTH : int, HEIGHT : int):
        super(Pipe, self).__init__()
        
        width = 170
        
        weight = random.random()

        self.surf_top = pg.image.load("assets/pipe_top.png").convert()
        self.surf_top = pg.transform.scale(self.surf_top, (width, HEIGHT * (max(weight - 0.13, 0))))
        self.surf_top.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.rect_top = self.surf_top.get_rect()
        
        self.surf_bottom = pg.image.load("assets/pipe_bottom.png").convert()
        self.surf_bottom = pg.transform.scale(self.surf_bottom, (width, HEIGHT * (max(1 - weight - 0.13, 0))))
        self.surf_bottom.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.rect_bottom = self.surf_bottom.get_rect()
        
        self.rect_top.move_ip((WIDTH, 0))
        self.rect_bottom.move_ip((WIDTH, HEIGHT - self.rect_bottom.height))
        
        self.given_point = False
        self.pointblock_rect = pg.Rect(WIDTH + width, 0, 1, HEIGHT)
        
        
    def update(self, SPEED : float, bird : bird.Bird) -> bool:
        """
        if returns true then add a point
        """
        self.rect_top.move_ip((-SPEED, 0))
        self.rect_bottom.move_ip((-SPEED, 0))
        self.pointblock_rect.move_ip((-SPEED, 0))
        
        if not self.given_point and self.pointblock_rect.colliderect(bird.rect):
            self.given_point = True
            return True
        
        return False
        

    def draw(self, window):
        window.blit(self.surf_top, self.rect_top)
        window.blit(self.surf_bottom, self.rect_bottom)