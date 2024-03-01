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

intercept = 0
learning_rate = 0.1
max_iterations = 1000
while True:
    a1.append(sum(points.square_residuals(0.64, intercept)))
    
    step_size = sum(points.derivative_square_residuals(0.64, intercept)) * learning_rate
    print(step_size, sum(points.derivative_square_residuals(0.64, intercept)), intercept)
    
    if abs(step_size) < 0.01 or max_iterations == 0: break
    
    intercept += -step_size
    max_iterations -= 1


plt.plot(a1, "ro")
plt.plot(a1)

plt.ylabel('sum of square residuals')
plt.xlabel('intercept')
plt.show()