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
        
        self.bsum = 0
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
        snapshot = pd.DataFrame()
        for index in range(len(data)):
            snapshot.append(
                {
                    "species": data["species"][index],
                }
            )
            
    def train(self, data : pd.DataFrame, **kwargs) -> Generator:
        training_points = [(key, func, False) for key, func in kwargs]
        
        while not all([should_break for _, _, should_break in training_points]):
            snapshot = self.snapshot(data)
            
            print(snapshot)
            
            for key, func, should_break in training_points:
                if not should_break:
                    value, should_break = func(value, data)
                    
                    training_points[key] = (key, value, should_break)
            
            # !| yield self.traverse()

mynet = Nn()

training_data = pd.DataFrame(
    {
        "petal": [0.04, 1, 0.50],
        "sepal": [0.42, 0.54, 0.37],
        "species": ["setosa", "virginica", "versicolor"],
        "probability": [None, None, None],
        "cross_entropy": [None, None, None],
    }
)



frames = list(mynet.train(training_data,
    bsum = lambda x : x
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

plt.show()