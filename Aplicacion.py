#!/usr/bin/env python

import subprocess
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import PostgreSQL
import sys
from time import sleep
from Plot import plot

CONF_PATH = "/home/pi/digitemp.conf"
USB_ADAPTER = "digitemp_DS9097U"
USB_PATH = "/dev/ttyUSB0"
NO_USB_ADAPTER = "DigiTemp v3.5.0 Copyright 1996-2007 by Brian C. Lane\nGNU General Public License v2.0 - http://www.digitemp.com\n"
ctr = "control"
separador = ";"
pines = ["4","17","18","22","23","24","25","27"]
errores = ["Ya existe sesion activa","Debe terminar la sesion activa para bajar datos",
			"No existe sesion activa actualmente","No es posible bajar datos de sesion actual"]

def IniciarCensado(gui,nombre,ciclo,sensor,terminal):
	"""
	Inicia el ciclo de sensado, los datos son almacenados cada "ciclo" minutos
	bajo el nombre de "nombre", se asume que no esta censando actualmente
	"""
	if (Estado() == 0):
		db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
		db.UpdateRegisterInTable(ctr,["id",1],["name",nombre])
		db.UpdateRegisterInTable(ctr,["id",1],["ciclo",ciclo-1])
		db.UpdateRegisterInTable(ctr,["id",1],["veces",0])
		db.UpdateRegisterInTable(ctr,["id",1],["status",1])
		if (sensor == 1):
			db.UpdateRegisterInTable(ctr,["id",1],["sensor",11])
		else:
			db.UpdateRegisterInTable(ctr,["id",1],["sensor",22])
		#Configuro los sensores 1wire
		salida = subprocess.Popen(["sudo",USB_ADAPTER,"-i","-s",USB_PATH,"-c",CONF_PATH],stdout=subprocess.PIPE).communicate()[0]
		if (salida != NO_USB_ADAPTER):
			f = open("/home/pi/digitemp.conf","r")
			lines = f.readlines()
			lines = lines[7:]
			#gui.glade.get_object("label23").set_markup('<span color="green">%i</span>'%(len(lines)))
			f.close()
		else:
			gui.glade.get_object("label23").set_markup('<span color="red">-</span>')
		#Busco que sensor de temp/hum esta conectado
		for i in range(len(pines)):
			intentos = 0
			MAX_INTENTOS = 3
			salida = subprocess.Popen(["sudo","/home/pi/Desktop/Python/Adafruit_DHT2",str(Sensor()),pines[i]],stdout=subprocess.PIPE).communicate()[0]
                	while (salida == "" and intentos <= MAX_INTENTOS): #Intento tomar la medida
                        	sleep(1)
                               	salida = subprocess.Popen(["sudo","/home/pi/Desktop/Python/Adafruit_DHT2",str(Sensor()),pines[i]],stdout=subprocess.PIPE).communicate()[0]
                               	intentos += +1
               		if (intentos <= MAX_INTENTOS):#Hay sensor
				db.UpdateRegisterInTable(ctr,["id",1],["gpio"+pines[i],1])
			else:
				db.UpdateRegisterInTable(ctr,["id",1],["gpio"+pines[i],0])
                       	sleep(1)
                       	intentos = 0
			
		db.CloseDB()
		if (not terminal):
			sensores = SensoresActivos()
			gui.glade.get_object("label23").set_markup('<span color="green">%i</span>'%(sensores[1]))
			if (sensores[0][0] == 1):
				gui.glade.get_object("label7").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label7").set_markup('<span color="red">-</span>')
			if (sensores[0][1] == 1):
				gui.glade.get_object("label11").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label11").set_markup('<span color="red">-</span>')
			if (sensores[0][2] == 1):
				gui.glade.get_object("label15").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label15").set_markup('<span color="red">-</span>')
			if (sensores[0][3] == 1):
				gui.glade.get_object("label19").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label19").set_markup('<span color="red">-</span>')
			if (sensores[0][4] == 1):
				gui.glade.get_object("label9").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label9").set_markup('<span color="red">-</span>')
			if (sensores[0][5] == 1):
				gui.glade.get_object("label13").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label13").set_markup('<span color="red">-</span>')
			if (sensores[0][6] == 1):
				gui.glade.get_object("label17").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label17").set_markup('<span color="red">-</span>')
			if (sensores[0][7] == 1):
				gui.glade.get_object("label21").set_markup('<span color="green">OK</span>')
			else:
				gui.glade.get_object("label21").set_markup('<span color="red">-</span>')
			GUI_Mensaje("%s: Sesion iniciada"%(Nombre()))
		else:
			print("%s: Sesion iniciada"%(Nombre()))
	else:
		if (not terminal):
			GUI_Mensaje(errores[0])
		else:
			print(errores[0])
				
