import matplotlib.pyplot as plt

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def residual(self, slope, intercept):
        return self.y - (intercept + slope * self.x)
        
class Points():
    def __init__(self, points : list[Point]) -> None:
        self.points = points
    
    def residuals(self, slope, intercept):
        return [point.residual(slope, intercept) for point in self.points]
    
    def square_residuals(self, slope, intercept):
        return [residual**2 for residual in self.residuals(slope, intercept)]
    
    def derivative_square_residuals(self, slope, intercept):
        return [-2 * residual for residual in self.residuals(slope, intercept)]


points = Points([Point(0.5, 1.4), Point(2.3, 1.9), Point(2.9, 3.2)])

a1 = []
i1 = []

intercept = 0
learning_rate = 0.01
max_iterations = 1000
while True:
    a1.append(sum(points.square_residuals(0.64, intercept)))
    i1.append(intercept)
    
    step_size = sum(points.derivative_square_residuals(0.64, intercept)) * learning_rate
    print(step_size, sum(points.derivative_square_residuals(0.64, intercept)), intercept)
    
    if abs(step_size) < 0.001 or max_iterations == 0: break
    
    intercept += -step_size
    max_iterations -= 1

a2 = []
i2 = []
intercept = 0
while intercept <= 2:
    a2.append(sum(points.square_residuals(0.64, intercept)))
    i2.append(intercept)
    
    intercept += 0.1

plt.plot(i2, a2)
plt.plot(i1, a1, "ro")
plt.ylabel('sum of square residuals')
plt.xlabel('intercept')
plt.show()