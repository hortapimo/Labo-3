# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 10:19:27 2020

@author: User
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os
from IPython import get_ipython


#%% ------------------------ Elegir modo de salida de los gráficos -----------------------------------
'''
Descomentar la línea que corresponda. 
Si quieren que las figuras aparezcan en la terminal: inline 
Si quieren que las figuras aparezcan en una ventana emergente: qt5
'''
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt5')

#%% ---------------------- Carga de datos ---------------------------------------


# Colocar la ruta de la carpeta con los archivos entre r' ':
#os.chdir (r'C:\Descargas')

# Nombre del archivo a analizar entre ' ' con la terminación .txt incluida:
file1 = '217.txt'

'''
Con np.loadtxt(ruta) podemos cargar los datos de una matriz guardada en un
archivo de texto como un array de numpy. Cada renglón es una fila.
Las columnas están separadas por una coma. Eso lo indicamos en el "delimiter".
Con skiprows=1 le pedimos que se saltee la primer fila, que tiene los títulos.
'''
Misdatos = np.loadtxt(file1, delimiter=",",skiprows=1) 

# argsort retorna los indices resultantes de ordernar de forma creciente, en este caso, Misdatos[:,2]

Misdatos1 = Misdatos[np.argsort(Misdatos[:, 2])]

'''
Armamos arrays(vectores) con las columnas de mi archivo:
'''

y0 = Misdatos1[:,0] #valores de tau
errory0 = Misdatos1[:,1] #incertidumbre de tau
x0 = Misdatos1[:,2] #valores de R


#%% ----------------------------- Gráfico de los datos crudos-----------------------

errorx0 = Misdatos1[:,3] #valores de incertidumbre de R
plt.ion() # Activa el modo interactivo del gráfico.

plt.close('all') # Cierro los gráficos abiertos por si había alguno.

# Grafico los datos del archivo
plt.figure(1)
plt.errorbar(x0,y0,xerr=errorx0,yerr=errory0,fmt=".b")

# En la siguiente linea podemos especificar los rangos de las escalas
#plt.axis([0,2,0,3.5])

plt.xlabel('Resistencia (ohm)');
plt.ylabel('Tau (s)');
plt.show()

print('Chequeamos que el comportamiento de Tau vs R sea lineal antes de realizar el ajuste')

#%% ----------------------------- Ajuste por cuadrados minimos con incertezas -----------------------


#%%
# Ajuste por cuadrados minimos ponderado con incertidumbres en y, w son los pesos asociados a cada valor y
w = 1/errory0
X = sm.add_constant(x0)
wls_model = sm.WLS(y0,X, weights=w) # Realiza el ajuste con el peso w
results = wls_model.fit() # Genera los parametros

o,C = results.params # Guardamos los parametros ajustados en las variables o y C

# Caluclo del intervalo de confianza para ordenada al origen y pendiente
oint,Cint = results.conf_int(alpha=0.05) # intervalos de confianza para o y C

deltaC=abs((Cint[1]-Cint[0])/2) # Error de C
deltao= abs((oint[1]-oint[0])/2) # Error de o

print("C=(", C," +/- ",deltaC,") F")
print("ordenada al origen=(", o," +/- ",deltao,") V")

# Calculo las bandas de confianza y predicción
from statsmodels.stats.outliers_influence import summary_table
from statsmodels.sandbox.regression.predstd import wls_prediction_std

st, data, ss2 = summary_table(results, alpha=0.05)

fittedvalues = data[:, 2] #resultado de los valores ajustados
predict_mean_ci_low, predict_mean_ci_upp = data[:, 4:6].T #bandas de confianza
prstd, iv_l, iv_u = wls_prediction_std(results,alpha=0.05) #bandas de predicción con P>0.95

#%% ----------------------------- Gráfico de datos con ajuste y bandas -----------------------

plt.figure(2)
plt.errorbar(x0,y0,xerr=errorx0,yerr=errory0,fmt=".b") # Grafico valores medidos

plt.xlabel('Resistencia(Ohm)');
plt.ylabel('Tau(s)');
plt.plot(x0, fittedvalues, '-', lw=1) #grafico de la recta de ajuste
plt.plot(x0, iv_l, 'r--', lw=2) #banda de predicción inferior
plt.plot(x0, iv_u, 'r--', lw=2) #banda de predicción superior
plt.plot(x0, predict_mean_ci_low, 'g--', lw=1) #banda de confianza inferior
plt.plot(x0, predict_mean_ci_upp, 'g--', lw=1) #banda de confianza superior
titulo=('RC transitorio, C = ('+ str(round(C,8))+" +/- "+ str(round(deltaC,8))+") F")
plt.title(titulo)

