import pygame as pg 
from objects import bird, pipe
import subprocess as sp

pg.init()

sp.run("clear", shell=True)

# ALL CAPS WIDTH AND HEIGHT ARE ALWAYS WINDOW DIMENSIONS
WIDTH = 700
HEIGHT = 875

GRAVITY = 0.4
SPEED = 3

PIPE_DISTANCE = 3000



darkmode = True

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ML")

clock = pg.time.Clock()

player = bird.Bird(HEIGHT, darkmode)

pg.time.set_timer(pg.USEREVENT + 1, PIPE_DISTANCE)
pipes = []

points = 0
running = True

while running:
    window.fill(pg.Color("white"))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                running = False
    
    if darkmode: window.fill(pg.Color("black"))
    else: window.fill(pg.Color("white"))
    
    player.draw(window)
    player.sprite_update()
    pg.display.flip()
    clock.tick(60)

running = True
while running:
    keyque = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            
            else:
                keyque.append(event.key)
            
        if event.type == pg.USEREVENT + 1:
            pipes.append(pipe.Pipe(WIDTH, HEIGHT))
            

    if darkmode: window.fill(pg.Color("black"))
    else: window.fill(pg.Color("white"))
    
    for pipeelm in pipes:
        if pipeelm.update(SPEED, player):
            points += 1
            print(points)
        pipeelm.draw(window)

    if player.update(GRAVITY, HEIGHT, pipes):
        running = False
    player.key_events(keyque)
    player.draw(window)
    #player.draw_hitbox(window)
    
    pg.display.flip()
    clock.tick(60)

pg.quit()