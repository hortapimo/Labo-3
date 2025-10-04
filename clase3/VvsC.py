import numpy as np

import matplotlib.pyplot as plt
from scipy.stats import linregress

voltaje = [1,2,3,4,5,6,7,8,9,10]
corriente = np.array([0.009,0.01804,0.0276,0.0378,0.0474,0.0571,0.0669,0.0769,0.0871,0.0981])

fig, ax =plt.subplots()

ax.scatter(corriente*1e3,voltaje)
ax.set_xlabel("Corriente [mA]")
ax.set_ylabel("Voltaje [V]")
ax.grid()

slope, intercept, r_value, p_value, std_err = linregress(corriente, voltaje)

ax.plot(corriente*1e3,corriente*slope + intercept, c="black", label = "- Regresion lineal, pendiente= 101,3 ohm \n- Valor medido de R = 98.1 ohm")
ax.legend()
print(f"The slope of the linear regression is: {slope}")