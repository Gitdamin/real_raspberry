import numpy as np
from numpy import cos
from numpy import pi
from matplotlib import pyplot as plt
import matplotlib.cm as cm

# parameters
f = 10
time_step = 0.01
num_sample = int(1/time_step)
t = np.arange(0, 1, time_step) # 수정
row = 100
col = 100

A = [1, 3, 5, 7, 9]
B = [100, 200, 300, 400, 500]
plt.plot(A, B, 'r--')
plt.title("test1")
plt.xlabel('A')
plt.ylabel('B')
plt.show()
