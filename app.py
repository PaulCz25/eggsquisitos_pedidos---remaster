from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from collections import defaultdict
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
    "Kid Cheese": 95
}

platillos_con_huevo = ["Slam", "Americano", "French Plate", "Mini", "2x2"]

@app.route('/')
def por_entregar():
    return render_template("por_entregar.html", pedidos=pendientes)

@app.route('/pedidos')
def ver_pedidos():
    return render_template("pedidos.html", menu=menu, huevo_menu=platillos_con_huevo)

@app.route('/historial')
def historial():
    return render_template("historial.html", pedidos=entregados)

@app.route('/online')
def online():
    return render_template("online.html", menu=menu, huevo_menu=platillos_con_huevo)

@app.route('/pedido', methods=['POST'])
def hacer_pedido():
    # ...
    tiempo_entrega = request.form.get('tiempo_entrega', '').strip()
    tiempo_entrega_segundos = None

    if tipo_pedido == "online":
        try:
            minutos = int(tiempo_entrega)
            tiempo_entrega_segundos = minutos * 60
        except:
            tiempo_entrega_segundos = None

    pedido = {
        #...
        "timestamp": int(time.time()) if tipo_pedido == "online" else None,
        "tiempo_entrega_segundos": tiempo_entrega_segundos
        "id": len(pendientes) + len(entregados) + 1,
        "conteo": conteo,
        "notas": notas,
        "huevos": dict(huevos),
        "total": total,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "tipo": tipo_pedido,
        "tiempo_entrega": tiempo_entrega if tipo_pedido == "online" else None,
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
