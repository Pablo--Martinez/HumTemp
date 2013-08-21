#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modulo encargado de gestionar una base de datos Postgesql
Version 1.1
"""

import psycopg2
import sys
import subprocess
from time import sleep

class PostgreSQL():
		
	def __init__(self,namedb="testdb",username="pablo"):
		"""
		Establece la conexion con la base de datos con nombre "namedb" y
		el usuario "username" en caso de no existir permite crearla
		"""
		self.conexion = None #Parto de la conexion nula
		
		try:
			conexion = psycopg2.connect(database=namedb, user=username) #Conecto con la base de datos 
			self.conexion = conexion #Relaciono la conexion con el objeto
			self.cursor = conexion.cursor() #Creo el cursor de la nueva conexion
			self.name = namedb
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				conexion.rollback()
				
			ans = raw_input("%sCreate db %s with owner %s? (y/n) " % (e,namedb,username))
			if ans == "y":
				subprocess.call(["createdb",namedb,"-O",username])
				conexion = psycopg2.connect(database=namedb, user=username) #Conecto con la base de datos 
				self.conexion = conexion #Relaciono la conexion con el objeto
				self.cursor = conexion.cursor() #Creo el cursor de la nueva conexion
				
			else:
				sys.exit(1)
    
			#print 'Error %s' % e    
			#sys.exit(1)
		
	def CreateTable(self,table_name,fields):
		"""
		Crea una nueva tabla dentro de la DB cuyo nombre es 'table_name'
		y 'fields' es una lista del tipo ['name_field type_field'] que
		indica los nombres y tipos de los campos que contiene la tabla.
		Ya posee un int autoincremental que es el id del elemento
		"""
		try:
			field = '' #Creo un nuevo string que representara los fields de la tabla
			for i in range(len(fields) - 1):
				field += fields[i] + ', '
			field += fields[len(fields) -1]
		
			command = 'CREATE TABLE ' + table_name + ' (id INT PRIMARY KEY, ' + field + ')' #Creo el comando a ser ejecutado
			self.cursor.execute(command)
			self.conexion.commit()
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e    
			#sys.exit(1)
			
	def InsertRegisterInTable(self,table_name,register):
		"""
		Inserta un nuevo registro dentro de la DB, especificamente dentro
		de la tabla cuyo nombre es 'table_name' y 'register' es una lista 
		que debe corresponder con la tabla en cuestion
		"""
		try:
			
			new_register = "" #Creo el nuevo registro que contendra los valores a insertar en la DB
			for i in range(len(register) - 1):
				if type(register[i]) == str: #En caso de ser str agrega "\'" para que sea un string
					new_register += "\'" + str(register[i]) + "\'" + ","
				else:
					new_register += str(register[i]) + ","
					
			if type(register[len(register) - 1]) == str:
				new_register += "\'" + str(register[len(register) - 1]) + "\'"
			else:
				new_register += str(register[len(register) - 1])
			
			
			command = "SELECT * FROM " + table_name #Cuento la cantidad de elementos para insertar el proximo
			self.cursor.execute(command)
						
			command = "INSERT INTO " + table_name + " VALUES(" + str(len(self.cursor.fetchall()) + 1) + "," + new_register + ")" #Comando a ser ejecutado en la insercion
			self.cursor.execute(command)
			self.conexion.commit()
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e   
			
	def UpdateRegisterInTable(self,table_name,consult, update_field):
		"""
		Actualiza un registro dentro de la DB, especificamente dentro
		de la tabla cuyo nombre es 'table_name' y 'update_register' es 
		una lista ['field_name', 'new'] que corresponde al campo de la 
		tabla a actualizar y el nuevo valor.
		La consulta debe ser una lista del tipo ['field_nama', 'value']
		que seleccionara el registro/s que cumple/n 'field_name=value' 
		"""
		try:
			if type(update_field[1]) == str:
				update_field[1] = "\'" + update_field[1] + "\'" 
			else:
				update_field[1] = str(update_field[1])
				
			if type(consult[1]) == str:
				consult[1] = "\'" + consult[1] + "\'"
			else:
				consult[1] = str(consult[1])
				
			command = "UPDATE " + table_name + " SET " + update_field[0] + '=' + update_field[1] + " WHERE " + consult[0] + "=" + consult[1]  #Comando para actualizar el registro seleccionado
			self.cursor.execute(command)        
			self.conexion.commit()
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e    
			#sys.exit(1)
    
		print "Number of rows updated: %d" % self.cursor.rowcount #Imprimo la cantidad de registros actualizados
		
	def SelectAllFromTable(self,table_name):
		"""
		Retorna todas las filas de la tabla cuyo nombre es 'table_name'
		"""
		try:
			command = "SELECT * FROM " + table_name #Comando para seleccionar
			self.cursor.execute(command)
			rows = self.cursor.fetchall()
			return rows #Retorno un array con todos los registros
		
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e    
			#sys.exit(1)
		
	def SelectFromTable(self,table_name,consult):
		"""
		Retorna las filas de la tabla con nombre 'table_name' que verifican
		la consulta, esta es una lista donde ['field', 'valor']
		"""
		try:
			if type(consult[1]) == str:
				consult[1] = "\'" + str(consult[1]) + "\'" 
			else:
				consult[1] = str(consult[1])
				
			command = "SELECT * FROM " + table_name + " WHERE " + consult[0] + "=" + consult[1]  #Comando se seleccion particular
			self.cursor.execute(command)
			rows = self.cursor.fetchall()
			return rows #Retorno el o los elementos seleccionados
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e    
			#sys.exit(1)
		
	def CopyToText(self,table_name,name):
		"""
		Copia los registros de la tabla 'table_name' en un archivo txt 
		de nombre 'name'
		"""
		try:
			f = open(name + '.txt','w')
			self.cursor.copy_to(f, table_name, sep="|")
			f.close()  
		
		except psycopg2.DatabaseError, e:
			print 'Error %s' % e    
			#sys.exit(1)

		except IOError, e:    
			print 'Error %s' % e   
			#sys.exit(1)
			
	def CopyFromText(self,table_name,name):
		"""
		Inserta los registros almacenados en el archivo 'name'.txt dentro
		de la tabla 'table_name', ellos	deben estar almacenados de la forma
		id|field|...|field
		"""
		try:
			f = open(name + '.txt','r')
			self.cursor.copy_from(f, table_name, sep="|")
			self.conexion.commit()
			f.close()  
		
		except psycopg2.DatabaseError, e:
			print 'Error %s' % e    
			#sys.exit(1)

		except IOError, e:    
			print 'Error %s' % e   
			#sys.exit(1)
		
	def DeleteRegisterInTable(self,table_name,consult):
		"""
		Borra el elemento/s dentro de 'table_name' que cumple/n la consulta
		La consulta debe ser una lista del tipo ["field_name", "value"] que corresponda
		con los fields de la tabla
		Si la consulta es vacia se borran todos los registros dentro de la tabla
		"""
		try:
			if type(consult[1]) == str:
				consult[1] = "\'" + consult[1] + "\'"
			else:
				consult[1] = str(consult[1])
			 
			command = "DELETE FROM " + table_name + " WHERE " + consult[0] + "= " + consult[1]
			self.cursor.execute(command)
			self.conexion.commit()
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e
			
	def ClearTable(self,table_name):
		"""
		Borra la tabla 'table_name' dentro de la DB
		"""
		try:
			command = "DROP TABLE IF EXISTS " + table_name #Comando de borrado
			self.cursor.execute(command)
			self.conexion.commit()
			
		except psycopg2.DatabaseError, e: #En caso de error se imprime en error y se revierten los cambios
			if self.conexion:
				self.conexion.rollback()
    
			print 'Error %s' % e
			
	def CloseDB(self):
		"""
		Termina la conexion con la base de datos acutal
		"""
		self.conexion.close()
				
	def DeleteDB(self):
		self.conexion.close()
		subprocess.call(["dropdb",self.name])
