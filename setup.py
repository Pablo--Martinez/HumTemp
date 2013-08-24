"""
Modulo encargado de preparar el sistema para poder realizar las mediciones
"""
import subprocess
import PostgreSQL.py

print("Instalando PostgreSQL...")
subprocess.call(["sudo","apt-get","install","postgresql"])
print("Instalación completada!")

print("Iniciando motor de base de datos...")
subprocess.call(["sudo","service","postgresql","start"])
print("Motor iniciado!")

print("Creando nuevo usuario...")
subprocess.call(["sudo","-u","postgresql","createuser","pi"])#Se deben insertar las opciones adecuadas
subporcess.call(["sudo","-u","postgresql","createuser","root"])
print("Nuevo usuario creado!")

print("Creando nueva base de datos...")
subproces.call(["sudo","-u","postgresql","createdb","testdb","-O","pi"])
print("Base de datos creada!")

print("Conectando con base de datos...")
db = PostgreSQL.PostgreSQL("testdb","pi")
print("Conexion realizada!")

print("Creando nuevas tablas...")
db.CreateTable("register",["name VARCHAR","gpio INTEGER","date TIMESTAMP","temp INTEGER","hum INTEGER"])
db.CreateTable("control",["name VARCHAR","ciclo INTEGER","veces INTEGER","status INTEGER"])
print("Tablas creadas!")

print("Otorgando permisos...")
db.GivePermissions("register","root")
db.GivePermissions("control","root")
print("Permisos otorgados!")

print("Cerrando conexion con base de datos...")
db.CloseDB()
print("Conexion terminada!")

print("Proceso finalizado!")






