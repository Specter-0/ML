import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button, Slider
import math, sys
import random as rn
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
        
        return self.ReLU(ssumed), self.ReLU(vsumed), self.ReLU(visummed)
        
    
    def ReLU(self, x : float) -> float:
        return max(0, x)
    
    def soft_pluss(self, x : float) -> float:
        return math.log(1 + math.exp(x))

mynet = Nn()

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 2)

ax.set_xlabel("in1")
ax.set_ylabel("in2")
ax.set_zlabel("out")

ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

axalp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
alpha_slider = Slider(
    ax=axalp,
    label="Alpha",
    valmin=0,
    valmax=1,
    valinit=0.85,
    orientation="vertical"
)

axX = fig.add_axes([0.25, 0.8, 0.65, 0.03])
X_slider = Slider(
    ax=axX,
    label="X",
    valmin=0,
    valmax=1,
    valinit=0.85,
    orientation="horizontal"
)

axY = fig.add_axes([0.25, 0.9, 0.65, 0.03])
Y_slider = Slider(
    ax=axY,
    label="Y",
    valmin=0,
    valmax=1,
    valinit=0.85,
    orientation="horizontal"
)

valuepoint = [0.5, 0.5, 0.5]

lx2 = np.linspace(0, 1, 30) # //! Change 30 to 10 if you have preformance issues
ly2 = np.linspace(0, 1, 30)
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

surf1 = ax.plot_surface(lx, ly, lz, alpha=0.8, cmap="viridis")
surf2 = ax.plot_surface(lx, ly, lz2, alpha=0.8, cmap="plasma")
surf3 = ax.plot_surface(lx, ly, lz3, alpha=0.8, cmap="inferno")
points = ax.scatter([], [], [], s=1000)
points.set_color([[rn.random(), rn.random(), rn.random()] for _ in range(3)])

def update_alpha(val):
    alpha = alpha_slider.val
    surf1.set_alpha(alpha)
    surf2.set_alpha(alpha)
    surf3.set_alpha(alpha)
    fig.canvas.draw_idle()
    
def update_point(val):
    x = X_slider.val
    y = Y_slider.val
    z1, z2, z3 = mynet(x, y)
    points._offsets3d = ([x, x, x], [y, y, y], [z1, z2, z3])

alpha_slider.on_changed(update_alpha)
X_slider.on_changed(update_point)
Y_slider.on_changed(update_point)

plt.show()