import matplotlib.pyplot as plt

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def residual(self, slope, intercept):
        return self.y - (intercept + slope * self.x)
    
    def square_residual(self, slope, intercept):
        return (self.y - (intercept + slope * self.x))**2
    
    def derivative_intercept(self, slope, intercept):
        return -2 * (self.y - (intercept + slope * self.x))
    
    def derivative_slope(self, slope, intercept):
        return -2 * self.x * (self.y - (intercept + slope * self.x))
        
class Points():
    def __init__(self, points : list[Point]) -> None:
        self.points = points
    
    def residuals(self, slope, intercept):
        return [point.residual(slope, intercept) for point in self.points]
    
    def square_residuals(self, slope, intercept):
        return [point.square_residual(slope, intercept) for point in self.points]
    
    def derivative_intercept(self, slope, intercept):
        return [point.derivative_intercept(slope, intercept) for point in self.points]
    
    def derivative_slope(self, slope, intercept):
        return [point.derivative_slope(slope, intercept) for point in self.points]


points = Points([Point(0.5, 1.4), Point(2.3, 1.9), Point(2.9, 3.2), Point(4.2, 3.8)])

a1 = []
i1 = []

intercept = 0
slope = 1
learning_rate = 0.01
max_iterations = 10000
while True:
    a1.append(sum(points.square_residuals(slope, intercept)))
    i1.append(intercept)
    
    step_size_intercept = sum(points.derivative_intercept(slope, intercept)) * learning_rate
    step_size_slope = sum(points.derivative_slope(slope, intercept)) * learning_rate
    
    if abs(step_size_intercept) < 0.0001 or max_iterations == 0: break
    
    intercept += -step_size_intercept
    slope += -step_size_slope
    max_iterations -= 1
    
print("slope: ", slope)
print("intercept: ", intercept)
print("iterations left: ", max_iterations)

a2 = []
i2 = []
intercept = 0
while intercept <= 2:
    a2.append(sum(points.square_residuals(0.64, intercept)))
    i2.append(intercept)
    
    intercept += 0.1

plt.plot(i2, a2)
plt.plot(i1, a1, "r")
plt.ylabel('sum of square residuals')
plt.xlabel('intercept')
plt.show()