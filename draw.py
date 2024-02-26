import pygame as pg 
from objects import bird, pipe

pg.init()

# ALL CAPS WIDTH AND HEIGHT ARE ALWAYS WINDOW DIMENSIONS
WIDTH = 800
HEIGHT = 600

GRAVITY = 0.2
SPEED = 3

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ML")

clock = pg.time.Clock()

player = bird.Bird()

pg.time.set_timer(pg.USEREVENT + 1, 4000)
pipes = []

points = 0
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
            

    window.fill(pg.Color("white"))
    
    for pipeelm in pipes:
        if pipeelm.update(SPEED, player):
            points += 1
            print(points)
        pipeelm.draw(window)

    if player.update(GRAVITY, HEIGHT, pipes):
        running = False
    player.key_events(keyque)
    player.draw(window)
    
    
    pg.display.flip()
    clock.tick(60)

pg.quit()