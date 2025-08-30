import numpy as np
import matplotlib.pyplot as plt

# Ajustar el tamaño global de las fuentes
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 14  # Tamaño de la fuente para todos los elementos
plt.rcParams['axes.titlesize'] = 17  # Solo para títulos de ejes
plt.rcParams['axes.labelsize'] = 14  # Solo para etiquetas de ejes
plt.rcParams['xtick.labelsize'] = 15 # Solo para etiquetas del eje X
plt.rcParams['ytick.labelsize'] = 15  # Solo para etiquetas del eje Y
plt.rcParams['legend.fontsize'] = 12 # Solo para la leyenda

def leer_datos_completos(nombre_archivo):

    try:
        datos = np.genfromtxt(nombre_archivo, delimiter=',')
        return datos
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo '{nombre_archivo}': {e}")
        return None

if __name__ == "__main__":

    datos1 = leer_datos_completos('G1_datos_0x01')
    if datos1 is not None:
        tiempo1 = datos1[:, 0]
        voltaje_prescale_1 = datos1[:, 1]

    datos2 = leer_datos_completos('G1_datos_0x02')
    if datos2 is not None:
        tiempo2 = datos2[:, 0]
        voltaje_prescale_2 = datos2[:, 1]

    datos3 = leer_datos_completos('G1_datos_0x03')
    if datos3 is not None:
        tiempo3 = datos3[:, 0]
        voltaje_prescale_3 = datos3[:, 1]

    datos4 = leer_datos_completos('G1_datos_0x04')
    if datos4 is not None:
        tiempo4 = datos4[:, 0]
        voltaje_prescale_4 = datos4[:, 1]

    h=7
    w=14
    fig1, ax1 = plt.subplots(figsize=(w, h))
    fig2, ax2 = plt.subplots(figsize=(w, h))
    fig3, ax3 = plt.subplots(figsize=(w, h))
    fig4, ax4 = plt.subplots(figsize=(w, h))

    
    def style(ax):
        ax.minorticks_on()
        ax.grid(which='major')
        ax.grid(which='minor',alpha=0.3)
        ax.set_ylabel("Voltaje [mV]")
        ax.set_xlabel(f"Tiempo [$\mu$seg]")
        
    style(ax1)
    ax1.plot(tiempo1*1e6, voltaje_prescale_1*1e3)
    ax1.scatter(tiempo1*1e6, voltaje_prescale_1*1e3,
                s=10, c="black", zorder=2)
    ax1.set_title("Medicion con pre-scaler en 1")
    
    style(ax2)   
    ax2.plot(tiempo2*1e6, voltaje_prescale_2*1e3)
    ax2.scatter(tiempo2*1e6, voltaje_prescale_2*1e3,
                s=10, c="black", zorder=2)
    ax2.set_title("Medicion con pre-scaler en 2")
    
    style(ax3)   
    ax3.plot(tiempo3*1e6, voltaje_prescale_3*1e3)
    ax3.scatter(tiempo3*1e6, voltaje_prescale_3*1e3,
                s=10, c="black", zorder=2)
    ax3.set_title("Medicion con pre-scaler en 3")
    
    style(ax4)           
    ax4.plot(tiempo4*1e6, voltaje_prescale_4*1e3)
    ax4.scatter(tiempo4*1e6, voltaje_prescale_4*1e3,
                s=10, c="black", zorder=2)
    ax4.set_title("Medicion con pre-scaler en 4")