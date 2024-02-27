import pygame as pg
import PIL.Image 

JUMP_HEIGHT = 15
TERMINAL_UP = 15
TERMINAL_DOWN = 25

class Bird(pg.sprite.Sprite):
    def __init__(self, HEIGHT : int, darkmode : bool):
        super(Bird, self).__init__()
        
        self.jump_height = 8
        self.velocity : float = 0

        
        image = PIL.Image.open('assets/bird.png')
        if darkmode:
            inverted_image = PIL.ImageChops.invert(image)
            self.surf = pg.image.fromstring(inverted_image.tobytes(), inverted_image.size, inverted_image.mode).convert()
            self.surf.set_colorkey((255, 255, 255), pg.RLEACCEL)
        else:
            self.surf = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert()
            self.surf.set_colorkey((0, 0, 0), pg.RLEACCEL)
        
        self.surf = pg.transform.scale(self.surf, (60, 60))
        self.rect = self.surf.get_rect()
        self.rect.move_ip((200, HEIGHT / 2.2))
        
        
        self.hitbox = self.rect.copy()
        self.hitbox.scale_by_ip(0.8)
        
        self.hitbox_surf = pg.Surface((self.hitbox.width, self.hitbox.height))
        self.hitbox_surf.fill((255, 0, 0))
        

    def update(self, GRAVITY : float, HEIGHT : int, pipes : list) -> bool:
        """
        if returns true then the bird is dead
        """
        self.velocity += GRAVITY
        if self.velocity > TERMINAL_DOWN:
            self.velocity = TERMINAL_DOWN
        
        self.rect.move_ip((0, self.velocity))
        

        if self.rect.y < -self.rect.height / 1.7:
            self.rect.y = -self.rect.height / 1.7
            self.velocity = 0   
        
        elif self.rect.y > HEIGHT - (self.rect.height - self.rect.height / 1.7):
            return True
        
        self.hitbox.move_ip((0, self.velocity))
        
        for pipeelm in pipes:
            if pipeelm.rect_top.colliderect(self.hitbox) or pipeelm.rect_bottom.colliderect(self.hitbox):
                return True
        
        return False
    
    def key_events(self, keyque : list):
        for key in keyque:
            if key == pg.K_SPACE:
                self.jump()

    def draw(self, window):
        window.blit(self.surf, self.rect)
        
    def draw_hitbox(self, window):
        window.blit(self.hitbox_surf, self.hitbox)

    def jump(self):
        if self.velocity > 0:
            self.velocity = -self.jump_height
        
        else:
            self.velocity = max(-TERMINAL_UP, self.velocity - self.jump_height)