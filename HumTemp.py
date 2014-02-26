#!/usr/bin/env python
import subprocess
import datetime
import sys
import psycopg2
import psycopg2.extras
import os
from time import sleep

CONF_PATH = "/home/pi/digitemp.conf"
USB_ADAPTER = "digitemp_DS9097U"
USB_PATH = "/dev/ttyUSB0"
pins = ["4","17","18","27","22","23","24","25"]
MAX_INTENTOS = 3
intentos = 0

db = psycopg2.connect(database="MapeoDB", user="root", password="bioguardpassword")
cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("SELECT * FROM control WHERE \"ID\"=1") #Busco el estado de la app
status = cursor.fetchone()

if status["ESTADO"] == 1:#Esta corriendo

	cursor.execute("SELECT * FROM sesion WHERE \"ID\"=%s",(status["ID_SESION"],))
	sesion = cursor.fetchone()
	
	if (sesion["CICLO"] == sesion["CONT"]):#Realizo medicion
		cursor.execute("UPDATE sesion SET \"CONT\"=0 WHERE \"ID\"=%s",(status["ID_SESION"],))
		db.commit()
		date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') #Momento de medicion
		#Leo los sensores 1wire
		salida = subprocess.Popen(["sudo",USB_ADAPTER,"-a","-s",USB_PATH,"-c",CONF_PATH],stdout=subprocess.PIPE).communicate()[0].split("\n")[2:-1]
		for i in range(len(salida)):
			cursor.execute("INSERT INTO registro (\"ID_SESION\",\"TIPO\",\"SENSOR\",\"TEMP\",\"FECHA\") VALUES (%s,%s,%s,%s,%s)",(status["ID_SESION"],"T",i,float(salida[i]),date))
			db.commit()

		#Leo los sensores de humedad y temperatura
		for i in range(len(pins)):
			salida = subprocess.Popen(["sudo","/home/pi/Desktop/HumTemp/Adafruit_DHT2","22",pins[i]],stdout=subprocess.PIPE).communicate()[0]
            		while (salida == "" and intentos <= MAX_INTENTOS): #Intento tomar la medida
				sleep(1)
				salida = subprocess.Popen(["sudo","/home/pi/Desktop/HumTemp/Adafruit_DHT2","22",pins[i]],stdout=subprocess.PIPE).communicate()[0]
				intentos += +1
			
            		if (intentos <= MAX_INTENTOS):#Hay sensor
				temp = float(salida.split(" ")[0])
				hum = float(salida.split(" ")[1])
				cursor.execute("INSERT INTO registro (\"ID_SESION\",\"TIPO\",\"SENSOR\",\"TEMP\",\"HUM\",\"FECHA\") VALUES (%s,%s,%s,%s,%s,%s)",(sesion["ID"],"H",int(pins[i]),temp,hum,date))
				db.commit()
				cursor.execute("UPDATE sesion SET \"GPIO\"[%s]=%s WHERE \"ID\"=%s",(i+1,1,status["ID_SESION"]))
				db.commit()
            		else:
				cursor.execute("UPDATE sesion SET \"GPIO\"[%s]=%s WHERE \"ID\"=%s",(i+1,0,status["ID_SESION"]))
				db.commit()
			
			sleep(1)
	        	intentos = 0

	else:
        	
	        cursor.execute("UPDATE sesion SET \"CONT\"=%s WHERE \"ID\"=%s",(sesion["CONT"]+1,sesion["ID"]))
		db.commit()
                
db.close() #Detengo la conexion com la base
