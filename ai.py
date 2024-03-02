import matplotlib.pyplot as plt
import math, sys

def bigboy(bias3value : float = 0) -> float:
    sqr = lambda observed, predicted : (observed - predicted)**2

    data = {0 : 0, 0.5 : 1, 1 : 0}

    w1 = lambda x : x * 3.32
    w2 = lambda x : x * -3.53
    w3 = lambda x : x * -1.22
    w4 = lambda x : x * -2.30

    b1 = lambda x : x + -1.43
    b2 = lambda x : x + 0.57
    b3 = lambda x : x + bias3value

    top_f = lambda x : math.log(1 + math.exp(x)) # soft pluss (>_<)
    bottom_f = lambda x : math.log(1 + math.exp(x))

    residuals = []
    final_points = []
    x = 0
    while x <= 1:
        x = round(x, 1)
        in_x = w1(x)
        in_x = b1(in_x)
        in_x = top_f(in_x)
        in_x = w3(in_x)
        
        in_y = w2(x)
        in_y = b2(in_y)
        in_y = bottom_f(in_y)
        in_y = w4(in_y)
        
        final_points.append((x, b3(in_x + in_y)))
        if x in data.keys():
            residuals.append(sqr(data[x], b3(in_x + in_y)))
        
        x += 0.1

    #plt.plot(data.keys(), data.values(), "ro")
    #plt.plot([point[0] for point in final_points], [point[1] for point in final_points], "b")
    #plt.show()

    #plt.plot(b3(0), sum(residuals), "ro")
    #plt.show()
    
    return sum(residuals)

arr = []
arr2 = []
x = 0
while x <= 5:
    print(bigboy(x))
    
    arr.append(x)
    arr2.append(bigboy(x))
    
    x = round(x + 0.1, 1)

plt.plot(arr, arr2, "ro")
plt.show()