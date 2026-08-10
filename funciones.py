import mysql.connector
import re
import colorama
colorama.init()
from colorama import Fore, Style, Back

def limpiarPantalla():
    print("\033c")

def conectarBD():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bd_refactions"
        )
        return conexion
    except mysql.connector.Error as err:
        print(Fore.RED + Style.BRIGHT + f"\n  ❌ Error al conectar a MySQL: {err}")
        return None
        
def validarTexto(mensaje):
    texto = r'^[a-zA-Z0-9\sñÑáéíóúÁÉÍÓÚ\.\-]+$'
    while True:
        cadena = input(mensaje).strip()
        if re.match(texto, cadena) and len(cadena) > 0:
            return cadena
        print(Fore.RED + "\t...⚠️ ¡Entrada no válida! Ingrese un texto válido...")

def validarCorreo(mensaje):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    while True:
        cadena = input(mensaje).strip()
        if re.match(patron, cadena):
            return cadena
        print(Fore.RED + "\t...⚠️ ¡Entrada no válida! Ingrese un correo electrónico válido...")

def validarTelefono(mensaje):
    patron = r'^\d{10}$' 
    while True:
        cadena = input(mensaje).strip()
        if re.match(patron, cadena):
            return cadena
        print(Fore.RED + "\t...⚠️ ¡Entrada no válida! Ingrese un número telefónico válido (10 dígitos)...")
        
def validarNumero(mensaje, tipo="float"):
    while True:
        try:
            val = input(mensaje).strip()
            if tipo == "int":
                num = int(val)
            else:
                num = float(val)
            if num >= 0:
                return num
            print(Fore.RED + "\t...⚠️ ¡Error! Ingrese un número mayor o igual a 0...")
        except ValueError:
            print(Fore.RED + "\t...⚠️ ¡Error! Ingrese un valor numérico válido...")

def espereTecla():
    input(Fore.YELLOW + Style.BRIGHT + "\n  👉 Presione ENTER para continuar...")

def accionExitosa():
    print(Fore.GREEN + Style.BRIGHT + "\n\t\t...✅ Operación realizada con ÉXITO...")
    espereTecla()

def accionNoExitosa():
    print(Fore.RED + Style.BRIGHT + "\n\t\t...❌ No se pudo realizar la operación...")
    espereTecla()