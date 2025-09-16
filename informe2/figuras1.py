import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# 1. Definimos la función para el ajuste
def funcion_ajuste(x, A, tau):
    """
    Función de ajuste del tipo: f(x) = A * (1 - e^(-x/tau))
    """
    return A * (1 - np.exp(-x / tau))

def funcion_ajuste_descarga(x, A, tau):
    """
    Función de ajuste del tipo: f(x) = A * (1 - e^(-x/tau))
    """
    return A * (np.exp(-x / tau))

def ajusteLineal(x,m,b):
    return b+m*x

def graficar_con_ajuste(ruta_archivo, ax,title, es_carga=True, tau_teorico =1):
    """
    Lee un archivo de texto, grafica los datos y realiza un ajuste
    con la función f(x) = A * (1 - e^(-x/tau)).

    Args:
        ruta_archivo (str): La ruta del archivo de texto.
        ax (matplotlib.axes.Axes): El objeto Axes donde se graficará.
    """
    try:
        df = pd.read_csv(ruta_archivo, header=None, sep=',')
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en la ruta: {ruta_archivo}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return

    # Verificamos que el DataFrame tenga al menos 3 columnas
    if df.shape[1] < 3:
        print("Error: El archivo debe tener al menos 3 columnas.")
        return

    # Extraemos los datos para el ajuste: Columna 0 (x) vs Columna 2 (y)
    x_data = df.iloc[:, 0]*1e3
    y_data = df.iloc[:, 2]

    # Realizamos el ajuste de la curva usando curve_fit
    # Es recomendable proporcionar un valor inicial (p0) para el ajuste.
    # Aquí, A podría ser un valor aproximado del valor máximo de y.
    # tau puede ser un valor inicial para la constante de tiempo.
    p0_inicial = [np.max(y_data), 1.0] # [A_inicial, tau_inicial]
    

    try:
        # curve_fit devuelve los parámetros óptimos (popt) y la matriz de covarianza (pcov)
        if es_carga:
            popt, pcov = curve_fit(funcion_ajuste, x_data, y_data, p0=p0_inicial)
            A_opt, tau_opt = popt
        else:
            p0_inicial = [np.max(y_data), 40.0]
            limites = ([4, 20], [6,150])
            popt, pcov = curve_fit(funcion_ajuste_descarga, x_data, y_data, p0=p0_inicial)
            A_opt, tau_opt = popt
            
        
        
        # Mostramos los parámetros óptimos encontrados
        print(f"Ajuste de la curva realizado con éxito.")
        print(f"Parámetros óptimos:")
        print(f"  A = {A_opt:.4f}")
        print(f"  tau = {tau_opt:.4f}")
        
    except RuntimeError:
        print("Error: No se pudo encontrar un ajuste para los datos.")
        A_opt, tau_opt = np.nan, np.nan # Asignamos NaN si el ajuste falla
    

    # 3. Graficamos la curva de ajuste si el ajuste fue exitoso
    if not np.isnan(A_opt):
        # Creamos una serie de puntos para la curva ajustada
        
        if es_carga:
            y_ajuste = funcion_ajuste(x_data, A_opt, tau_opt)
            
        else:
            y_ajuste = funcion_ajuste_descarga(x_data, A_opt, tau_opt)
        residuo = y_ajuste - y_data
        ss_res = np.sum((y_data - y_ajuste) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        rmse = 1 - (ss_res / ss_tot)
        
        ax.plot(x_data, y_ajuste, color='red', linestyle='--', label=f'Ajuste: $f(x) = {A_opt:.1f}(1-e^{{-x/{tau_opt:.2f}}})$, $R^2$ = {rmse:.2f}')
    
    residuo = y_ajuste - y_data
    rmse = np.sqrt(np.mean(residuo**2));
    
    # 2. Graficamos los datos originales (puntos)
    LSB=5e-5
    yerror=np.ones(len(y_data))*LSB
    ax.errorbar(x_data, y_data,fmt='o', color='black', markersize=2,
                alpha=1, label=r'$\tau$ teorico:'+f'{tau_teorico:.1f}ms\n'+r'$\tau$ medido:'+f'{tau_opt:.1f}ms')

    # 4. Personalizamos el gráfico
    #ax.set_xlabel('Tiempo [ms]')
    ax.set_ylabel('Voltaje [V]')
    ax.set_title(title)
    ax.grid(which='major')
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.3)
    ax.legend() # Muestra la leyenda
    
    return tau_opt
