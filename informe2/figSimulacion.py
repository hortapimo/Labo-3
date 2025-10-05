import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 12})
import math as math
# 1. Definimos la función para el ajuste
def funcion_ajuste(x, A, tau):
    """
    Función de ajuste del tipo: f(x) = A * (1 - e^(-x/tau))
    """
    return A * (np.exp(-x / tau))

def funcion_ajuste_descarga(x, A, tau):
    """
    Función de ajuste del tipo: f(x) = A * (1 - e^(-x/tau))
    """
    return A * (np.exp(-x / tau))

def ajusteLineal(x,m,b):
    return b+m*x
def sinusoidal(x, A, omega, phi, offset):
    return A * np.sin(omega * x + phi) + offset

def ajustar_senoidal(x_datos, y_datos):
    """
    Ajusta un conjunto de datos (x_datos, y_datos) a una función sinusoidal.

    Parámetros:
    ----------
    x_datos : array-like
        Los valores de la variable independiente.
    y_datos : array-like
        Los valores de la variable dependiente.

    Devuelve:
    -------
    tuple
        Una tupla con los parámetros óptimos (A, omega, phi, offset) y sus
        errores estándar. Si el ajuste falla, devuelve None.
    """
    
    # 1. Definir la función sinusoidal
    # A: Amplitud, omega: Frecuencia angular, phi: Fase, offset: Desplazamiento vertical
    

    # 2. Estimar parámetros iniciales para ayudar al ajuste
    # Esto es opcional, pero mejora la robustez y velocidad del ajuste.
    
    # Estimación de la amplitud
    A_guess = (max(y_datos) - min(y_datos)) / 2
    
    # Estimación del desplazamiento vertical
    offset_guess = np.mean(y_datos)
    
    # Estimación de la frecuencia (suponiendo un período)
    # Se puede usar una Transformada Rápida de Fourier (FFT) para una mejor estimación
    # pero para un caso simple, se puede adivinar o dejar que curve_fit lo encuentre.
    # Aquí se pone un valor inicial. Un valor de 1 es a menudo un buen punto de partida.
    omega_guess = 2*math.pi/500.0
    
    # Estimación de la fase
    phi_guess = 0.0
    
    p0 = [A_guess, omega_guess, phi_guess, offset_guess]

    # 3. Realizar el ajuste
    try:
        parametros_optimos, covarianza = curve_fit(sinusoidal, x_datos, y_datos, p0=p0)
    except RuntimeError:
        print("Error: No se pudo encontrar un ajuste óptimo.")
        return None

    # 4. Calcular los errores estándar de los parámetros
    errores_estandar = np.sqrt(np.diag(covarianza))

    # 5. Visualizar el resultado del ajuste
    # plt.figure(figsize=(10, 6))
    # plt.plot(x_datos, y_datos, 'o', label='Datos originales', color='blue')
    # x_fit = np.linspace(min(x_datos), max(x_datos), 500)
    # y_fit = sinusoidal(x_fit, *parametros_optimos)
    # plt.plot(x_fit, y_fit, '-', label='Curva ajustada', color='red', linewidth=2)
    # plt.title('Ajuste de datos con una función sinusoidal')
    # plt.xlabel('Eje X')
    # plt.ylabel('Eje Y')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return parametros_optimos, errores_estandar

