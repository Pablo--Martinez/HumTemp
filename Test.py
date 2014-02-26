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
import pygtk
pygtk.require('2.0')
import gtk

status = ["OK","No_Presente"]
pines = ["4","17","18","27","22","23","24","25"]
#values = []
MAX_VECES = 3

def Test(labels):
	veces = 0;
	for i in range(len(pines)):
		salida = subprocess.Popen(["sudo","/home/pi/Desktop/HumTemp/Adafruit_DHT2","22",pines[i]],stdout=subprocess.PIPE).communicate()[0]
		while (salida == "" and veces <= MAX_VECES): #Intento tomar la medida
			sleep(1)
			salida = subprocess.Popen(["sudo","/home/pi/Desktop/HumTemp/Adafruit_DHT2","22",pines[i]],stdout=subprocess.PIPE).communicate()[0]   
			veces = veces +1

		#values.append(salida)
		if (veces <= MAX_VECES):#Hay sensor
			labels[i][1].set_markup('<span color="green">%s</span>'%(status[0]))
		else:
			labels[i][1].set_markup('<span color="red">%s</span>'%(status[1]))
		sleep(1)
		veces = 0
			
def GUI_Test():
	gui = gtk.Window(gtk.WINDOW_TOPLEVEL)
	gui.set_title("BioGuard-Test")
	gui.set_size_request(500,200)
	gui.set_position(gtk.WIN_POS_CENTER)
	gui.connect("delete-event", gtk.main_quit)
	
	vbox_main = gtk.VBox()
	hbox_valores1 = gtk.HBox()
	hbox_valores2 = gtk.HBox()
	vbox_gpios = []
	#Labels que contendran si un sensor esta presente o no
	labels_gpios = []
	for i in range(8):
		labels_gpios.append([gtk.Label(),gtk.Label()])
		vbox_gpios.append(gtk.VBox())
		labels_gpios[i][0].set_text("GPIO"+pines[i])
		vbox_gpios[i].pack_start(labels_gpios[i][0])
		vbox_gpios[i].pack_start(labels_gpios[i][1])
		if (i < 4):
			hbox_valores1.pack_start(vbox_gpios[i])
		else:
			hbox_valores2.pack_start(vbox_gpios[i])
			
	#Seteo todos los gpios como "-"
	for i in range(8):
		labels_gpios[i][1].set_text("-")
			
	boton_test = gtk.Button("Testear")
	boton_test.connect("clicked",lambda a:Test(labels_gpios))
	
	vbox_main.pack_start(hbox_valores1)
	vbox_main.pack_start(hbox_valores2)
	vbox_main.pack_start(boton_test)
	
	gui.add(vbox_main)
	gui.show_all()
	gtk.main()
	
	
if __name__ == "__main__": #Programa principal
	GUI_Test()