# Ruta de tu archivo

# Crea una figura y un conjunto de subgráficos
# En este caso, creamos una figura con un solo subgráfico
fig, ax = plt.subplots(nrows = 5, ncols=2, figsize=(10, 6))

# Llama a la función y le pasas el objeto 'ax'
tau217_Carga = graficar_con_ajuste(    , ax[0,0],title="Carga, R=217omh", tau_teorico=22)
tau217_Desc = graficar_con_ajuste('data/217Descarga.txt', ax[0,1],title="Descarga, R=217omh", es_carga=False, tau_teorico=22)

tau317_Carga = graficar_con_ajuste('data/317Carga.txt', ax[1,0],title="Carga, R=317omh", tau_teorico=32)
tau217_Desc = graficar_con_ajuste('data/317Descarga.txt', ax[1,1],title="Descarga, R=317omh", es_carga=False, tau_teorico=32)

tau517_Carga = graficar_con_ajuste('data/517Carga.txt', ax[2,0],title="Carga, R=517omh", tau_teorico=52)
tau217_Desc = graficar_con_ajuste('data/517Descarga.txt', ax[2,1],title="Descarga, R=517omh", es_carga=False, tau_teorico=52)

tau817_Carga = graficar_con_ajuste('data/817Carga.txt', ax[3,0],title="Carga, R=817omh", tau_teorico=82)
tau217_Desc = graficar_con_ajuste('data/817Descarga.txt', ax[3,1],title="Descarga, R=817omh", es_carga=False, tau_teorico=82)

tau1017_Carga = graficar_con_ajuste('data/1017Carga.txt', ax[4,0],title="Carga, R=1017omh",tau_teorico=102)
tau217_Desc = graficar_con_ajuste('data/1017Descarga.txt', ax[4,1],title="Descarga, R=1017omh", es_carga=False,tau_teorico=102)
ax[4,1].set_xlabel('Tiempo [ms]')
ax[4,0].set_xlabel('Tiempo [ms]')
# Ajusta el diseño para evitar que las etiquetas se superpongan
plt.tight_layout()

# %%
taus =np.array([tau217_Carga, tau317_Carga, tau517_Carga, tau817_Carga, tau1017_Carga])
Rs=np.array([217,317,517,817,1017])

p0_inicial=[0.1,0]
popt, pcov = curve_fit(ajusteLineal, Rs, taus, p0=p0_inicial)
m, b = popt


fig2, ax2= plt.subplots()
ax2.errorbar(Rs, taus,fmt='o',c='black',alpha=0.7)
ax2.set_ylabel(r'$\tau$ [mseg]')
ax2.set_xlabel('Resistencias [omh]')
ax2.set_title(r"$\tau$ en funcion de las resistencias")
ax2.grid(which='major')
ax2.minorticks_on()
ax2.grid(which='minor', alpha=0.3)
y_ajuste = ajusteLineal(Rs, m, b)
ss_res = np.sum((taus - y_ajuste) ** 2)
ss_tot = np.sum((taus - np.mean(taus)) ** 2)
rmse = 1 - (ss_res / ss_tot)

ax2.plot(Rs, taus, color='red', linestyle='--', label=f'Ajuste: $f(x) = {b:.1f}+{m:.2f}x$, $R^2$ = {rmse:.2f}')
ax2.legend()
# Muestra el gráfico
plt.show()
# %%

