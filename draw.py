import pygame as pg 
from objects import bird, pipe, background
import subprocess as sp
import random, sys

pg.init()

sp.run("clear", shell=True)

# ALL CAPS WIDTH AND HEIGHT ARE ALWAYS WINDOW DIMENSIONS
WIDTH = 700
HEIGHT = 875

GRAVITY = 0.45
PIPE_SPEED = 4

MAX_BG_SPEED = 5
bg_speed = 1

PIPE_DISTANCE = 2000

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

player = bird.Bird(HEIGHT, 200)
flock = [player]

if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    print("provide a valid number of birds")
    quit()

for i in range(1, int(sys.argv[1])):
    flock.append(bird.Bird(HEIGHT, 200))


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
            
            if event.key == pg.K_ESCAPE:
                quit()
    
    bg.draw(window)
    bg.update(bg_speed)
    
    player.draw(window)
    player.sprite_update()
    pg.display.flip()
    clock.tick(60)

running = True
while running:
    keyque = handle_events()
    if keyque == None or len(flock) == 0:
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

    for index, bird in enumerate(flock):
        if bird.update(GRAVITY, HEIGHT, pipes):
            del flock[index]
        bird.key_events(keyque)
        bird.draw(window)
        
        if random.randint(0, 100) < 2:
            #bird.jump()
            pass
    
    if pg.K_h in keyque:
        blit_hitboxes = not blit_hitboxes

    if blit_hitboxes:
        player.draw_hitbox(window)
    
    pg.display.flip()
    clock.tick(60)

pg.quit()