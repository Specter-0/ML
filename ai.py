import matplotlib.pyplot as plt
import math, sys
import numpy as np

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
        
        self.sw3 = 1.5
        
        self.bsum = 0
    
    def __call__(self, in1 : float, in2 : float) -> float:
        px = self.pw1 * in1
        psx = self.sw1 * in2
        
        psum = (px + psx) + self.pbsum
        
        sx = self.sw1 * in2
        spx = self.pw2 * in1
        
        ssum = (sx + spx) + self.sbsum
        
        py = self.ReLU(psum)
        sy = self.ReLU(ssum)
        
        py = self.pw3 * py
        sy = self.sw3 * sy
        
        sumed = py + sy + self.bsum
        
        return self.ReLU(sumed)
    
    def parts(self, in1 : float, in2 : float) -> float:
        px = self.pw1 * in1
        psx = self.sw1 * in2
        
        psum = (px + psx) + self.pbsum
        
        sx = self.sw1 * in2
        spx = self.pw2 * in1
        
        ssum = (sx + spx) + self.sbsum
        
        py = self.ReLU(psum)
        sy = self.ReLU(ssum)
        
        return py, sy
        
    
    def ReLU(self, x : float) -> float:
        return max(0, x)
    
    def soft_pluss(self, x : float) -> float:
        return math.log(1 + math.exp(x))

mynet = Nn()

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 2)

ax.set_xlabel("in1")
ax.set_ylabel("in2")
ax.set_zlabel("out")

print(mynet(0, 0))

lx = []
ly = []
lz = []
lpz1 = []
lpz2 = []
for x in list(np.linspace(0, 1, 10)):
    for y in list(np.linspace(0, 1, 10)):
        lx.append(x)
        ly.append(y)
        lz.append(mynet(x, y))
        p1, p2 = mynet.parts(x, y)
        lpz1.append(p1)
        lpz2.append(p2)

ax.scatter(lx, ly, lz, color="red", s=100)
ax.scatter(lx, ly, lpz1, color="blue", s=100)
ax.scatter(lx, ly, lpz2, color="yellow", s=100)
plt.show()