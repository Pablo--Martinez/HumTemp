#!/usr/bin/python
"""
Script que realiza dos graficas, la primera contiene los valores de las
temperaturas y la segunda para la humedad. Se realizan varias graficas
sobre la misma grilla
"""
import pygtk
pygtk.require('2.0')
import gtk
import matplotlib.pyplot as plt
import psycopg2
import psycopg2.extras
import sys

def get_data(name):
	"""
	Obtiene los datos que seran graficados
	"""
	dates = [[],[],[],[],[],[],[],[]]
	temps = [[],[],[],[],[],[],[],[]]
	hums = [[],[],[],[],[],[],[],[]]
	db = psycopg2.connect(database="MapeoDB", user="pi", password="bioguardpassword")
	cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT \"ID\" FROM sesion WHERE \"NOMBRE\"=%s",(name,))
	sesion = cursor.fetchone()
	
	cursor.execute("SELECT * FROM registro WHERE \"ID_SESION\"=%s AND \"TIPO\"=\'H\' ORDER BY \"ID\"",(sesion["ID"],))
	rows = cursor.fetchall()
	db.close()
	
	for row in rows:
		if (row["SENSOR"] == 4):
			dates[0].append(row["FECHA"])
			temps[0].append(row["TEMP"])
			hums[0].append(row["HUM"])
		elif (row["SENSOR"] == 17):
			dates[1].append(row["FECHA"])
			temps[1].append(row["TEMP"])
			hums[1].append(row["HUM"])
		elif (row["SENSOR"] == 18):
			dates[2].append(row["FECHA"])
			temps[2].append(row["TEMP"])
			hums[2].append(row["HUM"])
		elif (row["SENSOR"] == 22):
			dates[3].append(row["FECHA"])
			temps[3].append(row["TEMP"])
			hums[3].append(row["HUM"])
		elif (row["SENSOR"] == 23):
			dates[4].append(row["FECHA"])
			temps[4].append(row["TEMP"])
			hums[4].append(row["HUM"])
		elif (row["SENSOR"] == 24):
			dates[5].append(row["FECHA"])
			temps[5].append(row["TEMP"])
			hums[5].append(row["HUM"])
		elif (row["SENSOR"] == 25):
			dates[6].append(row["FECHA"])
			temps[6].append(row["TEMP"])
			hums[6].append(row["HUM"])
		elif (row["SENSOR"] == 27):
			dates[7].append(row["FECHA"])
			temps[7].append(row["TEMP"])
			hums[7].append(row["HUM"])
			
	return dates,temps,hums

def plot(name):
	"""
	grafica los valores obtenidos con nombre "name"
	"""			
	dates,temps,hums = get_data(name)
	if (dates != [[],[],[],[],[],[],[],[]]): #Encuentra valores para graficar
		for i in range(8):
			if (temps[i] != []):
				plt.xlabel("Fecha")
				plt.grid(True)
				plt.subplot(211)
				plt.title("Temperatura-Humedad")
				plt.ylabel("Temperatura(c)")
				plt.plot_date(dates[i],temps[i],"o-",xdate = True)
				plt.grid(True)
				plt.subplot(212)
				plt.ylabel("Humedad(%)")
				plt.plot_date(dates[i],hums[i],"o-",xdate = True)
		plt.show()
		
	else: #No hay valores a graficar
		GUI_Mensaje("No existen valores para graficar")

def GUI_Mensaje(texto):
		error = gtk.MessageDialog(parent=None, flags=0, buttons=gtk.BUTTONS_OK)
		error.set_title("BioGuard-Graficas")
		error.set_size_request(400,150)
		error.connect("delete-event", gtk.main_quit)
		label = gtk.Label(texto)
		error.vbox.pack_start(label)
		error.show_all()
		error.run()
		error.destroy()	
			
def main():
	gui = gtk.Window(gtk.WINDOW_TOPLEVEL)
	gui.set_title("BioGuard-Graficas")
	gui.set_size_request(400,75)
	gui.set_position(gtk.WIN_POS_CENTER)
	gui.connect("delete-event", gtk.main_quit)
	
	vbox = gtk.VBox()
	entry_name = gtk.Entry()
	entry_name.set_text("Nombre de sesion a graficar...")
	boton_start = gtk.Button("Graficar")
	boton_start.connect("clicked",lambda a:plot(entry_name.get_text()))
	vbox.pack_start(entry_name)
	vbox.pack_start(boton_start)
	gui.add(vbox)
	gui.show_all()
	gtk.main()
	
if __name__ == "__main__": #Programa principal
	main()

