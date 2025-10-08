import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn-v0_8-talk")
# Reemplaza 'tu_archivo.csv' con la ruta a tu archivo



def plotear(file):
    df = pd.read_csv(file,header=None)

    # escala1=df[]
    # escala2=df[]
    CH1=df[4]*1e3
    CH2=df[10]*1e3
    time=(df[3]+abs(df[3][0]))*1e3

    fig,ax=plt.subplots(figsize=(12,5))
    ax.scatter(time,CH1,c="C0",s=8,zorder=10)
    ax.set_ylabel("Señal Emitida[mV]")
    ax2 = ax.twinx()
    ax2.scatter(time,CH2,c="C1",s=8,zorder=12)
    ax2.set_ylabel("Señal Recibida [mV]")
    ax.set_xlabel("Tiempo [ms]")
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor",alpha=0.3)
        
    plt.tight_layout()

#%%
plotear("datos/der100hz.csv")
plotear("datos/der300hz,70_sym.csv")
plotear("datos/der300hz,90_sym.csv")

#%%