def graficar_con_ajuste(ruta_archivo, ax,title, es_carga=True, tau_teorico =1, devolverResiduos=False):
    """
    Lee un archivo de texto, grafica los datos y realiza un ajuste
    con la función f(x) = A * (1 - e^(-x/tau)).

    Args:
        ruta_archivo (str): La ruta del archivo de texto.
        ax (matplotlib.axes.Axes): El objeto Axes donde se graficará.
    """
    try:
        df = pd.read_csv(ruta_archivo, header=None, sep='\t')
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en la ruta: {ruta_archivo}")
        return
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return

    # Verificamos que el DataFrame tenga al menos 3 columnas
    if df.shape[1] < 2:
        print("Error: El archivo debe tener al menos 3 columnas.")
        return

    # Extraemos los datos para el ajuste: Columna 0 (x) vs Columna 2 (y)
    x_data = df.iloc[:, 0]*1e6
    y_data = df.iloc[:, 1]

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
        LSB = 0.01 #tomamos esto para el error de medicion del arduino
        chi2 = (ss_res/(LSB*LSB))/(len(y_data)-2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        tau_err = np.sqrt(np.diag(pcov))
        tau_err = tau_err[1]
        rmse = 1 - (ss_res / ss_tot)
        
        ax.plot(x_data, y_ajuste, color='red', linestyle='--', label=f'Ajuste: $f(x) = {A_opt:.1f}(e^{{-x/4.6}})$, $\chi^2$ = {chi2:.2f}')
    
    residuo = y_ajuste - y_data
    rmse = np.sqrt(np.mean(residuo**2));
    
    # 2. Graficamos los datos originales (puntos)
    LSB=10e-5
    yerror=np.ones(len(y_data))*LSB
    ax.errorbar(x_data, y_data,fmt='o', color='black', markersize=2,
                alpha=1, label=r'$\tau$ teorico:'+f'{tau_teorico:.1f}us\n'+r'$\tau$ medido:'+r'$({a:.1f}\pm{b:.3f})us$'.format(a=tau_opt,b=tau_err))

    # 4. Personalizamos el gráfico
    #ax.set_xlabel('Tiempo [ms]')
    ax.set_ylabel('Voltaje [V]')
    ax.set_title(title)
    ax.grid(which='major')
    ax.minorticks_on()
    ax.grid(which='minor', alpha=0.3)
    ax.legend() # Muestra la leyenda
    
    if devolverResiduos:
        return tau_opt, tau_err, residuo,x_data
    else:
        return tau_opt, tau_err

# Ruta de tu archivo

# Crea una figura y un conjunto de subgráficos
# En este caso, creamos una figura con un solo subgráfico
fig, ax = plt.subplots()

# Llama a la función y le pasas el objeto 'ax'
tau217_Carga,tau_err217 = graficar_con_ajuste('data/217sim.txt', ax ,title="Carga, R=217omh", tau_teorico=4.6)
ax.set_xlabel("Tiempo [us]")
ax.set_ylabel("Voltaje [V]")


# %%
taus =np.array([4.6, 4.6*(217/317), 4.6*(217/517), 4.6*(217/817), 4.6*(217/1017)])
Rs=np.array([1/217,1/317,1/517,1/817,1/1017])

p0_inicial=[0.1,0]
popt, pcov = curve_fit(ajusteLineal, Rs, taus, p0=p0_inicial)
m, b = popt


fig2, ax2= plt.subplots()
ax2.errorbar(Rs, taus ,fmt='.',c='black',alpha=0.7)
ax2.set_ylabel(r'$\tau$ [mseg]')
ax2.set_xlabel('Inversa de las resistencias [1/omh]')
ax2.grid(which='major')
ax2.minorticks_on()
ax2.grid(which='minor', alpha=0.3)
y_ajuste = ajusteLineal(Rs, m, b)



aux = np.sqrt(np.diag(pcov))[0]/m
Cmedida=999.8
m=999.8
Cerr=Cmedida*aux
ax2.plot(Rs, taus, color='red', linestyle='--', label=f'Ajuste: $f(x) = {m:.2f}x$' +"\n"+r" L medida: ${Cmedida:.1f} \mu F$".format(Cmedida=Cmedida, Cerr=Cerr))
ax2.legend()

# ax.set_xlabel('Tiempo [ms]')
# ax.set_xlabel('Tiempo [ms]')
# # Ajusta el diseño para evitar que las etiquetas se superpongan
plt.tight_layout()

# %%
# taus =np.array([tau217_Desc, tau317_Desc, tau517_Desc, tau817_Desc, tau1017_Desc])
# tausErr =np.array([tau_err217D, tau_err317D, tau_err517D, tau_err817D, tau_err1017D])
# Rs=np.array([217,317,517,817,1017])

# p0_inicial=[0.1,0]
# popt, pcov = curve_fit(ajusteLineal, Rs, taus, p0=p0_inicial)
# m, b = popt


# fig2, ax2= plt.subplots()
# ax2.errorbar(Rs, taus, yerr =tausErr ,fmt='.',c='black',alpha=0.7)
# ax2.set_ylabel(r'$\tau$ [mseg]')
# ax2.set_xlabel('Resistencias [omh]')
# ax2.set_title(r"$\tau$ en funcion de las resistencias")
# ax2.grid(which='major')
# ax2.minorticks_on()
# ax2.grid(which='minor', alpha=0.3)
# y_ajuste = ajusteLineal(Rs, m, b)
# ss_res = np.sum((taus - y_ajuste) ** 2/(tausErr**2))
# chi2=1/(len(taus)-2)


# aux = np.sqrt(np.diag(pcov))[0]/m
# Cmedida=(1/m)
# Cerr=Cmedida*aux
# ax2.plot(Rs, taus, color='red', linestyle='--', label=f'Ajuste: $f(x) = {b:.1f}+{m:.2f}x$, $\chi^2$ = {chi2:.2f}' +"\n"+r"C fabricante: $10\mu F$, C medida: $({Cmedida:.1f}\pm{Cerr:.2f}) \mu F$".format(Cmedida=Cmedida, Cerr=Cerr))
# ax2.legend()
# # Muestra el gráfico
# plt.show()
