import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-talk')

df=pd.read_csv("datos/datos_RC.csv")
frec= df["Freq"]
transferencia = df["amp_out"]/df["amp_in"]
fase = df["fase_out"]

# %% Grafica Tranferencia
fig, ax = plt.subplots(figsize=(10,4))
ax.set_xscale('log')
ax.set_xlabel("Frecuencia [Hz]")
ax.set_ylabel(r"Tranferencia $[V_{out}/V_{in}]$")
ax.minorticks_on()
ax.grid(which='minor',alpha=0.3)
ax.grid(which='major',alpha=1)
ax.scatter(frec,transferencia,c='black',alpha=0.7,zorder=10)
fig.savefig('tranferencia_RC.svg')
plt.tight_layout()
#%% Grafica Fase
fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.set_xscale('log')
ax2.set_xlabel("Frecuencia [Hz]")
ax2.set_ylabel(r"Fase [°]")
ax2.minorticks_on()
ax2.grid(which='minor',alpha=0.3)
ax2.grid(which='major',alpha=1)
ax2.scatter(frec,fase,c='C1',alpha=1,zorder=10)
fig2.savefig('fase_RC.svg')
plt.tight_layout()
#%%