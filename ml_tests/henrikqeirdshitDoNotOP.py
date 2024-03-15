import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
points = {0:0, 0.5: 0.2, 1: 0}
print("hei")
class NN:
    def __init__(self, points : dict):
        self.w1 =-0.8290545550281081 #-1.0270867453610253 #np.random.normal(0, 1)
        self.w2 =3.080315916964262 #3.080315916964262 #np.random.normal(0, 1)
        self.w3 =-0.8290545550281081 #-0.8290545550281081 #np.random.normal(0, 1)
        self.w4 =-0.30741573319052634 #-0.30741573319052634 #np.random.normal(0, 1)
        self.b1 = 0
        self.b2 = 0
        self.b3 = 0

        self.lr = 0.1

        self.points = points
        self.running = []
        self.totres = 0

    def softplus(self, x):
        return np.log(1 + np.exp(x))
    
    def predict(self, x,):
        y = self.softplus((x * self.w1) + self.b1) * self.w3
        y_2 = self.softplus((x * self.w2) + self.b2) * self.w4 
        out = (y+y_2) + self.b3
        return out
    
    def calc_new_value(self, old_value, who) -> float:
       
        loss = 0
        for x, observed in self.points.items():

            unique = self.unique(who, x)
            predicted = self.predict(x)

            loss += -2 * (observed - predicted) * unique
        stepsize = loss * self.lr
        if abs(stepsize) < 0.000001:
            self.running.append(who)

        new_value = old_value - stepsize
        return new_value
    
    def unique(self, who, x):
        if who == "w1":
            
            return self.w3 * ((np.exp(x*self.w1+self.b1))/(np.exp(x*self.w1+self.b1)+1)) * x
        elif who == "w2":
            
            return self.w4 * ((np.exp(x*self.w2+self.b2))/(np.exp(x*self.w2+self.b2)+1)) * x
        elif who == "w3":
            
            return self.softplus((x * self.w1) + self.b1)
        elif who == "w4":
            
            return self.softplus((x * self.w2) + self.b2)
        elif who == "b1":
            
            return self.w3 * ((np.exp(x*self.w1+self.b1))/(np.exp(x*self.w1+self.b1)+1))
        elif who == "b2":
            
            return self.w4 * ((np.exp(x*self.w2+self.b2))/(np.exp(x*self.w2+self.b2)+1))
        elif who == "b3":
            
            return 1
   
    def get_graph_data(self):
        ly = []
        lx = []
        for x in list(np.linspace(0, 1, 100, endpoint=True)):
            y1 = self.softplus((x * self.w1) + self.b1) * self.w3
            y2 = self.softplus((x * self.w2) + self.b2) * self.w4 
            out = (y1 + y2) + self.b3
            ly.append(out)
            lx.append(x)
    
        return lx, ly


    def plot(self):
        dosage = 0
        y = []
        y2 = []
        skuigy = []
        x_list = []
        while dosage < 1:
            x = self.softplus((dosage * self.w1) + self.b1) * self.w3
            x1 = self.softplus((dosage * self.w2) + self.b2) * self.w4 
            x2 = (x+x1) + self.b3
            y.append(x)
            y2.append(x1)
            skuigy.append(x2)
            x_list.append(dosage)
            dosage += 0.01
        
        for object in self.points:
            plt.scatter(object, self.points[object])
        plt.plot(x_list, y, label="top")
        plt.plot(x_list, y2, label="bottom")
        plt.plot(x_list, skuigy, label="skuigy")

        plt.legend()
        plt.show()

dashit = NN(points)
graph_states = []
i = 0
while len(dashit.running) != 7:
    dashit.running = []
    i += 1
    w1 = dashit.calc_new_value(dashit.w1, "w1")
    w2 = dashit.calc_new_value(dashit.w2, "w2")
    w3 = dashit.calc_new_value(dashit.w3, "w3")
    w4 = dashit.calc_new_value(dashit.w4, "w4")
    b1 = dashit.calc_new_value(dashit.b1, "b1")
    b2 = dashit.calc_new_value(dashit.b2, "b2")
    b3 = dashit.calc_new_value(dashit.b3, "b3")

    dashit.w1 = w1
    dashit.w2 = w2
    dashit.w3 = w3
    dashit.w4 = w4
    dashit.b1 = b1
    dashit.b2 = b2
    dashit.b3 = b3
    
    
    graph_states.append(dashit.get_graph_data())
    if i > 20000:
        dashit = NN(points)
        i = 0
        graph_states = []
print(i, "training cycles")
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, 1)
    return line,

def update(state):
    x_list, y_list = state
    line.set_data(x_list, y_list)
    return line,

ani = animation.FuncAnimation(fig, update, frames=graph_states, init_func=init, interval=40, blit=True, repeat=False)

dashit.plot()
plt.show()