def TerminarCensado(gui,terminal):
	"""
	Cancela el censado actual, asume que actualmente se esta censando
	"""
	db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
	if (Estado() == 1):
		db.UpdateRegisterInTable(ctr,["id",1],["status",0])
		if (not terminal):
			gui.glade.get_object("label23").set_markup('<span color="red">-</span>')
			BajarDatos(Nombre(),0)
			GUI_Mensaje("%s: Sesion terminada"%(Nombre()))
					
		else:
			BajarDatos(Nombre(),1)
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
		db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
		row = db.SelectFromTable(ctr,["id",1])
		rows = db.SelectFromTable("register",["name",nombre])
		if (len(rows) > 0):
			f = open("/home/pi/Desktop/Python/" + nombre + "_humtemp.txt","w")
			for elem in rows:
				line = elem[1] + separador + str(elem[2]) + separador + str(elem[3]) + separador + str(elem[4]) + separador + str(elem[5])
				f.write(line + "\n")
			f.close()
		
			rows = db.SelectFromTable("register_temp",["name",nombre])
			if (len(row)):
				f = open("/home/pi/Desktop/Python/" + nombre + "_temp.txt","w")
				for elem in rows:
					line = elem[1] + separador + str(elem[2]) + separador + str(elem[3]) + separador + str(elem[4])
                                	f.write(line + "\n")
                        	f.close()
			
				f = open("/home/pi/digitemp.conf","r")
				lineas = f.readlines()
				lineas = lineas[7:]
				sensor_roms = open("/home/pi/Desktop/Python/" + nombre + "_ROMS.txt","w")
				for i in range(len(lineas)):
					rom = lineas[i][lineas[i].find("0x"):-2]
					sensor_roms.write("SENSOR:%i -> ROM:%s\n"%(i,rom))
				f.close()
				sensor_roms.close()
					
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
	db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
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
	db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	return row[0][1]

def Ciclo():
	"""
	Retorna el ciclo del censado actual
	"""
	db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	return row[0][2] + 1
	
def Sensor():
	"""
	Retorna el tipo de sensor
	"""
	db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	return row[0][5]

def SensoresActivos():
	"""
	Retorna una lista con los sensores, activos y desactivos
	"""
	db = PostgreSQL.PostgreSQL(namedb="BioGuardDB",username="BioGuard",host='localhost',passw="bioguardpassword")
	row = db.SelectFromTable(ctr,["id",1])
	db.CloseDB()
	sensores = []
	cant = 0
	salida = subprocess.Popen(["sudo",USB_ADAPTER,"-i","-s",USB_PATH,"-c",CONF_PATH],stdout=subprocess.PIPE).communicate()[0]
        if (salida != NO_USB_ADAPTER):
        	f = open("/home/pi/digitemp.conf","r")
        	lines = f.readlines()
        	lines = lines[7:]
		cant = len(lines)
        	f.close()
        for i in range(6,len(row[0])):
		sensores.append(row[0][i])
	return [sensores,cant]	

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
	
