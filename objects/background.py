import pygame as pg

class Background(pg.sprite.Sprite):
    def __init__(self, WIDTH : int, HEIGHT : int):
        super(Background, self).__init__()
        
        self.WIN_WIDTH = WIDTH
        self.WIN_HEIGHT = HEIGHT
        
        
        self.surf_first = pg.image.load("assets/mountian_bg.jpeg").convert()
        self.surf_first.set_colorkey((255, 255, 255), pg.RLEACCEL)
        self.surf_first = pg.transform.scale(self.surf_first, (self.WIN_WIDTH * 2, self.WIN_HEIGHT))
        
        self.rect_first = self.surf_first.get_rect()
        self.rect_first.move_ip((0, self.WIN_HEIGHT / 2 - self.rect_first.height / 2))
        
        
        self.surf_after = self.surf_first.copy()
        
        self.rect_after = self.surf_after.get_rect()
        self.rect_after.move_ip((self.WIN_WIDTH * 2, self.WIN_HEIGHT / 2 - self.rect_after.height / 2))
        
        

    def draw(self, window):
        window.blit(self.surf_first, self.rect_first)
        window.blit(self.surf_after, self.rect_after)
        
    def update(self, BG_SPEED : float):
        self.rect_first.move_ip((-BG_SPEED, 0))
        
        if self.rect_first.right < 0:
            self.rect_first.left = self.surf_first.get_width()
            
        self.rect_after.move_ip((-BG_SPEED, 0))
        
        if self.rect_after.right < 0:
            self.rect_after.left = self.surf_after.get_width()