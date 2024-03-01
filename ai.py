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

points = Points([Point(0.5, 1.4), Point(2.3, 1.9), Point(2.9, 3.2)])

tpp = []
intercept = 0
while intercept <= 2:
    tpp.append(sum(points.square_residuals(0.64, intercept)))
    intercept += 0.2

plt.plot(tpp, "ro")
plt.plot(tpp)
plt.ylabel('sum of square residuals')
plt.xlabel('intercept')
plt.show()