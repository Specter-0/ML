import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from typing import Generator
import math, sys
import random as rn
import numpy as np
import pandas as pd

plt.style.use('fivethirtyeight')

class Nn:
    def __init__(self) -> None:
        self.pw1 = -2.5
        self.pw2 = -1.5
        self.pbsum = 1.6
        
        self.sw1 = 0.6
        self.sw2 = 0.4
        self.sbsum = 0.7
        
        self.pw3 = -0.1
        self.pw4 = 2.4
        self.pw5 = -2.2
        
        self.sw3 = 1.5
        self.sw4 = -5.2
        self.sw5 = 3.7
        
        self.bsum = 1
        self.bsum2 = 0
        self.bsum3 = 1
    
    def __call__(self, in1 : float, in2 : float) -> float:
        px = self.pw1 * in1
        psx = self.sw1 * in2
        
        psum = (px + psx) + self.pbsum
        
        sx = self.sw1 * in2
        spx = self.pw2 * in1
        
        ssum = (sx + spx) + self.sbsum
        
        py = self.ReLU(psum)
        sy = self.ReLU(ssum)
        
        sp = self.pw3 * py
        ss = self.sw3 * sy
        
        ssumed = sp + ss + self.bsum
        
        vp = self.pw4 * py
        vs = self.sw4 * sy
        
        vsumed = vp + vs + self.bsum2
        
        vip = self.pw5 * py
        vis = self.sw5 * sy
        
        visummed = vip + vis + self.bsum3
        
        s, v, vi = ssumed, vsumed, visummed
        
        return self.soft_max(s, [s, v, vi]), self.soft_max(v, [s, v, vi]), self.soft_max(vi, [s, v, vi])
        
    def ReLU(self, x : float) -> float:
        return max(0, x)
    
    def soft_pluss(self, x : float) -> float:
        return math.log(1 + math.exp(x))
    
    def soft_max(self, x : float, components : list[float]) -> float:
        return math.exp(x) / sum([math.exp(x) for x in components])

    def traverse(self):
        lx2 = np.linspace(0, 1, 10) # //! Change 30 to 10 if you have preformance issues
        ly2 = np.linspace(0, 1, 10)
        lx, ly = np.meshgrid(lx2, ly2)

        lz = []
        lz2 = []
        lz3 = []
        for x in lx2:
            for y in ly2:
                y1, y2, y3 = mynet(x, y)
                lz.append(y1)
                lz2.append(y2)
                lz3.append(y3)

        # Convert lz and lz2 to 2D arrays
        lz = np.array(lz).reshape(lx.shape)
        lz2 = np.array(lz2).reshape(lx.shape)
        lz3 = np.array(lz3).reshape(lx.shape)
        
        return lx, ly, lz, lz2, lz3

    def snapshot(self, data) -> Generator:
        snapshot = {
            "values": {
                "pw1": self.pw1,
                "pw2": self.pw2,
                "pbsum": self.pbsum,
                "sw1": self.sw1,
                "sw2": self.sw2,
                "sbsum": self.sbsum,
                "pw3": self.pw3,
                "pw4": self.pw4,
                "pw5": self.pw5,
                "sw3": self.sw3,
                "sw4": self.sw4,
                "sw5": self.sw5,
                "bsum": self.bsum,
                "bsum2": self.bsum2,
                "bsum3": self.bsum3,
            }
        }
        for index, species in enumerate(data["species"].tolist()):
            row = data.iloc[index]
            snapshot[species] = {
                "petal": row["petal"],
                "sepal": row["sepal"],
                "predicted": self(row["petal"], row["sepal"])
            }

        return snapshot
            
    def train(self, data : pd.DataFrame, **kwargs) -> Generator:
        training_points = {key : (func, False) for key, func in kwargs.items()}
        
        iterations = 0
        while not all([should_break[1] for should_break in list(training_points.values())]):
            snapshot = self.snapshot(data)
            
            for key, values in training_points.items():
                func, should_break = values 
                
                if not should_break:
                    loss = func(snapshot)
                    
                    value, should_break = self.gradient_descent(snapshot["values"][key], loss, 0.1, 0.000001)
        
                    match key:
                        case "pw1":
                            self.pw1 = value
                        
                        case "pw2":
                            self.pw2 = value
                        
                        case "pw3":
                            self.pw3 = value
                            
                        case "pw4":
                            self.pw4 = value
                        
                        case "pw5":
                            self.pw5 = value
                            
                        case "sw1":
                            self.sw1 = value
                        
                        case "sw2":
                            self.sw2 = value
                        
                        case "sw3":
                            self.sw3 = value
                            
                        case "sw4":
                            self.sw4 = value
                        
                        case "sw5":
                            self.sw5 = value
                        
                        case "pbsum":
                            self.pbsum = value
                            
                        case "sbsum":
                            self.sbsum = value
                            
                        case "bsum":
                            self.bsum = value
                            
                        case "bsum2":
                            self.bsum = value
                            
                        case "bsum3":
                            self.bsum = value
                    
                    training_points[key] = (func, should_break)
            
            yield self.traverse()
            
            iterations += 1
            if iterations >= 150000:
                print("Training took too long")
                break
        
        print(f"Training took {iterations} iterations")
    
    def gradient_descent(self, value, loss, learning_rate, precision) -> None:
        step_size = loss * learning_rate
        
        print(f"step_size: {step_size}, value: {value}, loss: {loss}")
        
        value += -step_size
        
        return value, abs(step_size) < precision

mynet = Nn()

training_data = pd.DataFrame(
    {
        "petal": [0.04, 1, 0.50],
        "sepal": [0.42, 0.54, 0.37],
        "species": ["setosa", "virginica", "versicolor"],
    }
)


frames = list(mynet.train(training_data,
    bsum = lambda snapshot : snapshot["setosa"]["predicted"][0] - 1 + snapshot["setosa"]["predicted"][0] + snapshot["setosa"]["predicted"][0]
))

# //* drawing

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

ax.set_xlabel("in1")
ax.set_ylabel("in2")
ax.set_zlabel("out")

ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

def animate(state):
    for item in ax.collections:
        item.remove()
    
    lx, ly, lz1, lz2, lz3  = state
    
    surf1 = ax.plot_surface(lx, ly, lz1, alpha=0.8, cmap="viridis")
    surf2 = ax.plot_surface(lx, ly, lz2, alpha=0.8, cmap="plasma")
    surf3 = ax.plot_surface(lx, ly, lz3, alpha=0.8, cmap="inferno")
    
    return surf1, surf2, surf3

anim = FuncAnimation(
    fig, 
    animate, 
    frames=frames, 
    interval=40, 
    repeat=False, 
    cache_frame_data=False
)

print(mynet.bsum)
plt.show()