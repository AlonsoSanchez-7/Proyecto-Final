import mysql.connector
from colorama import Fore

# constantes
iva_porcentaje = 0.16
ganancia_porcentaje = 0.30
descuento_mayoreo_porcentaje = 0.10

def calcular_metricas(costo_unitario, stock_actual):
    # 20 expresiones algorítmicas
    costo_iva = costo_unitario * (1 + iva_porcentaje)
    precio_venta = costo_unitario * (1 + ganancia_porcentaje)
    precio_venta_iva = precio_venta * (1 + iva_porcentaje)
    ganancia_unitario = precio_venta - costo_unitario
    inversion_total = costo_unitario * stock_actual
    venta_estimada = precio_venta * stock_actual
    ganancia_estimada = venta_estimada - inversion_total
    inversion_iva = inversion_total * (1 + iva_porcentaje)
    precio_mayoreo = precio_venta * (1 - descuento_mayoreo_porcentaje)
    ganancia_mayoreo_unitario = precio_mayoreo - costo_unitario
    ganancia_mayoreo_total = ganancia_mayoreo_unitario * stock_actual
    costo_30_unidades = costo_unitario * 30
    venta_30_unidades = precio_venta * 30
    ganancia_30_unidades = ganancia_unitario * 30
    stock_doble = stock_actual * 2
    inversion_doble = inversion_total * 2
    ganancia_doble = ganancia_estimada * 2
    costo_mitad_stock = costo_unitario * (stock_actual / 2)
    margen_rendimiento = (ganancia_unitario / costo_unitario) * 100 if costo_unitario > 0 else 0
    costo_proyectado_mas_5 = (costo_unitario * 1.05) * stock_actual

    return [
        costo_iva, precio_venta, precio_venta_iva, ganancia_unitario,
        inversion_total, venta_estimada, ganancia_estimada, inversion_iva,
        precio_mayoreo, ganancia_mayoreo_unitario, ganancia_mayoreo_total,
        costo_30_unidades, venta_30_unidades, ganancia_30_unidades,
        stock_doble, inversion_doble, ganancia_doble, costo_mitad_stock,
        margen_rendimiento, costo_proyectado_mas_5
    ]

def obtener_metricas_diccionario(costo_unitario, stock_actual):
    lista_m = calcular_metricas(costo_unitario, stock_actual)
    return {
        "costo_unitario": costo_unitario,
        "stock_actual": stock_actual,
        "costo_iva": lista_m[0],
        "precio_venta": lista_m[1],
        "precio_venta_iva": lista_m[2],
        "ganancia_unitario": lista_m[3],
        "inversion_total": lista_m[4],
        "venta_estimada": lista_m[5],
        "ganancia_estimada": lista_m[6],
        "margen_rendimiento": lista_m[18]
    }

def insertar(nombre, costo, stock, proveedor, conexion):
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO productos (nombre, costo, stock, proveedor) VALUES (%s, %s, %s, %s)"
        valores = (nombre, costo, stock, proveedor)
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
        sql = "SELECT id, nombre, costo, stock, proveedor FROM productos"
        cursor.execute(sql)
        registros = cursor.fetchall() # 
        cursor.close()
        return registros
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al consultar productos: {err}")
        return [] 

def buscar(nombre, conexion):
    try:
        cursor = conexion.cursor()
        sql = "SELECT id, nombre, costo, stock, proveedor FROM productos WHERE nombre LIKE %s"
        cursor.execute(sql, (f"%{nombre}%",))
        registros = cursor.fetchall()
        cursor.close()
        return registros
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al buscar producto: {err}")
        return []

def borrar(nombre, conexion):
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM productos WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        conexion.commit()
        afectados = cursor.rowcount
        cursor.close()
        return afectados > 0
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al eliminar producto: {err}")
        return False

def modificar(nombre_nuevo, costo_nuevo, stock_nuevo, proveedor_nuevo, nombre_buscar, conexion):
    try:
        cursor = conexion.cursor()
        sql = "UPDATE productos SET nombre=%s, costo=%s, stock=%s, proveedor=%s WHERE nombre=%s"
        valores = (nombre_nuevo, costo_nuevo, stock_nuevo, proveedor_nuevo, nombre_buscar)
        cursor.execute(sql, valores)
        conexion.commit()
        afectados = cursor.rowcount
        cursor.close()
        return afectados > 0
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al modificar producto: {err}")
        return False

def vaciar(conexion):
    try:
        cursor = conexion.cursor()
        sql = "TRUNCATE TABLE productos"
        cursor.execute(sql)
        conexion.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(Fore.RED + f"\n  ❌ Error al vaciar productos: {err}")
        return False

def obtener_resumen_global(conexion):
    registros = consultar(conexion)
    if not registros:
        return None
    total_productos = len(registros) # Contador
    total_stock = sum(int(r[3]) for r in registros) # Contador
    inversion_global = sum(float(r[2]) * int(r[3]) for r in registros) # acumuluador
    
    venta_global = 0
    for r in registros:
        m = calcular_metricas(float(r[2]), int(r[3]))
        venta_global += m[5] # acumulador
        
    ganancia_global = venta_global - inversion_global # acumulador
    return {
        "total_productos": total_productos,
        "total_stock": total_stock,
        "inversion_global": inversion_global,
        "venta_global": venta_global,
        "ganancia_global": ganancia_global
    }