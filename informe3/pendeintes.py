import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pendientes = np.array([0.10773280626576565,
    3.818619531970567,
    17.446201384782213,
    88.91230614409427,
    755.1643773684146,
    1876.1273287757485,
    3808.92768882451,
    6739.706681978024,
    10780.301959548558,
    13232.812994332073])
picoPico=np.array([19,27*2,90,180,360,540,720,860,960,1100])

pendientesNormalizadas=pendientes/picoPico

f=np.array([100,300,500,1000,2000,3000,4000,5000,6000,7000])

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
