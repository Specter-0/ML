import pygame as pg
import os

JUMP_HEIGHT : int = 10
TERMINAL_UP : int = 15
TERMINAL_DOWN : int = 25
HITBOX_SCALE : tuple = (0.8, 0.4)
SPRITE_COUNT : int = len(os.listdir("assets/jet"))

class Bird(pg.sprite.Sprite):
    def __init__(self, HEIGHT : int):
        super(Bird, self).__init__()
        
        self.jump_height = JUMP_HEIGHT
        self.velocity : float = 0
        
        self.sprite_count = SPRITE_COUNT
        self.current_sprite_index = 1 # 1 indexing
        
        self.new_surf()
        self.rect = self.surf.get_rect()
        self.rect.move_ip((200, HEIGHT / 2.2))
        
        self.hitbox = self.rect.copy()
        self.hitbox.scale_by_ip(HITBOX_SCALE[0], HITBOX_SCALE[1])
        
        self.hitbox_surf = pg.Surface((self.hitbox.width, self.hitbox.height))
        self.hitbox_surf.fill((255, 0, 0))
    
    def new_surf(self):
        self.surf = pg.image.load(f"assets/jet/{self.current_sprite_index}.png").convert()
        self.surf.set_colorkey((255, 255, 255), pg.RLEACCEL)
        self.surf = pg.transform.flip(self.surf, True, False)
        self.surf = pg.transform.scale(self.surf, (80, 80))
    
    def sprite_update(self):
        self.current_sprite_index += 1
        if self.current_sprite_index > self.sprite_count:
            self.current_sprite_index = 1
        else:
            self.new_surf()
            
            self.tilt()
    
    def tilt(self):
        self.surf = pg.transform.rotate(self.surf, -self.velocity * 2 if -self.velocity > 0 else -self.velocity)
        self.hitbox 

    def update(self, GRAVITY : float, HEIGHT : int, pipes : list) -> bool:
        """
        if returns true then the bird is dead
        """
        
        self.sprite_update()
        
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