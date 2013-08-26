#!/usr/bin/python

import PostgreSQL
import pygtk
pygtk.require('2.0')
import gtk
import os
import subprocess
import sys

ctr = "control"
separador = ";"
pines = ["4","17","18","22","23","24","25","27"]
errores = ["Ya existe sesion activa","Debe terminar la sesion activa para bajar datos",
			"No existe sesion activa actualmente","No es posible bajar datos de sesion actual"]

def IniciarCensado(nombre,ciclo,sensor,terminal):
		"""
		Inicia el ciclo de sensado, los datos son almacenados cada "ciclo" minutos
		bajo el nombre de "nombre", se asume que no esta censando actualmente
		"""
		db = PostgreSQL.PostgreSQL()
		if (Estado() == 0):
			db = PostgreSQL.PostgreSQL()
			try: #Intento modificar control a la db
				db.UpdateRegisterInTable(ctr,["id",1],["name",nombre])
				db.UpdateRegisterInTable(ctr,["id",1],["ciclo",ciclo-1])
				db.UpdateRegisterInTable(ctr,["id",1],["veces",0])
				db.UpdateRegisterInTable(ctr,["id",1],["status",1])
				if (sensor == "DHT11"):
					db.UpdateRegisterInTable(ctr,["id",1],["sensor",11])
				else:
					db.UpdateRegisterInTable(ctr,["id",1],["sensor",22])
			except: #No existe control
				db.CreateTable(ctr,["name VARCHAR","ciclo INTEGER","veces INTEGER","status INTEGER","sensor INTEGER"])
				db.InsertRegisterInTable(ctr,[nombre,ciclo-1,0,1,11])
				db.UpdateRegisterInTable(ctr,["id",1],["name",nombre])
				db.UpdateRegisterInTable(ctr,["id",1],["ciclo",ciclo-1])
				db.UpdateRegisterInTable(ctr,["id",1],["veces",0])
				db.UpdateRegisterInTable(ctr,["id",1],["status",1])
				if (sensor == "DHT11"):
					db.UpdateRegisterInTable(ctr,["id",1],["sensor",11])
				else:
					db.UpdateRegisterInTable(ctr,["id",1],["sensor",22])
			db.CloseDB()
			
			if (not terminal):
				GUI_Mensaje("%s: Sesion iniciada"%(Nombre()))
				gtk.main_quit()
				os.system(os.getcwd() + "/Aplicacion.py" )
			else:
				print("%s: Sesion iniciada"%(Nombre()))
		else:
			if (not terminal):
				GUI_Mensaje(errores[0])
			else:
				print(errores[0])
				
def TerminarCensado(terminal):
	"""
	Cancela el censado actual, asume que actualmente se esta censando
	"""
	db = PostgreSQL.PostgreSQL()
	if (Estado() == 1):
		db.UpdateRegisterInTable(ctr,["id",1],["status",0])
		if (not terminal):
			GUI_Mensaje("%s: Sesion terminada"%(Nombre()))
			gtk.main_quit()
			os.system(os.getcwd() + "/Aplicacion.py" )
		else:
			print("%s: Sesion terminada"%(Nombre()))
	else:
		if (not terminal):
			GUI_Mensaje(errores[2])
		else:
			print(errores[2])
	db.CloseDB()
			
def BajarDatos(nombre,terminal): 
	"""
	Baja los datos de la sesion con nombre pasado como parametro
	"""
	if (Nombre() != nombre or Estado() == 0):
		db = PostgreSQL.PostgreSQL()
		row = db.SelectFromTable(ctr,["id",1])
		rows = db.SelectFromTable("register",["name",nombre])
		if (len(rows) > 0):
			f = open(nombre + "_datos.txt","w")
			for elem in rows:
				line = elem[1] + separador + str(elem[2]) + separador + str(elem[3]) + separador + str(elem[4]) + separador + str(elem[5])
				f.write(line + "\n")
			f.close()
			if (not terminal):
				GUI_Mensaje("%s: Datos guardados correctamente" %(nombre))
			else:
				print("%s: Datos guardados correctamente" %(nombre))		
		else:
			if (not terminal):
				GUI_Mensaje("%s: No existen registros" %(nombre))
			else:
				print("%s: No existen registros" %(nombre))	
		db.CloseDB()
	else:
		if (not terminal):
			GUI_Mensaje(errores[3])
		else:
			print(errores[3])	
	
