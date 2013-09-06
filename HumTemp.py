#!/usr/bin/env python
import subprocess
import datetime
import sys
import PostgreSQL
import os
from time import sleep

pins = ["4","17","18","21","22","23","24","25"]
MAX_INTENTOS = 3
intentos = 0

db = PostgreSQL.PostgreSQL("testdb","root")#Inicio motor de busqueda
status = db.SelectFromTable("control",["id","1"])#Busco el estado de la app
if status[0][4] == 1:#Esta corriendo
        if (status[0][3] == status[0][2]):#Realizo medicion
                db.UpdateRegisterInTable("control",["id",1],["veces",0]) #Actualizo
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') #Momento de medicion
                name = status[0][1]
                sensor = status[0][5]
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
                        
			sleep(1)
                        intentos = 0

	else:
        	veces = status[0][3]
                veces += 1
                db.UpdateRegisterInTable("control",["id",1],["veces",veces]) #Actualizo
                
db.CloseDB()#Cierro la base de datos
