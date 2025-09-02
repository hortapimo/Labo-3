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

def cargar_datos_npy(nombre_archivo):
    """
    Carga un array de NumPy desde un archivo .npy.
    
    Args:
        nombre_archivo (str): La ruta del archivo .npy que se va a cargar.
        
    Returns:
        np.ndarray: El array de NumPy cargado.
    """
    try:
        datos = np.load(nombre_archivo)
        print(f"Datos cargados exitosamente desde '{nombre_archivo}'.")
        return datos
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo: {e}")
        return None
escala=1500
chanel1_0gr = cargar_datos_npy('ch1_0grd.npy')*(escala/255)-escala/2
chanel1_45gr = cargar_datos_npy('ch1_45grd.npy')*(escala/255)-escala/2
chanel1_90gr = cargar_datos_npy('ch1_90grd.npy')*(escala/255)-escala/2
chanel1_180gr = cargar_datos_npy('ch1_180grd.npy')*(escala/255)-escala/2

chanel2_0gr = cargar_datos_npy('ch2_0grd.npy')*(escala/255)-escala/2
chanel2_45gr = cargar_datos_npy('ch2_45grd.npy')*(escala/255)-escala/2
chanel2_90gr = cargar_datos_npy('ch2_90grd.npy')*(escala/255)-escala/2
chanel2_180gr = cargar_datos_npy('ch2_180grd.npy')*(escala/255)-escala/2

def style(ax):
    ax.minorticks_on()
    ax.grid(which='major')
    ax.grid(which='minor',alpha=0.3)
    ax.set_ylabel("Voltaje [mV]")
    ax.set_xlabel("Voltaje [mV]")
 
h=8
w=9
       
fig, ax = plt.subplots(2, 2,figsize=(w, h))
style(ax[0,0])
ax[0,0].set_title(f"Desfase teorico de: 0 grados")
ax[0,0].plot(chanel1_0gr, chanel2_0gr)

style(ax[0,1])
ax[0,1].set_title(f"Desfase teorico de: 45 grados")
ax[0,1].plot(chanel1_45gr, chanel2_45gr)

style(ax[1,0])
ax[1,0].set_title(f"Desfase teorico de: 90 grados")
ax[1,0].plot(chanel1_90gr, chanel2_90gr)

style(ax[1,1])
ax[1,1].set_title(f"Desfase teorico de: 180 grados")
ax[1,1].plot(chanel1_180gr, chanel2_180gr)


