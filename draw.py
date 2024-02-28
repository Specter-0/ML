import pygame as pg 
from objects import bird, pipe, background
import subprocess as sp

pg.init()

sp.run("clear", shell=True)

# ALL CAPS WIDTH AND HEIGHT ARE ALWAYS WINDOW DIMENSIONS
WIDTH = 700
HEIGHT = 875

GRAVITY = 0.4
PIPE_SPEED = 4

MAX_BG_SPEED = 5
bg_speed = 1

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

def accelerate(n : float, MAX : float, STEP : float, EXPONENT : float = 1) -> float:
    if n >= MAX:
        return MAX
    return min(MAX, n + STEP * EXPONENT)

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
    
    bg.draw(window)
    bg.update(bg_speed)
    
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

    bg.draw(window)
    bg_speed = accelerate(bg_speed, 2, 0.02, 1.5)
    bg.update(bg_speed)
    
    for pipeelm in pipes:
        if pipeelm.update(PIPE_SPEED, player):
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