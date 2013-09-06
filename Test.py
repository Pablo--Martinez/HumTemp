#!/usr/bin/python
"""
Modulo encargado de realizar el testeo sobre los sensores
Al correr el script retorna:
pin -> estado(OK/No_Presente)
"""
import subprocess
import sys
from time import sleep
from datetime import datetime

status = ["OK","No_Presente"]
pins = ["4","17","18","21","22","23","24","25"]
values = []
MAX_VECES = 3
veces = 0;

try: #Intento correr el script
        if (len(sys.argv) >= 2): #Encuentro el argumento del sensor
                print(datetime.now())
		for i in range(len(pins)):
			salida = subprocess.Popen(["sudo","./Adafruit_DHT2",sys.argv[1],pins[i]],stdout=subprocess.PIPE).communicate()[0]
                        #values.append(salida)
			while (salida == "" and veces <= MAX_VECES): #Intento tomar la medida
				sleep(1)
				salida = subprocess.Popen(["sudo","./Adafruit_DHT2",sys.argv[1],pins[i]],stdout=subprocess.PIPE).communicate()[0]   
				veces = veces +1
	
			values.append(salida)
			if (veces <= MAX_VECES):#Hay sensor
				print("GPIO_%s --> STATUS: \033[1;32m%s\033[1;m"%(pins[i],status[0]))
                        else: #No hay sensor conectado
                                print("GPIO_%s --> STATUS: \033[1;31m%s\033[1;m"%(pins[i],status[1]))
        		sleep(1)
			veces = 0
		print(datetime.now())
	else: #Falta argumento del sensor
                print("Tipo de sensor faltante, ejecute: sudo ./Test.py sensor")
except: #No se corrio con privilegios de root
        print("El test debe se corrido como root, ejecute: sudo ./Test.py sensor")
