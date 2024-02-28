import pygame as pg 
from objects import bird, pipe, background
import subprocess as sp

pg.init()

sp.run("clear", shell=True)

# ALL CAPS WIDTH AND HEIGHT ARE ALWAYS WINDOW DIMENSIONS
WIDTH = 700
HEIGHT = 875

GRAVITY = 0.4
SPEED = 4

PIPE_DISTANCE = 3000

def handle_events() -> list:
    keyque = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return None
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return None
            
            else:
                keyque.append(event.key)
            
        if event.type == pg.USEREVENT + 1:
            pipes.append(pipe.Pipe(WIDTH, HEIGHT))
    
    return keyque

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ML")

clock = pg.time.Clock()

player = bird.Bird(HEIGHT)
bg = background.Background(WIDTH, HEIGHT)

pg.time.set_timer(pg.USEREVENT + 1, PIPE_DISTANCE)
pipes = []

points = 0
running = True
blit_hitboxes = False

while running:
    window.fill(pg.Color("white"))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                running = False
    
    window.fill(pg.Color("black"))
    
    player.draw(window)
    player.sprite_update()
    pg.display.flip()
    clock.tick(60)

running = True
while running:
    keyque = handle_events()
    if keyque == None:
        running = False
        break

    window.fill(pg.Color("black"))
    
    bg.draw(window)
    bg.update(6)
    
    for pipeelm in pipes:
        if pipeelm.update(SPEED, player):
            points += 1
            print(points)
        pipeelm.draw(window)

    if player.update(GRAVITY, HEIGHT, pipes):
        running = False
    
    player.key_events(keyque)
    player.draw(window)
    
    if pg.K_h in keyque:
        blit_hitboxes = not blit_hitboxes

    if blit_hitboxes:
        player.draw_hitbox(window)
    
    pg.display.flip()
    clock.tick(60)

pg.quit()