poj´ñimport pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt


# inicializo comunicacion con equipos
rm = visa.ResourceManager()
#lista de dispositivos conectados, para ver las id de los equipos
print(rm.list_resources())

#%% Generador de funciones AFG1022

#inicializo generador de funciones
fungen = rm.open_resource('USB0::0x0699::0x0353::2139465::INSTR')
osci = rm.open_resource('USB0::0x0699::0x0368::C017059::INSTR')

fungen.close()
osci.close()

#%%
frec=1500

amplitud=1
fungen.write(f'SOUR1:FREQ {frec}')
fungen.write(f'SOUR1:VOLT {amplitud}')
fungen.write(f'SOUR1:PHAse 0')

angulo_grados = 180
angulo=angulo_grados *2*np.pi/360

amplitud=1
fungen.write(f'SOUR2:FREQ {frec}')
fungen.write(f'SOUR2:VOLT {amplitud}')
fungen.write(f'SOUR2:PHAse {angulo}')


chanel=1
scale1 = 0.15
osci.write(f"CH{chanel}:SCA {scale1}")

chanel=2
scale2 = 0.15
osci.write(f"CH{chanel}:SCA {scale2}")

ch = 1
osci.write('DATA:SOUR CH{}'.format(ch))

data_ch1 = osci.query_binary_values('CURV?', datatype='B',container=np.array)
numpy.savetxt(data_ch1)
#plt.plot(data)

#le pido los parametros de la pantalla
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';') 
xze
xin
voltaje = (data_ch1 - yoff) * ymu + yze 
tiempo = xze + np.arange(len(data_ch1)) * xin
fig, ax = plt.subplots()

ax.plot(tiempo,voltaje)

ch = 2
osci.write('DATA:SOUR CH{}'.format(ch))

data_ch2 = osci.query_binary_values('CURV?', datatype='B',container=np.array)
numpy.savetxt(data_ch2)
#plt.plot(data)

#le pido los parametros de la pantalla
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';') 
xze
xin
voltaje = (data_ch2 - yoff) * ymu + yze 
tiempo = xze + np.arange(len(data_ch2)) * xin

ax.plot(tiempo,voltaje, "--")

fig2, ax2 = plt.subplots()
ax2.set_title(f"desfase de: {angulo_grados}")
ax2.plot(data_ch1, data_ch2)


#%%

