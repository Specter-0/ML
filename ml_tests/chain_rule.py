import matplotlib.pyplot as plt
import math

class Graph():
    def __init__(self, points : list[tuple[float, float]] = []) -> None:
        self.points = points
        self.x : list[float] = []
        self.y : list[float] = []
    
    def step(self, x, y):
        self.x.append(x)
        self.y.append(y)
        
    def residuals(self, slope, intercept):
        return [point[1] - (intercept + slope * point[0]) for point in self.points]
    
    def plot(self):
        plt.plot(self.x, self.y)
    
    def scatter(self):
        if len(self.points) == 0:
            print("No points to scatter")
            return
        
        plt.scatter([point[0] for point in self.points], [point[1] for point in self.points])
        
        
f = lambda x, slope = 1, intercept = 0 : x * slope + intercept

hw = Graph([(1, 2.1), (1.5, 1)])


weight = 0
intercept = 0
while weight <= 3:
    hw.step(weight, f(weight, 1, intercept))
    weight += 0.01

residuals = Graph([])

intercept = 0
print(sum(hw.residuals(1, intercept)))
while intercept <= 3:
    residuals.points.append((intercept, sum(hw.residuals(1, intercept))))
    intercept += 0.1
    
hw.plot()
hw.scatter()
plt.xlabel("time since last snack")
plt.ylabel("craves ice cream")
plt.show()

residuals.scatter()
plt.xlabel("intercept")
plt.ylabel("Residual")
plt.show()

Squared_residuals = Graph([(point[0], point[1]**2) for point in residuals.points])

Squared_residuals.scatter()
plt.xlabel("Residual")
plt.ylabel("Squared Residual")
plt.show()