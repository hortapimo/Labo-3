import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

desvio = np.array([134.47531520030944,92.44295139946844,93.01631937470859,37.21105796008442])
picoPico=np.array([1640,1300,800])

pendientesNormalizadas=desvio/picoPico

f=np.array([])

fig,ax=plt.subplots(figsize=(8,6))
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.scatter(f,pendientesNormalizadas, c="black", alpha=0.8,zorder=4)
ax.grid(which="major")
ax.minorticks_on()
ax.grid(which="minor",alpha=0.3)
ax.set_xlabel("Frecuencia [Hz]")
ax.set_ylabel("Pendiente normalizada [1/ms]")
plt.tight_layout()
fig.savefig("curvapendientes.svg")
