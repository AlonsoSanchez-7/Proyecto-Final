from funciones import *
from productos import crud

def menuProductos():
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("        ⚙️ SISTEMA REFACCONTROL - MÓDULO PRODUCTOS ⚙️")
    print("="*60)
    print(Fore.YELLOW + "  1. 📦 Agregar nuevo producto")
    print(Fore.GREEN +  "  2. 📋 Consultar productos y métricas")
    print(Fore.CYAN +   "  3. 🔍 Buscar producto por nombre")
    print(Fore.RED +    "  4. ❌ Borrar producto")
    print(Fore.BLUE +   "  5. ✏️ Modificar producto")
    print(Fore.MAGENTA +"  6. 🗑️ Vaciar tabla de productos")
    print(Fore.WHITE + Style.BRIGHT + "  7. 📄 Exportar reporte financiero a TXT")
    print(Fore.RED + Style.BRIGHT + "  8. 🔙 Regresar al Menú Principal")
    print(Fore.CYAN + "="*60)
    return input(Fore.WHITE + Style.BRIGHT + "  Seleccione una opción (1-8): ").strip()

def agregarProductos(conexionBD):
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("                 📦 AGREGAR NUEVO PRODUCTO                  ")
    print("="*60)
    nombre = validarTexto(Fore.YELLOW + "  Ingrese nombre del producto: ")
    costo = validarNumero(Fore.GREEN + "  Ingrese costo unitario ($): ", tipo="float")
    stock = validarNumero(Fore.CYAN + "  Ingrese cantidad en stock: ", tipo="int")
    proveedor = validarTexto(Fore.MAGENTA + "  Ingrese nombre del proveedor: ")
    
    if crud.insertar(nombre, costo, stock, proveedor, conexionBD):
        accionExitosa()
    else:
        accionNoExitosa()

def mostrarProductos(conexionBD):
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("         📋 CONSULTA DE PRODUCTOS Y MÉTRICAS              ")
    print("="*60)
    registros = crud.consultar(conexionBD)
    
    if registros:
        for r in registros:
            c = float(r[2])
            s = int(r[3])
            m = crud.calcular_metricas(c, s)
            print(Fore.YELLOW + "="*60)
            print(Fore.WHITE + Style.BRIGHT + f"  🆔 ID: {r[0]} | 🛠️ Producto: {r[1]} | 🏭 Proveedor: {r[4]}")
            print(Fore.GREEN + f"  💲 Costo Unitario: ${c:.2f} | 📦 Stock: {s} pzas")
            print(Fore.CYAN + f"  🏷️ Precio Venta: ${m[1]:.2f} (con IVA: ${m[2]:.2f})")
            print(Fore.BLUE + f"  💵 Ganancia Unitario: ${m[3]:.2f} | 📈 Rendimiento: {m[18]:.1f}%")
            print(Fore.MAGENTA + f"  💰 Inversión Total: ${m[4]:.2f} | 📊 Ganancia Estimada: ${m[6]:.2f}")
        
        print(Fore.YELLOW + "="*60)
        resumen = crud.obtener_resumen_global(conexionBD)
        if resumen:
            print(Back.BLUE + Fore.WHITE + Style.BRIGHT + "                   📊 RESUMEN GLOBAL                       " + Style.RESET_ALL)
            print(Fore.WHITE + f"  📦 Total Ítems: {resumen['total_productos']} | Unidades Stock: {resumen['total_stock']}")
            print(Fore.GREEN + f"  💰 Inversión Global: ${resumen['inversion_global']:.2f}")
            print(Fore.CYAN + f"  💵 Venta Proyectada: ${resumen['venta_global']:.2f}")
            print(Fore.YELLOW + Style.BRIGHT + f"  📈 Utilidad Proyectada: ${resumen['ganancia_global']:.2f}")
        espereTecla()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ No hay productos registrados en la base de datos.")
        espereTecla()

def buscarProductos(conexionBD):
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("                 🔍 BUSCAR PRODUCTO POR NOMBRE             ")
    print("="*60)
    nombre = validarTexto(Fore.YELLOW + "  Ingrese el nombre del producto a buscar: ")
    registros = crud.buscar(nombre, conexionBD)
    
    if registros:
        for r in registros:
            c = float(r[2])
            s = int(r[3])
            dict_m = crud.obtener_metricas_diccionario(c, s)
            print(Fore.YELLOW + "="*60)
            print(Fore.WHITE + Style.BRIGHT + f"  🆔 ID: {r[0]} | 🛠️ Producto: {r[1]} | 🏭 Proveedor: {r[4]}")
            print(Fore.GREEN + f"  💲 Costo: ${dict_m['costo_unitario']:.2f} | 🏷️ Venta: ${dict_m['precio_venta']:.2f}")
            print(Fore.CYAN + f"  💰 Inversión: ${dict_m['inversion_total']:.2f} | 📊 Ganancia Est: ${dict_m['ganancia_estimada']:.2f}")
        print(Fore.YELLOW + "="*60)
        espereTecla()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ No se encontraron productos coincidentes.")
        espereTecla()

