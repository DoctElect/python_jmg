import numpy as np 
import matplotlib.pyplot as plt

l1 = 10
l2 = 7

x = []
y = []
for teta1 in range(0,100,5):
    for teta2 in range(-100,100,5):
        x.append(l1*np.cos(teta1/100)+l2*np.cos(teta1/100+teta2/100))
        y.append(l1*np.sin(teta1/100)+l2*np.sin(teta1/100+teta2/100))


plt.plot(y,x, 'o')
plt.show()