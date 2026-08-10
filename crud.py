import mysql.connector
from colorama import Fore

def insertar(nombre, rfc, telefono, correo, conexion):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO proveedores (nombre, rfc, telefono, correo) VALUES (%s, %s, %s, %s)"
        valores = (nombre, rfc, telefono, correo)
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error en Base de Datos: {err}")
        return False

def consultar(conexion):
    try:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, rfc, telefono, correo FROM proveedores"
        cursor.execute(sql)
        registros = cursor.fetchall()
        cursor.close()
        return registros
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al consultar proveedores: {err}")
        return []

def buscar(nombre, conexion):
    try:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, rfc, telefono, correo FROM proveedores WHERE nombre LIKE %s"
        cursor.execute(sql, (f"%{nombre}%",))
        registros = cursor.fetchall()
        cursor.close()
        return registros
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al buscar proveedor: {err}")
        return []

def borrar(nombre, conexion):
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM proveedores WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        conexion.commit()
        afectados = cursor.rowcount
        cursor.close()
        return afectados > 0
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al borrar proveedor: {err}")
        return False

def modificar(nombre_nuevo, rfc_nuevo, telefono_nuevo, correo_nuevo, nombre_buscar, conexion):
    try:
        cursor = conexion.cursor()
        sql = "UPDATE proveedores SET nombre=%s, rfc=%s, telefono=%s, correo=%s WHERE nombre=%s"
        valores = (nombre_nuevo, rfc_nuevo, telefono_nuevo, correo_nuevo, nombre_buscar)
        cursor.execute(sql, valores)
        conexion.commit()
        afectados = cursor.rowcount
        cursor.close()
        return afectados > 0
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al modificar proveedor: {err}")
        return False

def vaciar(conexion):
    try:
        cursor = conexion.cursor()
        sql = "TRUNCATE TABLE proveedores"
        cursor.execute(sql)
        conexion.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al vaciar proveedores: {err}")
        return False
    
#update peliculas set nombre = %s where nombre = "nombre pelicula"