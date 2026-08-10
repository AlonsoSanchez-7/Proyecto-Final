from funciones import *
from productos.productos import *
from proveedores.proveedores import *

def menuGeneral():
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("      🛠️ SISTEMA DE CONTROL DE REFACCIONARIA (REFACCONTROL) 🛠️")
    print("="*60)
    print(Fore.YELLOW + "  1. 📦 Módulo de Productos (Inventario y Métricas)")
    print(Fore.BLUE +   "  2. 🏭 Módulo de Proveedores (Directorio)")
    print(Fore.RED + Style.BRIGHT + "  3. 🚪 Salir del Sistema")
    print(Fore.CYAN + "="*60)
    return input(Fore.WHITE + Style.BRIGHT + "  Seleccione una opción (1-3): ").strip()

def flujoProductos(conexionBD):
    while True:
        opc = menuProductos()
        if opc == "1":
            agregarProductos(conexionBD)
        elif opc == "2":
            mostrarProductos(conexionBD)
        elif opc == "3":
            buscarProductos(conexionBD)
        elif opc == "4":
            borrarProductos(conexionBD)
        elif opc == "5":
            modificarProductos(conexionBD)
        elif opc == "6":
            limpiarProductos(conexionBD)
        elif opc == "7":
            exportarReporteTXT(conexionBD)
        elif opc == "8":
            break
        else:
            print("\n\t\t...Opción no válida...")
            espereTecla()

def flujoProveedores(conexionBD):
    while True:
        opc = menuProveedores()
        if opc == "1":
            agregarProveedores(conexionBD)
        elif opc == "2":
            mostrarProveedores(conexionBD)
        elif opc == "3":
            buscarProveedores(conexionBD)
        elif opc == "4":
            borrarProveedores(conexionBD)
        elif opc == "5":
            modificarProveedores(conexionBD)
        elif opc == "6":
            limpiarProveedores(conexionBD)
        elif opc == "7":
            break
        else:
            print("\n\t\t...Opción no válida...")
            espereTecla()

def main():
    conexionBD = conectarBD()
    if not conexionBD:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ No se pudo conectar a MySQL. Verifique que XAMPP / MySQL esté activo.")
        espereTecla()
        return

    while True:
        opc = menuGeneral()
        if opc == "1":
            flujoProductos(conexionBD)
        elif opc == "2":
            flujoProveedores(conexionBD)
        elif opc == "3":
            conexionBD.close()
            limpiarPantalla()
            print("\n\t... Gracias por usar RefacControl. Hasta luego ...\n")
            break
        else:
            print("\n\t\t...Opción no válida...")
            espereTecla()

if __name__ == "__main__":
    main()