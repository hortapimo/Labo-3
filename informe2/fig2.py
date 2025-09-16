import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 12})

# 1. Definimos la función para el ajuste
def funcion_ajuste(x, A, tau):
    """
    Función de ajuste del tipo: f(x) = A * (1 - e^(-x/tau))
    """
    return A * (1 - np.exp(-x / tau))

def funcion_ajuste_descarga(x, A, tau):

    return A * (np.exp(-x / tau))

ruta_archivo ='data/817omh_T1_23Ciclos.txt'
def graficarHistogramas(N, ruta_archivo,ax,rango, bins=7):
    try:
        df = pd.read_csv(ruta_archivo, header=None, sep=',')
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en la ruta: {ruta_archivo}")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        
    j=0
    TausCargas = []
    TausDescargas = []
    
    for i in range(N):
        tiempoCarga = df.iloc[j:j+79, 0]*1e3
        voltajeCarga = df.iloc[j:j+79, 2]
        tiempoDescarga = df.iloc[j+80:j+159, 0]*1e3
        voltajeDescarga = df.iloc[j+80:j+159, 2]
        j=j+160
        
        p0_inicial_carga = [np.max(voltajeCarga), 80]
        p0_inicial_descarga = [np.max(voltajeDescarga), 80]
        
        popt, pcov = curve_fit(funcion_ajuste, tiempoCarga, voltajeCarga, p0=p0_inicial_carga)
        A_opt, tau_carga = popt
        TausCargas.append(tau_carga)
        
        popt, pcov = curve_fit(funcion_ajuste_descarga, tiempoDescarga, voltajeDescarga, p0=p0_inicial_descarga)
        A_opt, tau_descarga = popt
        TausDescargas.append(tau_descarga)
        
        
    mediaCarga = np.mean(TausCargas)
    stdCarga = np.std(TausCargas)
    mediaDescarga = np.mean(TausDescargas)
    stdDescarg = np.std(TausDescargas)
    
    ax.hist(TausCargas, density=True,bins = bins,facecolor='#36BBA7', alpha=1, label =r"$\tau$ cargas"+"\n"+r"$\mu =$"+f"{mediaCarga:.2f}ms, "+r"$\sigma =$"+f"{stdCarga:.3f}ms")
    ax.hist(TausDescargas, density=True, bins=bins, facecolor='#FF2056', alpha=1, label =r"$\tau$ descargas"+"\n"+r"$\mu =$"+f"{mediaDescarga:.2f}ms, "+r"$\sigma =$"+f"{stdDescarg:.3f}ms")
    ax.set_xlim(rango)
    ax.grid(which = 'major')
    ax.minorticks_on()
    ax.grid(which = 'minor', alpha = 0.3)
    ax.legend()
    # ax.set_ylabel("Ocurrencias [%]")
    # ax.set_xlabel("Tiempo [ms]")
    
    print(f"media de carga {np.mean(TausCargas):.2f}, y desvio: {np.std(TausCargas):.3f}")
    print(f"media de descarga {np.mean(TausDescargas):.2f}, y desvio: {np.std(TausDescargas):.3f}")


fig, ax= plt.subplots(nrows = 2,ncols=2)

ruta_archivo ='data/317omh_T1_7Ciclos.txt'
graficarHistogramas(7,ruta_archivo, ax[0,0], (31.75,32))
ax[0,0].set_title("R = 317 ohm, # mediciones:7")
ax[0,0].set_ylabel("Ocurrencias [%]")

ruta_archivo ='data/517omh_T1_16_ciclos.txt'
graficarHistogramas(13,ruta_archivo, ax[0,1], (51,52))
ax[0,1].set_title("R = 517 ohm, # mediciones:13")

ruta_archivo ='data/817omh_T1_23Ciclos.txt'
graficarHistogramas(5,ruta_archivo, ax[1,0], (80,80.7))
ax[1,0].set_title("R = 817 ohm, # mediciones:5")
ax[1,0].set_ylabel("Ocurrencias [%]")
ax[1,0].set_xlabel("Tiempo [ms]")

ruta_archivo ='data/1017omh_T1_6ciclos.txt'
graficarHistogramas(18,ruta_archivo, ax[1,1], (98.75,100.25))
ax[1,1].set_title("R = 1017 ohm, # mediciones:18")
ax[1,1].set_xlabel("Tiempo [ms]")





