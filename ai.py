import matplotlib.pyplot as plt
import numpy as np
import math

class NeuralNetwork():
    def __init__(self, points : dict[float, float]) -> None:
        self.points = points
        
        self.w1 = lambda x : x * 3.34
        self.w2 = lambda x : x * -3.53
        self.w3 = lambda x : x * 0.36 # should be np.random.normal(0, 1) for real testing
        self.w4 = lambda x : x * 0.63 # should be np.random.normal(0, 1) for real testing
        
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
        
        in_2 = self.w2(x)
        in_2 = self.b2(in_2)
        in_2 = self.activation_function_2(in_2)
        
        return (in_1, in_2)
    
    def traverse(self, minx, maxx, step):
        return [x for x in np.arange(minx, maxx, step)], [self.forward(x) for x in np.arange(minx, maxx, step)]
        

class EzGraph():
    def __init__(self, points : dict[float, float]) -> None:
        self.chart : dict[str, dict[str, list[float]]] = {}
        self.points = points
    
    def append(self, x, y, name):
        if name not in self.chart.keys():
            self.chart[name] = {"x" : [], "y" : []}
        
        self.chart[name]["x"].append(x)
        self.chart[name]["y"].append(y)
    
    def from_list(self, x : list[float], y : list[float], name : str):
        self.chart[name] = {"x" : x, "y" : y}
    
    def plot(self, names : list[str], types : list[str] = ["b"], render_points : bool = False):
        for index, name in enumerate(names):
            plt.plot(self.chart[name]["x"], self.chart[name]["y"], types[index] if len(types) > index else types[0])
        
        if render_points:
            plt.plot(self.points.keys(), self.points.values(), "bo")
        
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
    
    def __call__(self, value, poly : Poly) -> float:
        loss = sum([(observed - predicted) * -2 for observed, predicted in zip(mynet.points.values(), poly.values(mynet.points.keys())[1])])
        
        step_size = loss * self.learning_rate
        
        value += - step_size
        self.max_iterations -= 1
        
        return value, (abs(step_size) < self.precision or self.max_iterations == 0)

mynet = NeuralNetwork({0 : 0, 0.5 : 1, 1 : 0})

graph = EzGraph(mynet.points)

gd = GradientDecent(max_iterations=100, precision=0.001)
v = 0
while True:
    lx, ly = mynet.traverse(0, 1, 0.1)
    poly = Poly(lx, ly, 2)
    
    v, should_break = gd(v, poly)
   
    mynet.b3 = lambda x : x + v
    
    if should_break: break

gd = GradientDecent(max_iterations=100, precision=0.001)
v = mynet.w3(1)
while True:
    lx, ly = mynet.traverse(0, 1, 0.1)
    poly = Poly(lx, ly, 2)
    
    v, should_break = gd(v, poly)
   
    mynet.w3 = lambda x : x * v
    
    if should_break: break
    
gd = GradientDecent(max_iterations=100, precision=0.001)
v = mynet.w4(1)
while True:
    lx, ly = mynet.traverse(0, 1, 0.1)
    poly = Poly(lx, ly, 2)
    
    v, should_break = gd(v, poly)
   
    mynet.w4 = lambda x : x * v
    
    if should_break: break

lx, ly = mynet.traverse(0, 1, 0.1)
poly = Poly(lx, ly, 2)

print("b3: ", mynet.b3(0))
print("w3: ", mynet.w3(1))
print("w4: ", mynet.w4(1))


graph.from_list(lx, ly, "neural network")
graph.plot(["neural network"], ["b"], True)