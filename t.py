import pygame as pg 
from objects import bird, pipe, background
import subprocess as sp
import random, sys

class Game():
    def __init__(self) -> None:
        pg.init()
        
        # ALL CAPS WIDTH AND HEIGHT ARE ALWAYS WINDOW DIMENSIONS
        self.WIDTH = 700
        self.HEIGHT = 875

        self.GRAVITY = 0.45
        
        self.PIPE_SPEED = 4
        self.PIPE_DISTANCE = 2000

        self.MAX_BG_SPEED = 5
        self.bg_speed = 1
        
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        
        self.background = background.Background(self.WIDTH, self.HEIGHT)
        
        self.pipes : list = []
        self.flock : list = []
        
        self.running = True
        self.blit_hitboxes = False
    
    def setup(self, bird_count : int = 1) -> None:
        sp.run("clear", shell=True)
        
        pg.display.set_caption("ML")
        
        pg.time.set_timer(pg.USEREVENT + 1, self.PIPE_DISTANCE)
        
        self.create_flock(bird_count)
        
    def handle_events(self) -> list:
        keyque = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return None
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    return None
                
                if event.key == pg.K_h: self.blit_hitboxes = not self.blit_hitboxes
                
                keyque.append(event.key)
                
            if event.type == pg.USEREVENT + 1:
                self.pipes.append(pipe.Pipe(self.WIDTH, self.HEIGHT))
        
        return keyque

    def accelerate(self, n : float, MAX : float, STEP : float, EXPONENT : float = 1) -> float:
        if n >= MAX:
            return MAX
        return min(MAX, n + STEP * EXPONENT)
    
    def create_flock(self, num : int) -> None:
        assert num > 0, "num should be greater than 0"
            
        for i in range(0, num):
            self.flock.append(bird.Bird(self.HEIGHT, 200, i))
    
    def create_pipe(self) -> None:
        self.pipes.append(pipe.Pipe(self.WIDTH, self.HEIGHT))
    
    def draw(self) -> None:
        self.background.draw(self.window)
        
        for bird in self.flock:
            bird.draw(self.window)
            if self.blit_hitboxes:
                bird.draw_hitbox(self.window)
        
        
        for pipe in self.pipes:
            pipe.draw(self.window)
        
        pg.display.flip()
        self.clock.tick(60)
    
    def update(self, keyque : list) -> None:
        for bird in self.flock:
            if bird.update(self.GRAVITY, self.HEIGHT, self.pipes):
                self.flock.remove(bird)
        
        if len(self.flock) > 0:
            self.flock[0].key_events(keyque)
            
        for pipe in self.pipes:
            for bird in self.flock:
                if pipe.update(self.PIPE_SPEED, bird):
                    bird.add_point()
        
        self.bg_speed = self.accelerate(self.bg_speed, 2, 0.02, 1.5)
        self.background.update(self.bg_speed)
    
    def mainloop(self):
        while self.running:
            keyque = self.handle_events()
            
            if pg.K_h in keyque: self.blit_hitboxes = not self.blit_hitboxes
            
            if len(self.flock) == 0:
                self.running = False
                print("All birds are dead")
                return
            
            self.update(keyque)
            self.draw()
            
    def reset(self, bird_count : int = 1) -> None:
        self.pipes = []
        self.flock = []
        
        self.running = True
        
        self.create_flock(bird_count)
    
    def quit(self) -> None:
        pg.quit()
        quit()