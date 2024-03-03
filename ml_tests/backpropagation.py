import matplotlib.pyplot as plt
import math, sys

def bigboy(bias3value : float, data : dict[float, float], do_draw = False) -> dict:
    w1 = lambda x : x * 3.32
    w2 = lambda x : x * -3.53
    w3 = lambda x : x * -1.22
    w4 = lambda x : x * -2.30

    b1 = lambda x : x + -1.43
    b2 = lambda x : x + 0.57
    b3 = lambda x : x + bias3value

    top_f = lambda x : math.log(1 + math.exp(x)) # soft pluss (>_<)
    bottom_f = lambda x : math.log(1 + math.exp(x))

    states = {}
    final_points = []
    x = 0
    while x <= 1:
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
            states[x] = {
                "predicted" : b3(in_x + in_y),
                "observed" : data[x],
            }
        
        x = round(x + 0.1, 1) # round to avoid floating point errors

    if do_draw:
        plt.plot(data.keys(), data.values(), "bo")
        plt.plot([point[0] for point in final_points], [point[1] for point in final_points], "b")
        plt.show()

    return states


def lossfunc(states : list[dict], points : dict[float, float]) -> float:
    ssqr = 0
    dssqr = 0
    for pointx, observed in points.items():
        state = states[pointx]
        
        ssqr += (observed - state["predicted"]) **2
        dssqr += (observed - state["predicted"]) * -2 
        
        
    return (dssqr, ssqr)
        
data = {0 : 0, 0.5 : 1, 1 : 0}

xl = []
yl = []
learning_rate = 0.1
max_iterations = 1000

bias = 0
while True:
    states = bigboy(bias, data)
    loss, ssqr = lossfunc(states, data)
    
    step_size = loss * learning_rate
    if abs(step_size) < 0.001 or max_iterations == 0: break
    
    xl.append(bias)
    yl.append(ssqr)
    
    bias += - step_size
    max_iterations -= 1
    
    bigboy(bias, data, True)

print("bias: ", bias)

plt.plot(xl, yl)
plt.show()