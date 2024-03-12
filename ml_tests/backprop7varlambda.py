import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Generator
import numpy as np
import math, sys, time

plt.style.use('fivethirtyeight')

class NeuralNetwork():
    def __init__(self, points : dict[float, float]) -> None:
        self.points = points

        # weight top before activation function
        self.weight_tb = 3.32
        self.bias_tb = -1.43
        
        # weight bottom before activation function
        self.weight_bb = -3.53
        self.bias_bb = 0.57
        
        # weight top after activation function
        self.weight_ta = -1.22
        
        # weight bottom after activation function
        self.weight_ba = -2.30
        
        self.bias_sum = 2.60
        
    def __call__(self, x : float) -> float:
        in_1 = self.weight_tb * x
        in_1 = self.bias_tb + in_1
        in_1 = self.soft_pluss(in_1)
        in_1 = self.weight_ta * in_1
        
        in_2 = self.weight_bb * x
        in_2 = self.bias_bb + in_2
        in_2 = self.soft_pluss(in_2)
        in_2 = self.weight_ba * in_2
        
        return self.bias_sum + (in_1 + in_2)
    
    def parts(self, x):
        in_1 = self.weight_tb * x
        xt = self.bias_tb + in_1
        yt = self.soft_pluss(xt)
        
        in_2 = self.weight_bb * x
        xb = self.bias_bb + in_2
        yb = self.soft_pluss(xb)
        
        return (xt, xb, yt, yb)
    
    def fparts(self, x): # full parts
        in_1 = self.weight_tb * x
        in_1 = self.bias_tb + in_1
        in_1 = self.soft_pluss(in_1)
        in_1 = self.weight_ta * in_1
        
        in_2 = self.weight_bb * x
        in_2 = self.bias_bb + in_2
        in_2 = self.soft_pluss(in_2)
        in_2 = self.weight_ba * in_2
        
        return (in_1, in_2)
    
    def soft_pluss(self, x : float) -> float:
        return math.log(1 + math.exp(x))
    
    def keypoints(self) -> Generator:
        pindex = 0
        for px, observed in self.points.items():
            predicted = self(px)
            x_top, x_bottom, y_top, y_bottom = self.parts(px)
            
            
            yield ({
                "point_index": pindex,
                "point_x" : px,
                "predicted" : predicted,
                "observed" : observed,
                "x_top" : x_top,
                "x_bottom" : x_bottom,
                "y_top": y_top,
                "y_bottom": y_bottom,
                "snapshot": {
                    "weight_tb": self.weight_tb,
                    "bias_tb": self.bias_tb,
                    "weight_bb": self.weight_bb,
                    "bias_bb": self.bias_bb,
                    "weight_ta": self.weight_ta,
                    "weight_ba": self.weight_ba,
                    "bias_sum": self.bias_sum,
                }
            })
            
            pindex += 1
            
    def train(self, *args) -> Generator:
        stuff = [(func, value, False) for func, value in args]
        
        iterations = 0
        while True:
            states = list(self.keypoints())
            
            index = 0
            for func, value, should_break in stuff:
                if not should_break:
                    value, should_break = func(value, states)
                    
                    stuff[index] = (func, value, should_break)
                
                index += 1
                    
            if all([should_break for _, _, should_break in stuff]):
                break
            
            yield list(np.linspace(0, 1, 20, endpoint=True)), [self(x) for x in np.linspace(0, 1, 20, endpoint=True)], zip(*[self.fparts(x) for x in np.linspace(0, 1, 20, endpoint=True)])
                
            iterations += 1
            if iterations >= 150000:
                print("Training took too long")
                break
        
        print(f"Training took {iterations} iterations")
    
    def train_value(self, lossfunc, to_set, value, states) -> bool:
        loss = 0
        for state in states:
            loss += lossfunc(state)
            
        value, should_break = self.gradient_descent(value, loss, 0.1, 0.000001)
        
        match to_set:
            case "bias_tb":
                self.bias_tb = value
            
            case "bias_bb":
                self.bias_bb = value
            
            case "bias_sum":
                self.bias_sum = value
                
            case "weight_tb":
                self.weight_tb = value
            
            case "weight_bb":
                self.weight_bb = value
            
            case "weight_ta":
                self.weight_ta = value
            
            case "weight_ba":
                self.weight_ba = value
        
        return value, should_break
            
    
    def gradient_descent(self, value, loss, learning_rate, precision) -> None:
        step_size = loss * learning_rate
        
        value += -step_size
        
        return value, abs(step_size) < precision
   