def Estado():
	"""
	Retorna el estado actual del censado
	"""
	db = PostgreSQL.PostgreSQL()
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	if (row[0][4] == 1):
		return 1
	else:
		return 0
	
def Nombre():
	"""
	Retorna el nombre del censado actual
	"""
	db = PostgreSQL.PostgreSQL()
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	return row[0][1]

def Ciclo():
	"""
	Retorna el ciclo del censado actual
	"""
	db = PostgreSQL.PostgreSQL()
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	return row[0][2] + 1
	
def Sensor():
	"""
	Retorna el tipo de sensor
	"""
	db = PostgreSQL.PostgreSQL()
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	return row[0][5]

class GUI_Mensaje():
	def __init__(self,texto):
		error = gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK)
		error.set_title("BioGuard")
		error.set_size_request(400,150)
		error.connect("delete-event", gtk.main_quit)
		label = gtk.Label(texto)
		error.vbox.pack_start(label)
		error.show_all()
		error.run()
		error.destroy()
				
class GUI_app():
	def __init__(self):
		#Creo la ventana
		gui = gtk.Window(gtk.WINDOW_TOPLEVEL)
		gui.set_title("BioGuard")
		gui.set_size_request(600,270)
		gui.set_position(gtk.WIN_POS_CENTER)
		gui.connect("delete-event", gtk.main_quit)
	
		#Boxes que contienen los labels,botones y entradas
		hbox_main = gtk.HBox()
		vbox_main = gtk.VBox()
		vbox1 = gtk.VBox()
		vbox2 = gtk.VBox()
		hbox_valores1 = gtk.HBox()
		hbox_valores2 = gtk.HBox()
		vbox_gpios = []
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
		
		hbox_botones = gtk.HBox()
		hbox_salir = gtk.HBox()
	
		label_estado = gtk.Label("Estado")
		boton_inicio = gtk.Button("INICIAR")
		boton_detener = gtk.Button("DETENER")
		boton_bajar = gtk.Button("BAJAR DATA")
		boton_salir = gtk.Button("SALIR")
		boton_salir.connect('clicked',lambda a: gtk.main_quit())
		label_nombre = gtk.Label("Nombre")
		label_ciclo = gtk.Label("Ciclo(min)")
		label_menu = gtk.Label("Sensor")
		label_bajar = gtk.Label("Datos a bajar:")
		entry_bajar = gtk.Entry()
		entry_bajar.set_text("Nombre de sesion a bajar...")
		
				
		if (Estado() == 1): #Actualmente midiendo
			valor_estado = gtk.Label()
			valor_estado.set_markup('<span color="green">CENSANDO</span>');
			entry_nombre = gtk.Label(Nombre())
			entry_ciclo = gtk.Label(Ciclo())
			menu = gtk.Label("DHT" + str(Sensor()))
			boton_inicio.connect("clicked",lambda a:IniciarCensado("","","",0))
			boton_detener.connect("clicked",lambda a:TerminarCensado(0))
			boton_bajar.connect("clicked",lambda a:BajarDatos(entry_bajar.get_text(),0))
			#for i in range(8):
			#	labels_gpios[i][1] = subprocess.Popen(["sudo","/home/pi/Desktop/Python/Adafruit_DHT2","11",pines[i]],stdout=subprocess.PIPE).communicate()[0]

	
		else: #No esta midiendo
			valor_estado = gtk.Label()
			valor_estado.set_markup('<span color="red">SIN CENSAR</span>');
			entry_nombre = gtk.Entry()
			entry_ciclo = gtk.Entry()
			entry_nombre.set_text("Ingrese el nombre para ser guardaro..")
			entry_ciclo.set_text("Tiempo en minutos entre medidas...")
			#Menu desplegable para selecionar el sensor
			menu = gtk.Combo()
			opciones = ["DHT11","DHT22"]
			menu.set_popdown_strings(opciones)
			#Establezco la conexion entre botones y funciones
			boton_inicio.connect('clicked',lambda a:IniciarCensado(entry_nombre.get_text(),int(entry_ciclo.get_text()),menu.entry.get_text(),0))
			boton_detener.connect("clicked",lambda a:TerminarCensado(0))
			boton_bajar.connect('clicked',lambda a:BajarDatos(entry_bajar.get_text(),0))
			for i in range(8):
				labels_gpios[i][1].set_text("-")
					
		#Empaqueto los botones,labels y entradas en los boxes
		vbox1.pack_start(label_estado)
		vbox1.pack_start(label_nombre)
		vbox1.pack_start(label_ciclo)
		vbox1.pack_start(label_menu)
	
		vbox2.pack_start(valor_estado)
		vbox2.pack_start(entry_nombre)
		vbox2.pack_start(entry_ciclo)
		vbox2.pack_start(menu)
		
		hbox_bajar = gtk.HBox()
		hbox_bajar.pack_start(label_bajar)
		hbox_bajar.pack_start(entry_bajar)
			
		hbox_main.pack_start(vbox1)
		hbox_main.pack_start(vbox2)
	
		hbox_botones.pack_start(boton_inicio)
		hbox_botones.pack_start(boton_detener)
		#hbox_botones.pack_start(boton_bajar)
	
		vbox_main.pack_start(hbox_main)
		vbox_main.pack_start(hbox_valores1)
		vbox_main.pack_start(hbox_valores2)
		vbox_main.pack_start(hbox_botones)
		vbox_main.pack_start(hbox_bajar)
		vbox_main.pack_start(boton_bajar)
		vbox_main.pack_start(boton_salir)
	
		#Agrego el box principal y muestro en pantalla
		gui.add(vbox_main)
		gui.show_all()
		gtk.main()
		
