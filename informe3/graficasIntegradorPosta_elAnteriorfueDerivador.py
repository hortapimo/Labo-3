import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("seaborn-talk")

def plotear(file,ax,ax2,fin=1,inicio=0):
    df = pd.read_csv(file,header=None)
    CH1=df[4]*1e3
    CH2=df[10]*1e3
    time=(df[3]+abs(df[3][0]))*1e3
    fin = int(len(CH1)//fin)
    ax.scatter(time[:fin],CH1[inicio:fin],c="C0",s=8,zorder=10)   
    ax2.scatter(time[:fin],CH2[inicio:fin],c="C1",s=8,zorder=12)
    
    plt.tight_layout()


#%%
def formatear(ax,ax2,onlabelI=True,onlabelD=True):
    if onlabelI:
        ax.set_ylabel("Señal Emitida[mV]")
        
    if onlabelD:
        ax2.set_ylabel("Señal Recibida [mV]")
    ax.set_xlabel("Tiempo [ms]")
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor",alpha=0.3)

# plotear("datos/der100hz.csv",ax,ax2)

fig3,ax3=plt.subplots(figsize=(5,3))
ax4 = ax3.twinx()
formatear(ax3,ax4,onlabelD=False)
plotear("datos/int22500hz,RC.csv",ax3,ax4)


fig3,ax3=plt.subplots(figsize=(5,3))
ax4 = ax3.twinx()
formatear(ax3,ax4,onlabelI=False, onlabelD=False)
plotear("datos/int7500hz,RC.csv",ax3,ax4,fin=1.3, inicio = 0)

fig5,ax5=plt.subplots(figsize=(5,3))
ax6 = ax5.twinx()
formatear(ax5,ax6,onlabelI=False)
plotear("datos/int3500hz,RC.csv",ax5,ax6,fin=3)
