import matplotlib.pyplot as plt
import numpy as np
import math

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
        
    def __str__(self) -> str:
        return f""" 
    w1: {self.w1(1)} \n
    w2: {self.w2(1)} \n
    w3: {self.w3(1)} \n
    w4: {self.w4(1)} \n
    b1: {self.b1(1)} \n
    b2: {self.b2(1)} \n
    b3: {self.b3(1)} 
        """

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
    
    def plot(self, names : list[str] = None, types : list[str] = ["b"], render_points : bool = False):
        if names == None:
            names = self.chart.keys()
        
        for index, name in enumerate(names):
            plt.plot(self.chart[name]["x"], self.chart[name]["y"], types[index] if len(types) > index else types[0])
        
        if render_points:
            plt.plot(self.points.keys(), self.points.values(), "bo")
        
        plt.show(block=False)
        plt.pause(0.03)
        plt.close()

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
   
   
vb3 = mynet.b3(0)
vw3 = mynet.w3(1)
vw4 = mynet.w4(1)
optimized = [False, False, False]

 
while not all(optimized):
    vb3, vw3, vw4, optimized = step(vb3, vw3, vw4, optimized)
    print("vb3:", vb3, "\n")
    print("vw3:", vw3, "\n")
    print("vw4:", vw4, "\n")
    print("optimized:", optimized, "\n")
    
    graph = EzGraph(mynet.points)
    lx, ly = mynet.traverse(0, 1.0, 0.01)
    graph.from_list(lx, ly, "predicted")
    graph.plot(render_points=True)
    
    
    

print(mynet)
graph = EzGraph(mynet.points)
lx, ly = mynet.traverse(0, 1.0, 0.01)
graph.from_list(lx, ly, "predicted")
graph.plot(render_points=True)