class EzGraph():
    def __init__(self, points : dict[float, float]) -> None:
        self.chart : dict = {}
        self.points = points
        
    def add(self, name):
        fig, ax = plt.subplots()
        line1 = ax.plot([], [], lw=2)[0]
        
        line2 = ax.plot([], [], lw=2)[0]
        line3 = ax.plot([], [], lw=2)[0]
        
        self.chart[name] = {"fig" : fig, "ax" : ax, "line1" : line1, "line2" : line2, "line3" : line3, "anim": None}
        
    
    def animate(self, name : str, frames, interval : int, xlim : tuple[float, float] = None, ylim : tuple[float, float] = None):
        def animate(state):
            lx, lin_1, lin_2, ly  = state
            
            self.chart[name]["line1"].set_data(lx, ly)
            self.chart[name]["line2"].set_data(lx, lin_1)
            self.chart[name]["line3"].set_data(lx, lin_2)
            
            return self.chart[name]["line1"], self.chart[name]["line2"], self.chart[name]["line3"]
        
        def init():
            if xlim: self.chart[name]["ax"].set_xlim(*xlim)
            if ylim: self.chart[name]["ax"].set_ylim(*ylim)
            
            return self.chart[name]["line1"], self.chart[name]["line2"], self.chart[name]["line3"]
        
        self.chart[name]["anim"] = FuncAnimation(
            self.chart[name]["fig"], 
            animate, 
            frames=frames, 
            interval=interval, 
            init_func=init, 
            blit=True, 
            repeat=False, 
            cache_frame_data=False
        )
    
    def plot_points(self):
        plt.plot(self.points.keys(), self.points.values(), "bo")
        
    def show(self):
        plt.show()   
     
mynet = NeuralNetwork({0 : 0, 0.5 : 1, 1 : 0})

mynet.bias_sum = 0
mynet.weight_ta = np.random.normal(0, 1) # good inital: -0.8290545550281081
mynet.weight_ba = np.random.normal(0, 1) # good inital: -0.30741573319052634
mynet.weight_tb = np.random.normal(0, 1) # good inital: -1.0270867453610253
mynet.weight_bb = np.random.normal(0, 1) # good inital: 3.080315916964262
mynet.bias_bb = 0
mynet.bias_tb = 0

print(f""" variables
weight_ta: {mynet.weight_ta}
weight_ba: {mynet.weight_ba}
weight_tb: {mynet.weight_tb}
weight_bb: {mynet.weight_bb}
""")

lx, ly, lpy1_2 = zip(*list(mynet.train( 
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]), "bias_sum", value, states), mynet.bias_sum),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["y_top"], "weight_ta", value, states), mynet.weight_ta),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["y_bottom"], "weight_ba", value, states), mynet.weight_ba),
    
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ta"] * (np.exp(state["x_top"]) / (1 + np.exp(state["x_top"]))) * state["point_x"], "weight_tb", value, states), mynet.weight_tb),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ta"] * (np.exp(state["x_top"]) / (1 + np.exp(state["x_top"]))) * 1, "bias_tb", value, states), mynet.bias_tb),
    
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ba"] * (np.exp(state["x_bottom"]) / (1 + np.exp(state["x_bottom"]))) * state["point_x"], "weight_bb", value, states), mynet.weight_bb),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ba"] * (np.exp(state["x_bottom"]) / (1 + np.exp(state["x_bottom"]))) * 1, "bias_bb", value, states), mynet.bias_bb),
)))
lpy1, lpy2 = zip(*lpy1_2)

ff = [(x, lpy1[index], lpy2[index], ly[index]) for index, x in enumerate(lx)]

graph = EzGraph(mynet.points)
graph.add("main")
graph.animate("main", frames=ff, interval=10, xlim=(-0.1, 1.1), ylim=(-3, 2.1))
graph.plot_points()
graph.show()

print(f""" variables

weight_tb:  {mynet.weight_tb}
bias_tb:    {mynet.bias_tb}

weight_bb:   {mynet.weight_bb}
bias_bb:   {mynet.bias_bb}

weight_ta:  {mynet.weight_ta}

weight_ba:  {mynet.weight_ba}

bias_sum:   {mynet.bias_sum}

""")