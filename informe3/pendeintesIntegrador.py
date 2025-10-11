import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.style.use("seaborn-talk")

def ajuste(y,m,b):
    return m*y+b

def plotear(file,ax,ax2,fin=-1,inicio=0,plotear=True):
    df = pd.read_csv(file,header=None)
    CH1=df[4]*1e3
    CH2=df[10]*1e3
    time=(df[3]+abs(df[3][0]))*1e3

    if plotear:
        ax.scatter(time[inicio:fin],CH1[inicio:fin],c="darkblue",s=8,zorder=5)   
        ax2.scatter(time[inicio:fin],CH2[inicio:fin],c="gray",alpha=1,s=8,zorder=6)
    plt.tight_layout()
    return (time, CH1, CH2)

fig,ax=plt.subplots(figsize=(6,6))
ax2=ax.twinx()
fin=-890
inicio=1290
time, CH1, CH2=plotear("datos/int3500hz,RC.csv",ax,ax2,fin=fin, inicio=inicio)
#%%
m,cov = curve_fit(ajuste,time[inicio:fin],CH2[inicio:fin])
desvio=np.sqrt(cov[1][1])
ax2.plot(time, ajuste(time,m[0],m[1]), c="red", label=f"Ajuste:\n$({m[0]:.0f}\pm{desvio:.0f})\cdot x+({m[1]:.1f})$",zorder=10)
ax.grid(which="major")
ax2.set_ylabel("Señal Recibida [mV]")
ax.set_ylabel("Señal Emitida[mV]")
ax.set_xlabel("Tiempo [ms]")
ax.minorticks_on()
ax2.legend()
ax.grid(which="minor", alpha=0.3)
plt.tight_layout()
fig.savefig("ajusteInt.svg")
print(desvio)
#%%