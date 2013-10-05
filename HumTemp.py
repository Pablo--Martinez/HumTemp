#!/usr/bin/env python
import subprocess
import datetime
import sys
import PostgreSQL
import os
from time import sleep

CONF_PATH = "/home/pi/digitemp.conf"
USB_ADAPTER = "digitemp_DS9097U"
USB_PATH = "/dev/ttyUSB0"
pins = ["4","17","18","27","22","23","24","25"]
MAX_INTENTOS = 3
intentos = 0

db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")#Inicio motor de busqueda
status = db.SelectFromTable("control",["id","1"])#Busco el estado de la app
if status[0][4] == 1:#Esta corriendo
        if (status[0][3] == status[0][2]):#Realizo medicion
                db.UpdateRegisterInTable("control",["id",1],["veces",0]) #Actualizo
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') #Momento de medicion
                name = status[0][1]
                sensor = status[0][5]
		#Leo los sensores 1wire
		salida = subprocess.Popen(["sudo",USB_ADAPTER,"-a","-s",USB_PATH,"-c",CONF_PATH],stdout=subprocess.PIPE).communicate()[0].split("\n")[2:-1]
		for i in range(len(salida)):
			db.InsertRegisterInTable("register_temp",[name,i,date,float(salida[i])])
		#Leo los sensores de humedad y temperatura
                for i in range(len(pins)):
			salida = subprocess.Popen(["sudo","/home/pi/Desktop/Python/Adafruit_DHT2",str(sensor),pins[i]],stdout=subprocess.PIPE).communicate()[0]
                        while (salida == "" and intentos <= MAX_INTENTOS): #Intento tomar la medida
                                sleep(1)
                                salida = subprocess.Popen(["sudo","/home/pi/Desktop/Python/Adafruit_DHT2",str(sensor),pins[i]],stdout=subprocess.PIPE).communicate()[0]
                                intentos += +1
			
                        if (intentos <= MAX_INTENTOS):#Hay sensor
 				temp = float(salida.split(" ")[0])
                                hum = float(salida.split(" ")[1])
                                db.InsertRegisterInTable("Register",[name,int(pins[i]),date,temp,hum])
				db.UpdateRegisterInTable("control",["id",1],["gpio"+pins[i],1])
                        else:
				db.UpdateRegisterInTable("control",["id",1],["gpio"+pins[i],0])
			sleep(1)
                        intentos = 0

	else:
        	veces = status[0][3]
                veces += 1
                db.UpdateRegisterInTable("control",["id",1],["veces",veces]) #Actualizo
                
db.CloseDB()#Cierro la base de datos