class Terminal():
	"""
	Permite ejecutar la aplicacion en version terminal
	"""
	comandos = ["ayuda","iniciar","terminar","bajar","status","salir"]
	
	def __init__(self):
		comando = raw_input("BIOGUARD $ ").split(" ")
		while (comando[0] != "salir"):
			if (comando[0] == "iniciar"): #Inicio de sesion
				if (len(comando) >= 4): #Cantidad de comandos correctos
					if (Estado() == 0): #No se esta censando acutalmente
						if (type(comando[2] == "int")): #El ciclo es un numero
							IniciarCensado(comando[1],int(comando[2]),comando[3],1)
							print("Sesion iniciada...")
						else:
							print("ciclo incorrecto...")
					else:
						print(errores[0])
				else:
					print("Argumentos faltantes...")
		
			elif(comando[0] == "terminar"): #Terminar sesion activa
				TerminarCensado(1)
						
			elif(comando[0] == "status"): #Imprimo los valores actuales de la sesion si esta activa
				if (Estado() == 1):
					print("	-Estado --> Corriendo")
					print("	-Nombre --> %s" %(Nombre()))
					print("	-Ciclo --> %i" %(Ciclo()))
					if (Sensor() == 11):
						print("	-Sensor --> DHT11")
					else:
						print("	-Sensor --> DHT22")
				else:
					print("	-Estado --> Detenido")
					
			elif(comando[0] == "bajar"): #Bajo los datos de la sesion actual
				if (len(comando) >= 2):
					BajarDatos(comando[1],1)
				else:
					print("Argumentos faltantes...")
					
			elif(comando[0] == "ayuda"): #Imprimo ayuda en pantalla
				print("	-ayuda --> Menu de ayuda")
				print("	-iniciar nombre ciclo sensor(DHT11/DHT22) --> Crea una nueva sesion")
				print("	-terminar --> Termina la sesion actual")
				print("	-bajar --> Baja los datos de la sesion actual")
				print("	-status --> Muestra el estado del sistema ")
			
			else:
				print("Comando desconocido...")
	
			comando = raw_input("BIOGUARD $ ").split(" ")
		sys.exit()

if __name__ == "__main__":
	if (len(sys.argv) >= 2):
		if (sys.argv[1] == "-t"):
			Terminal()
	else:
		GUI_app()
