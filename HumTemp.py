#!/usr/bin/env python
import subprocess
import datetime
import sys
import PostgreSQL
import os

pins = ["4","17","18","21","22","23","24","25"]
values = []

db = PostgreSQL.PostgreSQL("testdb","root")#Inicio motor de busqueda
status = db.SelectFromTable("control",["id","1"])#Busco el estado de la app
if status[0][4] == 1:#Esta corriendo
        if (status[0][3] == status[0][2]):#Realizo medicion
                db.UpdateRegisterInTable("control",["id",1],["veces",0]) #Actualizo
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') #Momento de medicion
                name = status[0][1]
                for i in range(len(pins)):
                        salida = subprocess.Popen(["sudo","/home/pi/Desktop/Python/Adafruit_DHT2","11",pins[i]],stdout=subprocess.PIPE).communicate()[0]
                        values.append(salida)
                        if (values[i] != ""): #Hay sensor en ese pin
                                temp = int(values[i].split(" ")[0])
                                hum = int(values[i].split(" ")[1])                                
                                db.InsertRegisterInTable("Register",[name,int(pins[i]),date,temp,hum])
        else:
                veces = status[0][3]
                veces += 1
                db.UpdateRegisterInTable("control",["id",1],["veces",veces]) #Actualizo
                
db.CloseDB()#Cierro la base de datos
