import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Generator
import numpy as np
import math, sys

plt.style.use('fivethirtyeight')

class NeuralNetwork():
    def __init__(self, points : dict[float, float]) -> None:
        self.points = points
        
        self.w1 = lambda x : x * 3.34
        self.w2 = lambda x : x * -3.53
        self.w3 = lambda x : x * np.random.normal(0, 1) 
        self.w4 = lambda x : x * np.random.normal(0, 1) 
        
        self.b1 = lambda x : x + -1.43
        self.b2 = lambda x : x + 0.57
        self.b3 = lambda x : x + 0
        
        self.activation_function_1 = lambda x : math.log(1 + math.exp(x)) # soft pluss (>_<)
        self.activation_function_2 = lambda x : math.log(1 + math.exp(x)) # soft pluss (>_<)
    
    def forward(self, x : float) -> float:
        in_1 = self.w1(x)
        in_1 = self.b1(in_1)
        in_1 = self.activation_function_1(in_1)
        in_1 = self.w3(in_1)
        
        in_2 = self.w2(x)
        in_2 = self.b2(in_2)
        in_2 = self.activation_function_2(in_2)
        in_2 = self.w4(in_2)
        
        return self.b3(in_1 + in_2)

    def halv_forward(self, x : float) -> tuple[float, float]:
        in_1 = self.w1(x)
        in_1 = self.b1(in_1)
        in_1 = self.activation_function_1(in_1)
        in_1 = self.w3(in_1)
        
        in_2 = self.w2(x)
        in_2 = self.b2(in_2)
        in_2 = self.activation_function_2(in_2)
        in_2 = self.w4(in_2)
        
        return (in_1, in_2)
    
    def traverse(self, minx, maxx, step):
        return [x for x in np.arange(minx, maxx + step, step)], [self.forward(x) for x in np.arange(minx, maxx + step, step)]
    
    def traverse_half(self, minx, maxx, step):
        return [x for x in np.arange(minx, maxx + step, step)], [self.halv_forward(x) for x in np.arange(minx, maxx + step, step)]
        
    def __str__(self) -> str:
        return f"""w1: {self.w1(1)} 
w2: {round(self.w2(1), 3)} 
w3: {round(self.w3(1), 3)} 
w4: {round(self.w4(1), 3)} \n
b1: {round(self.b1(1), 3)} 
b2: {round(self.b2(1), 3)} 
b3: {round(self.b3(1), 3)} 
"""

    def config(self) -> str:
        return {
            "w1" : round(self.w1(1), 3),
            "w2" : round(self.w2(1), 3),
            "w3" : round(self.w3(1), 3),
            "w4" : round(self.w4(1), 3),
            "b1" : round(self.b1(0), 3),
            "b2" : round(self.b2(0), 3),
            "b3" : round(self.b3(0), 3),
        }

class EzGraph():
    def __init__(self, points : dict[float, float]) -> None:
        self.chart : dict = {}
        self.points = points
        
    def add(self, name):
        fig, ax = plt.subplots()
        line1 = ax.plot([], [], lw=2)[0]
        line1.set_label("sum + bias3")
        
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
        plt.tight_layout()
        plt.show()

class Poly():
    def __init__(self, xvalues, yvalues, degree) -> None:
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.degree = degree
        
        self.coefficients = np.polyfit(self.xvalues, self.yvalues, self.degree)
    
    def __call__(self, x):
        return np.polyval(self.coefficients, x)

    def traverse(self, minx, maxx, step):
        return [x for x in np.arange(minx, maxx, step)], [self(x) for x in np.arange(minx, maxx, step)]
    
    def values(self, xvalues : list[float]):
        return xvalues, [self(x) for x in xvalues]
    
class GradientDecent():
    def __init__(self, learning_rate : float = 0.1, max_iterations : int = 1000, precision : float = 0.001) -> None:
        self.learning_rate = learning_rate
        self.precision = precision
        self.max_iterations = max_iterations
    
    def __call__(self, value : float, loss : float) -> float:
        step_size = loss * self.learning_rate
        
        value += - step_size
        self.max_iterations -= 1
        return value, (abs(step_size) < self.precision or self.max_iterations == 0)


mynet = NeuralNetwork({0 : 0, 0.5 : 1, 1 : 0})
gdb3 = GradientDecent(max_iterations=1000, precision=0.0001)
gdw3 = GradientDecent(max_iterations=1000, precision=0.0001)
gdw4 = GradientDecent(max_iterations=1000, precision=0.0001)

def step(vb3, vw3, vw4, optimized):
    global mynet
    lx, ly = mynet.traverse(0, 1, 0.1)
    poly = Poly(lx, ly, 2)
    
    if not optimized[0]:
        loss = sum([(observed - predicted) * -2 for observed, predicted in zip(mynet.points.values(), poly.values(mynet.points.keys())[1])])
        
        vb3, should_break = gdb3(vb3, loss)

        mynet.b3 = lambda x : x + vb3
        
        if should_break: optimized[0] = True
        
    if not optimized[1]: 
        loss = 0
        for x, observed in mynet.points.items():
            predicted = poly(x)
            
            in_1 = mynet.w1(x)
            in_1 = mynet.b1(in_1)
            in_1 = mynet.activation_function_1(in_1)
            
            loss += -2 * (observed - predicted) * in_1
        
        vw3, should_break = gdw3(vw3, loss)

        mynet.w3 = lambda x : x * vw3
        
        if should_break: optimized[1] = True

    if not optimized[2]:
        loss = 0
        for x, observed in mynet.points.items():
            predicted = poly(x)
            
            in_2 = mynet.w2(x)
            in_2 = mynet.b2(in_2)
            in_2 = mynet.activation_function_2(in_2)
            
            loss += -2 * (observed - predicted) * in_2
            
        vw4, should_break = gdw4(vw4, loss)
    
        mynet.w4 = lambda x : x * vw4
        
        if should_break: optimized[2] = True
    
    return vb3, vw3, vw4, optimized

def run() -> Generator[tuple[list[float], list[float]], None, None]:
    global mynet
    vb3 = mynet.b3(0)
    vw3 = mynet.w3(1)
    vw4 = mynet.w4(1)
    optimized = [False, False, False]

    while not all(optimized):
        vb3, vw3, vw4, optimized = step(vb3, vw3, vw4, optimized)
        
        x, lxy = mynet.traverse_half(0, 1, 0.01)
        lx, ly = zip(*lxy)
        
        yield (mynet.traverse(0, 1, 0.01), (x, lx, ly))

# shit is for drawing --------------------

f, lin1_2 = zip(*list(run()))

lx, in_1, in_2 = zip(*lin1_2)

ff = []
for index, x in enumerate(lx):
    ff.append((x, in_1[index], in_2[index], f[index][1]))



gre = EzGraph(mynet.points)
gre.add("main")
gre.animate("main", frames=ff, interval=10, xlim=(-0.1, 1.1), ylim=(-3, 1.1))
gre.plot_points()
plt.legend()
gre.show()
    


# --------------------

with open("values.txt", "w") as f:
    f.write(str(mynet))