def borrarProductos(conexionBD):
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("                   ❌ BORRAR PRODUCTO                      ")
    print("="*60)
    nombre = validarTexto(Fore.YELLOW + "  Nombre exacto del producto a eliminar: ")
    encontrados = crud.buscar(nombre, conexionBD)
    
    if encontrados:
        confirmar = input(Fore.RED + Style.BRIGHT + f"  ⚠️ ¿Seguro que desea eliminar '{nombre}'? (S/N): ").strip().upper()
        if confirmar == "S":
            if crud.borrar(nombre, conexionBD):
                accionExitosa()
            else:
                accionNoExitosa()
        else:
            print(Fore.YELLOW + "\n  ⚠️ Operación cancelada por el usuario.")
            espereTecla()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ El producto especificado no existe.")
        espereTecla()

def modificarProductos(conexionBD):
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("                  ✏️ MODIFICAR PRODUCTO                     ")
    print("="*60)
    nombre_buscar = validarTexto(Fore.YELLOW + "  Nombre exacto del producto a modificar: ")
    encontrados = crud.buscar(nombre_buscar, conexionBD)
    
    if encontrados:
        print(Fore.WHITE + Style.BRIGHT + "\n  Ingrese los nuevos datos del producto:")
        nombre_nuevo = validarTexto(Fore.YELLOW + "  Nuevo nombre: ")
        costo_nuevo = validarNumero(Fore.GREEN + "  Nuevo costo ($): ", tipo="float")
        stock_nuevo = validarNumero(Fore.CYAN + "  Nuevo stock: ", tipo="int")
        proveedor_nuevo = validarTexto(Fore.MAGENTA + "  Nuevo proveedor: ")
        
        if crud.modificar(nombre_nuevo, costo_nuevo, stock_nuevo, proveedor_nuevo, nombre_buscar, conexionBD):
            accionExitosa()
        else:
            accionNoExitosa()
    else:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ El producto especificado no existe.")
        espereTecla()

def limpiarProductos(conexionBD):
    limpiarPantalla()
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "="*60)
    print("              🗑️ VACIAR TABLA DE PRODUCTOS                 ")
    print("="*60)
    confirmar = input(Fore.YELLOW + Style.BRIGHT + "  ⚠️ ¿Está COMPLETAMENTE SEGURO de vaciar la tabla? (S/N): ").strip().upper()
    if confirmar == "S":
        if crud.vaciar(conexionBD):
            accionExitosa()
        else:
            accionNoExitosa()
    else:
        print(Fore.YELLOW + "\n  ⚠️ Operación cancelada por el usuario.")
        espereTecla()

def exportarReporteTXT(conexionBD):
    limpiarPantalla()
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print("         📄 EXPORTAR REPORTE FINANCIERO A TXT             ")
    print("="*60)
    registros = crud.consultar(conexionBD)
    if not registros:
        print(Fore.RED + Style.BRIGHT + "\n  ⚠️ No hay datos para exportar.")
        espereTecla()
        return

    try:
        with open("reporte_inventario.txt", "w", encoding="utf-8") as f:
            f.write("="*60)
            f.write("\n      🛠️ REPORTE DE INVENTARIO Y MÉTRICAS - REFACCONTROL   \n")
            f.write("="*60)
            for r in registros:
                c = float(r[2])
                s = int(r[3])
                dict_m = crud.obtener_metricas_diccionario(c, s)
                f.write(f"\nID: {r[0]} | Producto: {r[1]} | Proveedor: {r[4]}\n")
                f.write(f"  - Costo Unitario: ${dict_m['costo_unitario']:.2f}\n")
                f.write(f"  - Stock: {dict_m['stock_actual']} pzas\n")
                f.write(f"  - Precio Venta Estimado: ${dict_m['precio_venta']:.2f}\n")
                f.write(f"  - Inversión Total: ${dict_m['inversion_total']:.2f}\n")
                f.write(f"  - Ganancia Estimada: ${dict_m['ganancia_estimada']:.2f}\n")
                f.write(f"  - Rendimiento: {dict_m['margen_rendimiento']:.1f}%\n")
                f.write("-" * 60 + "\n")
            
            resumen = crud.obtener_resumen_global(conexionBD)
            if resumen:
                f.write("="*60)
                f.write("\n                     RESUMEN GLOBAL                         \n")
                f.write("="*60)
                f.write(f"\nTotal Ítems: {resumen['total_productos']}\n")
                f.write(f"Total Unidades Stock: {resumen['total_stock']}\n")
                f.write(f"Inversión Global: ${resumen['inversion_global']:.2f}\n")
                f.write(f"Venta Proyectada: ${resumen['venta_global']:.2f}\n")
                f.write(f"Utilidad Proyectada: ${resumen['ganancia_global']:.2f}\n")

        print(Fore.GREEN + Style.BRIGHT + "\n  ✅ Archivo 'reporte_inventario.txt' generado con éxito en el directorio raíz.")
        espereTecla()
    except Exception as e:
        print(Fore.RED + f"\n  ❌ Error al exportar archivo: {e}")
        espereTecla()