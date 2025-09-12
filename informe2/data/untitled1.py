import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Modelo del tipo: f(t) = b * (1 - exp(-t/a))
def modelo_crecimiento(t, a, b):
    return b * (1 - np.exp(-t / a))

# Leer el archivo
nombre_archivo = '217Carga.txt'  # Cambia este nombre si es necesario

# Cargar los datos (suponiendo que no hay encabezados)
datos = np.loadtxt(nombre_archivo, delimiter=',')

# Extraer columna 1 (tiempo t) y columna 3 (f(t))
t = datos[:, 0]*1e3
f_t = datos[:, 2]

# Ajustar el modelo a los datos
parametros, _ = curve_fit(modelo_crecimiento, t, f_t, p0=[1, max(f_t)])  # p0 es la estimación inicial
a, b = parametros

# Generar datos ajustados para graficar la curva suave
t_fit = np.linspace(min(t), max(t), 500)
f_fit = modelo_crecimiento(t_fit, a, b)

# Graficar datos y curva ajustada
plt.figure(figsize=(8, 6))
plt.scatter(t, f_t, label='Datos\n Tau teorico: 22 ms\n Tau obtenido: 23 ms', color='blue')
plt.plot(t_fit, f_fit, label=f'Ajuste: f(t) = {b:.3f}(1 - exp(-t/{a:.3f}))', color='red')
plt.xlabel('Tiempo [ms]')
plt.ylabel('Voltaje [V]')
plt.title('Ajuste a f(t) = b(1 - exp(-t/a))')
plt.legend()
plt.grid(True)
plt.minorticks_on()
plt.grid(which='minor', alpha=0.3)
plt.tight_layout()
plt.show()
