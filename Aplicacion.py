#!/usr/bin/python

import PostgreSQL
import pygtk
pygtk.require('2.0')
import gtk
import os

ctr = "control"
separador = ";"

class GUI_app():
	def __init__(self):
		#Creo la ventana
		gui = gtk.Window(gtk.WINDOW_TOPLEVEL)
		gui.set_title("BioGuard")
		gui.set_size_request(600,150)
		gui.set_position(gtk.WIN_POS_CENTER)
		gui.connect("delete-event", gtk.main_quit)
	
		#Boxes que contienen los labels,botones y entradas
		hbox_main = gtk.HBox()
		vbox_main = gtk.VBox()
		vbox1 = gtk.VBox()
		vbox2 = gtk.VBox()
		hbox_botones = gtk.HBox()
		hbox_salir = gtk.HBox()
	
		label_estado = gtk.Label("Estado")
		boton_inicio = gtk.Button("INICIAR")
		boton_detener = gtk.Button("DETENER")
		boton_bajar = gtk.Button("BAJAR DATA")
		boton_salir = gtk.Button("SALIR")
		boton_salir.connect('clicked',lambda a: gtk.main_quit())
		label_nombre = gtk.Label("Nombre")
		label_ciclo = gtk.Label("Ciclo")
	
		if (self.Estado() == 1): #Actualmente midiendo
			valor_estado = gtk.Label()
			valor_estado.set_markup('<span color="green">CENSANDO</span>');
			entry_nombre = gtk.Label(self.Nombre())
			entry_ciclo = gtk.Label(self.Ciclo())
			#Establezco la conexion entre botones y funciones
			boton_detener.connect("clicked",lambda a:self.TerminarCensado())
		else: #No esta midiendo
			valor_estado = gtk.Label()
			valor_estado.set_markup('<span color="red">SIN CENSAR</span>');
			entry_nombre = gtk.Entry()
			entry_ciclo = gtk.Entry()
			entry_nombre.set_text("Ingrese el nombre para ser guardaro..")
			entry_ciclo.set_text("Tiempo en minutos entre medidas...")
			#Establezco la conexion entre botones y funciones
			boton_inicio.connect('clicked',lambda a:self.IniciarCensado(entry_nombre,entry_ciclo))
			boton_bajar.connect('clicked',lambda a:self.BajarDatos())
					
		#Empaqueto los botones,labels y entradas en los boxes
		vbox1.pack_start(label_estado)
		vbox1.pack_start(label_nombre)
		vbox1.pack_start(label_ciclo)
	
		vbox2.pack_start(valor_estado)
		vbox2.pack_start(entry_nombre)
		vbox2.pack_start(entry_ciclo)
	
		hbox_main.pack_start(vbox1)
		hbox_main.pack_start(vbox2)
	
		hbox_botones.pack_start(boton_inicio)
		hbox_botones.pack_start(boton_detener)
		hbox_botones.pack_start(boton_bajar)
	
		vbox_main.pack_start(hbox_main)
		vbox_main.pack_start(hbox_botones)
		vbox_main.pack_start(boton_salir)
	
		#Agrego el box principal y muestro en pantalla
		gui.add(vbox_main)
		gui.show_all()
		gtk.main()
		
		
	def IniciarCensado(self,widget1,widget2):
		"""
		Inicia el ciclo de sensado, los datos son almacenados cada "ciclo" minutos
		bajo el nombre de "nombre", en caso de que se este actualmente censado se 
		retorna -1.
		"""
		db = PostgreSQL.PostgreSQL()
		nombre = widget1.get_text()
		ciclo =  int(widget2.get_text())
		try: #Intento modificar control a la db
			row = db.SelectFromTable(ctr,["id",1])
			if (row[0][4] == 0):
				db.UpdateRegisterInTable(ctr,["id",1],["name",nombre])
				db.UpdateRegisterInTable(ctr,["id",1],["ciclo",ciclo-1])
				db.UpdateRegisterInTable(ctr,["id",1],["veces",0])
				db.UpdateRegisterInTable(ctr,["id",1],["status",1])
			else:
				return -1	
		except: #No existe control
			db.CreateTable(ctr,["name VARCHAR","ciclo INTEGER","veces INTEGER","status INTEGER"])
			db.InsertRegisterInTable(ctr,[nombre,ciclo-1,0,1])
		
		db.CloseDB()
		gtk.main_quit()
		os.system('./Aplicacion.py')
		return 0
		
	def TerminarCensado(self):
		"""
		Cancela el censado actual, en caso de no existir una etapa de censado
		actual retorna -1
		"""
		db = PostgreSQL.PostgreSQL()
		row = db.SelectFromTable(ctr,["id",1])
		if (row[0][4] == 1):
			db.UpdateRegisterInTable(ctr,["id",1],["status",0])
			gtk.main_quit()
			os.system('./Aplicacion.py')
			db.CloseDB()
			return 0
		else:
			return -1
		db.CloseDB()
		
	
	def BajarDatos(self): 
		"""
		Baja los datos de la db del ulitmo ciclo de censado, es decir donde el 
		nombre es el guardado el almacenado en control.
		En caso de que el ciclo de censado anterior no haya concluido retorna -1
		"""
		db = PostgreSQL.PostgreSQL()
		row = db.SelectFromTable(ctr,["id",1])
		if (row[0][4] == 0):
			rows = db.SelectFromTable("register",["name",row[0][1]])
			if (len(rows) > 0):
				f = open(row[0][1] + "_datos.txt","w")
				for elem in rows:
					line = elem[1] + separador + str(elem[2]) + separador + str(elem[3]) + separador + str(elem[4]) + separador + str(elem[5])
					f.write(line + "\n")
				f.close()
			db.CloseDB()
			return 0
		else:
			return -1
		
	def Estado(self):
		"""
		Retorna el estado actual del censado
		"""
		db = PostgreSQL.PostgreSQL()
		row = db.SelectFromTable(ctr,["id",1])
		if (row[0][4] == 1):
			db.CloseDB()
			return 1
		else:
			return 0
		
	def Nombre(self):
		"""
		Retorna el nombre del censado actual
		"""
		db = PostgreSQL.PostgreSQL()
		row = db.SelectFromTable(ctr,["id",1])
		return row[0][1]
	
	def Ciclo(self):
		"""
		Retorna el ciclo del censado actual
		"""
		db = PostgreSQL.PostgreSQL()
		row = db.SelectFromTable(ctr,["id",1])
		db.CloseDB()
		return row[0][2] + 1
	
if __name__ == "__main__":
	GUI_app()
