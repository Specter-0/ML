import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()

        self.surf = pg.image.load("assets/bird.png").convert()
        self.surf = pg.transform.scale(self.surf, (60, 60))
        self.surf.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.rect = self.surf.get_rect()
        
        self.rect.move_ip((250, 0))
        
        self.velocity : float = 0

    def update(self, GRAVITY : float, HEIGHT : int, pipes : list) -> bool:
        """
        if returns true then the bird is dead
        """
        self.velocity += GRAVITY
        
        self.rect.move_ip((0, self.velocity))

        if self.rect.y < -self.rect.height / 1.7:
            self.rect.y = -self.rect.height / 1.7
            self.velocity = 0
        
        elif self.rect.y > HEIGHT - (self.rect.height - self.rect.height / 1.7):
            return True
        
        for pipeelm in pipes:
            if pipeelm.rect_top.colliderect(self.rect) or pipeelm.rect_bottom.colliderect(self.rect):
                return True

    def key_events(self, keyque : list):
        for key in keyque:
            if key == pg.K_SPACE:
                self.jump()

    def draw(self, window):
        window.blit(self.surf, self.rect)

    def jump(self):
        if self.velocity > 0:
            self.velocity = -5
        
        else:
            self.velocity = max(-10, self.velocity - 5)