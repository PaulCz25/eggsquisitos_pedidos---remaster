from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from collections import defaultdict, Counter
import time

app = Flask(__name__)

pendientes = []
entregados = []

menu = {
    "Slam": 150,
    "Hotcakes": 70,
    "Hotcakes con fruta": 95,
    "Bacon": 95,
    "Muffin": 95,
    "Croissant": 95,
    "2x2": 105,
    "Sándwich": 125,
    "Americano": 125,
    "French Plate": 125,
    "Mini": 95,
    "Chilaquiles": 125,
    "Chilaquiles Deluxe": 150,
    "Kid Cheese": 95,
    "Cafe Americano 12Oz": 35,
    "Cafe Americano 16Oz": 45,
    "Licuado Fresa": 65,
    "Licuado Platano": 65,
    "Licuado Platano-Fresa": 65,
    "Licuado Platano-Choco": 65,
    "Licuado Chocomil": 55,
    "Jugo de naranja": 45,
    "Jugo verde": 65,
    "Soda": 35
}

platillos_con_huevo = ["Slam", "Americano", "French Plate", "Mini", "2x2", "Chilaquiles", "Chilaquiles Deluxe"]

@app.route('/')
def por_entregar():
    pendientes_ordenados = sorted(pendientes, key=lambda x: x["timestamp"] or 0)
    return render_template("por_entregar.html", pedidos=pendientes_ordenados)

@app.route('/pedidos')
def ver_pedidos():
    return render_template("pedidos.html", menu=menu, huevo_menu=platillos_con_huevo)

@app.route('/historial')
def historial():
    entregados_ordenados = sorted(entregados, key=lambda x: x.get("fecha_entrega", ""), reverse=True)

    pedidos_por_dia = {}
    ganancias_por_dia = {}
    conteo_platillos = Counter()
    total_ganancias = 0
    total_pedidos = len(entregados)

    for pedido in entregados:
        fecha = pedido.get("fecha_entrega", "").split(" ")[0]
        pedidos_por_dia[fecha] = pedidos_por_dia.get(fecha, 0) + 1
        ganancias_por_dia[fecha] = ganancias_por_dia.get(fecha, 0) + pedido["total"]
        total_ganancias += pedido["total"]

        for platillo, cantidad in pedido["conteo"].items():
            conteo_platillos[platillo] += cantidad

    pedidos_por_dia_lista = sorted(pedidos_por_dia.items())
    ganancias_por_dia_lista = sorted(ganancias_por_dia.items())
    platillos_mas_pedidos = conteo_platillos.most_common(10)

    return render_template(
        "historial.html",
        pedidos=entregados_ordenados,
        pedidos_por_dia=pedidos_por_dia_lista,
        ganancias_por_dia=ganancias_por_dia_lista,
        platillos_mas_pedidos=platillos_mas_pedidos,
        total_ganancias=total_ganancias,
        total_pedidos=total_pedidos
    )

@app.route('/online')
def online():
    return render_template("online.html", menu=menu, huevo_menu=platillos_con_huevo)

@app.route('/pedido', methods=['POST'])
def hacer_pedido():
    tipo_pedido = request.form.get('tipo_pedido', 'presencial')
    notas = request.form.get('notas', '').strip()
    tiempo_entrega = request.form.get('tiempo_entrega', '').strip()
    tiempo_entrega_segundos = None

    if tipo_pedido == "online":
        try:
            minutos = int(tiempo_entrega)
            tiempo_entrega_segundos = minutos * 60
        except:
            tiempo_entrega_segundos = 0

    items_seleccionados = request.form.getlist('item')
    conteo = defaultdict(int)
    huevos = defaultdict(list)
    total = 0

    for item in items_seleccionados:
        cantidad = request.form.get(f'cantidad_{item}', '1')
        try:
            cantidad = int(cantidad)
        except:
            cantidad = 1
        conteo[item] += cantidad
        total += menu.get(item, 0) * cantidad

        if item in platillos_con_huevo:
            huevos_item = request.form.getlist(f'huevo_{item}[]')
            huevos[item].extend(huevos_item)

    pedido = {
        "id": len(pendientes) + len(entregados) + 1,
        "conteo": dict(conteo),
        "notas": notas,
        "huevos": dict(huevos),
        "total": total,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "tipo": tipo_pedido,
        "tiempo_entrega": tiempo_entrega if tipo_pedido == "online" else None,
        "tiempo_entrega_segundos": tiempo_entrega_segundos if tipo_pedido == "online" else None,
        "timestamp": int(time.time()) if tipo_pedido == "online" else None
    }

    pendientes.append(pedido)
    return redirect('/')

@app.route("/entregar/<int:pedido_id>", methods=["POST"])
def marcar_entregado(pedido_id):
    for pedido in pendientes:
        if pedido["id"] == pedido_id:
            pendientes.remove(pedido)
            pedido["fecha_entrega"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            entregados.append(pedido)
            break
    return redirect('/')

@app.route('/check_nuevos')
def check_nuevos():
    return {"total": len(pendientes)}
