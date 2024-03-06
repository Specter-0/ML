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
            
    def train(self, *kwargs) -> None:
        stuff = [(func, value, False) for func, value in kwargs]
        
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
                
            iterations += 1
            if iterations >= 200000:
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
        
mynet = NeuralNetwork({0 : 0, 0.5 : 1, 1 : 0})

mynet.bias_sum = 0
mynet.weight_ta = np.random.normal(0, 1)
mynet.weight_ba = np.random.normal(0, 1)
mynet.weight_tb = np.random.normal(0, 1)
mynet.weight_bb = np.random.normal(0, 1)
mynet.bias_bb = 0
mynet.bias_tb = 0

mynet.train(
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]), "bias_sum", value, states), mynet.bias_sum),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["y_top"], "weight_ta", value, states), mynet.weight_ta),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["y_bottom"], "weight_ba", value, states), mynet.weight_ba),
    
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ta"] * (np.exp(state["x_top"]) / (1 + np.exp(state["x_top"]))) * state["point_x"], "weight_tb", value, states), mynet.weight_tb),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ta"] * (np.exp(state["x_top"]) / (1 + np.exp(state["x_top"]))) * 1, "bias_tb", value, states), mynet.bias_tb),
    
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ba"] * (np.exp(state["x_bottom"]) / (1 + np.exp(state["x_bottom"]))) * state["point_x"], "weight_bb", value, states), mynet.weight_bb),
    (lambda value, states : mynet.train_value(lambda state : -2 * (state["observed"] - state["predicted"]) * state["snapshot"]["weight_ba"] * (np.exp(state["x_bottom"]) / (1 + np.exp(state["x_bottom"]))) * 1, "bias_bb", value, states), mynet.bias_bb),
)

lx = []
ly = []
ly1 = []
ly2 = []
for x in np.linspace(0, 1, 100, endpoint=True):
    lx.append(x)
    ly.append(mynet(x))
    ly1.append(mynet.parts(x)[2] * mynet.weight_ta)
    ly2.append(mynet.parts(x)[3] * mynet.weight_ba)

plt.plot(lx, ly)
plt.plot(lx, ly1)
plt.plot(lx, ly2)
plt.scatter(mynet.points.keys(), mynet.points.values(), c="r")
plt.show()

print(f""" variables

weight_tb: should be 3.32 is {mynet.weight_tb}
bias_tb: should be -1.43 is {mynet.bias_tb}

weight_bb: should be -3.53 is {mynet.weight_bb}
bias_bb: should be 0.57 is {mynet.bias_bb}

weight_ta: should be -1.22 is {mynet.weight_ta}

weight_ba: should be -2.30 is {mynet.weight_ba}

bias_sum: should be 2.60 is {mynet.bias_sum}

""")