class App():
	
	def __init__(self):
		self.gladefile = "/home/pi/Desktop/Python/app.glade" 
		self.glade = gtk.Builder()
		self.glade.add_from_file(self.gladefile)
		self.glade.connect_signals(self)
		self.glade.get_object("MainWindow")
		self.glade.get_object("window1").set_title("BioGuard")
		self.glade.get_object("window1").connect("delete-event", gtk.main_quit)

		self.functions = {"start":self.startButton,
	                     "stop":self.stopButton,
        	             "download":self.downloadData,
                	     "plot":self.plotData,
                    	     "exit":self.exit}
                    	     
		if (Estado() == 1):
			self.glade.get_object("label5").set_markup('<span color="green">CENSANDO</span>')
			self.glade.get_object("button2").set_sensitive(True)
			self.glade.get_object("button1").set_sensitive(False)
			self.glade.get_object("entry3").set_sensitive(False)
			self.glade.get_object("entry3").set_text(Nombre())
			self.glade.get_object("entry4").set_sensitive(False)
			self.glade.get_object("entry4").set_text(str(Ciclo()))
			self.glade.get_object("combobox1").set_sensitive(False)
			listaelementos=gtk.ListStore(str)
			if (Sensor() == 11):
                        	listaelementos.append(["DHT22"])
                        	listaelementos.append(["DHT11"])
			else:
				listaelementos.append(["DHT11"])
                                listaelementos.append(["DHT22"])
                        self.glade.get_object("combobox1").set_model(listaelementos)
                        render = gtk.CellRendererText()
                        self.glade.get_object("combobox1").pack_start(render, True)
                        self.glade.get_object("combobox1").add_attribute(render, 'text', 0)
			sensores = SensoresActivos()
			if (sensores[1] != 0):
				self.glade.get_object("label23").set_markup('<span color="green">%i</span>'%(sensores[1]))
			else:
				self.glade.get_object("label23").set_markup('<span color="red">-</span>')
			if (sensores[0][0] == 1):
				self.glade.get_object("label7").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label7").set_markup('<span color="red">-</span>')
			if (sensores[0][1] == 1):
				self.glade.get_object("label11").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label11").set_markup('<span color="red">-</span>')
			if (sensores[0][2] == 1):
				self.glade.get_object("label15").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label15").set_markup('<span color="red">-</span>')
			if (sensores[0][3] == 1):
				self.glade.get_object("label19").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label19").set_markup('<span color="red">-</span>')
			if (sensores[0][4] == 1):
				self.glade.get_object("label9").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label9").set_markup('<span color="red">-</span>')
			if (sensores[0][5] == 1):
				self.glade.get_object("label13").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label13").set_markup('<span color="red">-</span>')
			if (sensores[0][6] == 1):
				self.glade.get_object("label17").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label17").set_markup('<span color="red">-</span>')
			if (sensores[0][7] == 1):
				self.glade.get_object("label21").set_markup('<span color="green">OK</span>')
			else:
				self.glade.get_object("label21").set_markup('<span color="red">-</span>')
			
						
		else:
			self.glade.get_object("button2").set_sensitive(False)
			self.glade.get_object("label5").set_markup('<span color="red">SIN CENSAR</span>')
			self.glade.get_object("button1").set_sensitive(True)
			self.glade.get_object("entry3").set_sensitive(True)
			self.glade.get_object("entry4").set_sensitive(True)
			self.glade.get_object("combobox1").set_sensitive(True)
			self.glade.get_object("label7").set_markup('<span color="red">-</span>')
			self.glade.get_object("label11").set_markup('<span color="red">-</span>')
			self.glade.get_object("label15").set_markup('<span color="red">-</span>')
			self.glade.get_object("label19").set_markup('<span color="red">-</span>')
			self.glade.get_object("label9").set_markup('<span color="red">-</span>')
			self.glade.get_object("label13").set_markup('<span color="red">-</span>')
			self.glade.get_object("label17").set_markup('<span color="red">-</span>')
			self.glade.get_object("label21").set_markup('<span color="red">-</span>')
			listaelementos=gtk.ListStore(str)
                        listaelementos.append(["DHT22"])
                        listaelementos.append(["DHT11"])
                        self.glade.get_object("combobox1").set_model(listaelementos)
                        render = gtk.CellRendererText()
                        self.glade.get_object("combobox1").pack_start(render, True)
                        self.glade.get_object("combobox1").add_attribute(render, 'text', 0)
			
	
	def startButton(self,widget):
		"""
		Starts a new session
		"""
		#Desactivo la sensibilidad de algunos elementos
		widget.set_sensitive(False)
		self.glade.get_object("label5").set_markup('<span color="green">CENSANDO</span>')
		self.glade.get_object("button2").set_sensitive(True)
		self.glade.get_object("entry3").set_sensitive(False)
		self.glade.get_object("entry4").set_sensitive(False)
		self.glade.get_object("combobox1").set_sensitive(False)

		#Obtengo los datos para iniciar la sesion}
		nombre= str(self.glade.get_object("entry3").get_text())
		ciclo = int(self.glade.get_object("entry4").get_text())
		sensor = int(self.glade.get_object("combobox1").get_active())
		IniciarCensado(self,nombre,ciclo,sensor,0)
		

	def stopButton(self,widget):
		"""
		Stops the current session
		"""
		widget.set_sensitive(False)
		self.glade.get_object("label5").set_markup('<span color="red">SIN CENSAR</span>')
		self.glade.get_object("button1").set_sensitive(True)
		self.glade.get_object("entry3").set_sensitive(True)
		self.glade.get_object("entry4").set_sensitive(True)
		self.glade.get_object("combobox1").set_sensitive(True)
		self.glade.get_object("label7").set_markup('<span color="red">-</span>')
		self.glade.get_object("label11").set_markup('<span color="red">-</span>')
		self.glade.get_object("label15").set_markup('<span color="red">-</span>')
		self.glade.get_object("label19").set_markup('<span color="red">-</span>')
		self.glade.get_object("label9").set_markup('<span color="red">-</span>')
		self.glade.get_object("label13").set_markup('<span color="red">-</span>')
		self.glade.get_object("label17").set_markup('<span color="red">-</span>')
		self.glade.get_object("label21").set_markup('<span color="red">-</span>')
		TerminarCensado(self,0)

	def downloadData(self,widget):
		"""
		Donwload specific data from a session
		"""
		nombre = self.glade.get_object("entry1").get_text()
		BajarDatos(nombre,0)

	def plotData(self,widget):
		"""
		Plot specific data, if widget.get_text() == "" plot the current session
		"""
		nombre = self.glade.get_object("entry2").get_text()
		plot(nombre)

	def exit(self,widget):
		gtk.main_quit()

