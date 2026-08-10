from funciones import *
from proveedores import crud

def menuProveedores():
    limpiarPantalla()
    print(Fore.BLUE + Style.BRIGHT + "="*60)
    print("        🏭 SISTEMA REFACCONTROL - MÓDULO PROVEEDORES 🏭")
    print("="*60)
    print(Fore.YELLOW + "  1. ✏️ Registrar nuevo proveedor")
    print(Fore.GREEN +  "  2. 📖 Consultar directorio de proveedores")
    print(Fore.CYAN +   "  3. 🔍 Buscar proveedor por empresa")
    print(Fore.RED +    "  4. ❌ Eliminar proveedor")
    print(Fore.BLUE +   "  5. 🖊️ Modificar datos de proveedor")
    print(Fore.MAGENTA +"  6. 🗑️ Vaciar catálogo de proveedores")
    print(Fore.WHITE + Style.BRIGHT + "  7. 🔙 Regresar al Menú Principal")
    print(Fore.BLUE + "="*60)
    return input(Fore.WHITE + Style.BRIGHT + "  Seleccione una opción (1-7): ").strip()

def agregarProveedores(conexionBD):
    limpiarPantalla()
    print(Fore.BLUE + Style.BRIGHT + "="*60)
    print("               ✏️ REGISTRAR NUEVO PROVEEDOR                ")
    print("="*60)
    nombre = validarTexto(Fore.YELLOW + "  🏢 Nombre de la Empresa: ")
    rfc = validarTexto(Fore.CYAN + "  👤 RFC: ")
    telefono = validarTelefono(Fore.GREEN + "  📞 Teléfono de contacto: ")
    correo = validarCorreo(Fore.MAGENTA + "  ✉️ Correo electrónico: ")
    
    if crud.insertar(nombre, rfc, telefono, correo, conexionBD):
        accionExitosa()
    else:
        accionNoExitosa()

def mostrarProveedores(conexionBD):
    limpiarPantalla()
    print(Fore.BLUE + Style.BRIGHT + "="*60)
    print("             📖 DIRECTORIO DE PROVEEDORES                   ")
    print("="*60)
    registros = crud.consultar(conexionBD)
    
    if registros:
        for r in registros:
            print(Fore.YELLOW + "="*60)
            print(Fore.WHITE + Style.BRIGHT + f"  🆔 ID: {r[0]} | 🏢 Empresa: {r[1]}")
            print(Fore.CYAN + f"  👤 rfc: {r[2]}")
            print(Fore.GREEN + f"  📞 Teléfono: {r[3]} | ✉️ Email: {r[4]}")
        print(Fore.YELLOW + "="*60)
        espereTecla()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ No hay proveedores registrados.")
        espereTecla()

def buscarProveedores(conexionBD):
    limpiarPantalla()
    print(Fore.BLUE + Style.BRIGHT + "="*60)
    print("             🔍 BUSCAR PROVEEDOR POR EMPRESA                ")
    print("="*60)
    nombre = validarTexto(Fore.CYAN + "  Ingrese el nombre de la empresa a buscar: ")
    registros = crud.buscar(nombre, conexionBD)
    
    if registros:
        for r in registros:
            print(Fore.YELLOW + "="*60)
            print(Fore.WHITE + Style.BRIGHT + f"  🆔 ID: {r[0]} | 🏢 Empresa: {r[1]}")
            print(Fore.CYAN + f"  👤 RFC: {r[2]} | 📞 Teléfono: {r[3]}")
        print(Fore.YELLOW + "="*60)
        espereTecla()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ No se encontraron coincidencias.")
        espereTecla()

def borrarProveedores(conexionBD):
    limpiarPantalla()
    print(Fore.BLUE + Style.BRIGHT + "="*60)
    print("                  ❌ ELIMINAR PROVEEDOR                     ")
    print("="*60)
    nombre = validarTexto(Fore.CYAN + "  Nombre exacto de la empresa a eliminar: ")
    encontrados = crud.buscar(nombre, conexionBD)
    
    if encontrados:
        confirmar = input(Fore.RED + Style.BRIGHT + f"  ⚠️ ¿Está seguro de eliminar '{nombre}'? (S/N): ").strip().upper()
        if confirmar == "S":
            if crud.borrar(nombre, conexionBD):
                accionExitosa()
            else:
                accionNoExitosa()
        else:
            print(Fore.YELLOW + "\n  ⚠️ Operación cancelada por el usuario.")
            espereTecla()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ La empresa especificada no existe.")
        espereTecla()

def modificarProveedores(conexionBD):
    limpiarPantalla()
    print(Fore.BLUE + Style.BRIGHT + "="*60)
    print("               🖊️ MODIFICAR PROVEEDOR                       ")
    print("="*60)
    nombre_buscar = validarTexto(Fore.CYAN + "  Nombre exacto de la empresa a modificar: ")
    encontrados = crud.buscar(nombre_buscar, conexionBD)
    
    if encontrados:
        print(Fore.WHITE + Style.BRIGHT + "\n  Ingrese los nuevos datos del proveedor:")
        nombre_nuevo = validarTexto(Fore.YELLOW + "  🏢 Proveedor nuevo: ")
        rfc_nuevo = validarTexto(Fore.CYAN + "  👤 RFC: ")
        telefono_nuevo = validarTelefono(Fore.GREEN + "  📞 Nuevo teléfono: ")
        correo_nuevo = validarCorreo(Fore.MAGENTA + "  ✉️ Nuevo correo: ")
        
        if crud.modificar(nombre_nuevo, rfc_nuevo, telefono_nuevo, correo_nuevo, nombre_buscar, conexionBD):
            accionExitosa()
        else:
            accionNoExitosa()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ La empresa especificada no existe.")
        espereTecla()

def limpiarProveedores(conexionBD):
    limpiarPantalla()
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "="*60)
    print("              🗑️ VACIAR CATÁLOGO DE PROVEEDORES              ")
    print("="*60)
    confirmar = input(Fore.YELLOW + Style.BRIGHT + "  ⚠️ ¿Está SEGURO de eliminar TODOS los proveedores? (S/N): ").strip().upper()
    if confirmar == "S":
        if crud.vaciar(conexionBD):
            accionExitosa()
        else:
            accionNoExitosa()
    else:
        print(Fore.YELLOW + "\n  ⚠️ Operación cancelada por el usuario.")
        espereTecla()