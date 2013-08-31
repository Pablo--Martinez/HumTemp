#!/usr/bin/python
"""
Modulo encargado de realizar el testeo sobre los sensores
Al correr el script retorna:
pin -> estado(OK/No_Presente)
"""
import subprocess
import sys

status = ["OK","No_Presente"]
pins = ["4","17","18","21","22","23","24","25"]
values = []

try: #Intento correr el script
        if (len(sys.argv) >= 2): #Encuentro el argumento del sensor
                for i in range(len(pins)):
                        salida = subprocess.Popen(["sudo","./Adafruit_DHT2",sys.argv[1],pins[i]],stdout=subprocess.PIPE).communicate()[0]
                        values.append(salida)
                        if (values[i] != ""): #Hay sensor en ese pin
                                print("GPIO_%s --> STATUS: %s"%(pins[i],status[0]))
                        else: #No hay sensor conectado
                                print("GPIO_%s --> STATUS: %s"%(pins[i],status[1]))
        else: #Falta argumento del sensor
                print("Tipo de sensor faltante, ejecute: sudo ./Test.py sensor")
except: #No se corrio con privilegios de root
        print("El test debe se corrido como root, ejecute: sudo ./Test.py sensor")