class Terminal():
	"""
	Permite ejecutar la aplicacion en version terminal
	"""
	comandos = ["ayuda","iniciar","terminar","bajar","estado","salir"]
	
	def __init__(self):
		comando = raw_input("BIOGUARD $ ").split(" ")
		while (comando[0] != "salir"):
			if (comando[0] == "iniciar"): #Inicio de sesion
				if (len(comando) >= 4): #Cantidad de comandos correctos
					if (Estado() == 0): #No se esta censando acutalmente
						if (type(comando[2] == "int")): #El ciclo es un numero
							IniciarCensado("",comando[1],int(comando[2]),comando[3],1)
							print("Sesion iniciada...")
						else:
							print("ciclo incorrecto...")
					else:
						print(errores[0])
				else:
					print("Argumentos faltantes...")
		
			elif(comando[0] == "terminar"): #Terminar sesion activa
				TerminarCensado("",1)
						
			elif(comando[0] == "estado"): #Imprimo los valores actuales de la sesion si esta activa
				if (Estado() == 1):
					print("	-Estado --> Corriendo")
					print("	-Nombre --> %s" %(Nombre()))
					print("	-Ciclo --> %i" %(Ciclo()))
					if (Sensor() == 0):
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
				print("	-bajar nombre --> Baja los datos de la sesion actual")
				print("	-estado --> Muestra el estado del sistema ")
			
			else:
				print("Comando desconocido...")
	
			comando = raw_input("BIOGUARD $ ").split(" ")
		sys.exit()

if __name__ == "__main__":
	if (len(sys.argv) >= 2):
		if (sys.argv[1] == "-t"):
			Terminal()
	else:
		gui = App()
		gtk.main()

