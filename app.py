from flask import Flask, render_template, request, redirect
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Pedidos globales
pendientes = []
entregados = []

# Menú con precios
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

# Platillos que requieren tipo de huevo
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

@app.route('/pedido', methods=['POST'])
def hacer_pedido():
    items_seleccionados = request.form.getlist('item')
    notas = request.form.get('notas', '').strip()

    conteo = {}
    huevos = defaultdict(list)
    total = 0

    for item in items_seleccionados:
        cantidad = int(request.form.get(f'cantidad_{item}', 1))
        conteo[item] = cantidad
        total += menu[item] * cantidad

        if item in platillos_con_huevo:
            huevo_terminos = request.form.getlist(f'huevo_{item}[]')
            huevos[item] = huevo_terminos[:cantidad]  # solo tomamos tantos como cantidad

    pedido = {
        "id": len(pendientes) + len(entregados) + 1,
        "conteo": conteo,
        "notas": notas,
        "huevos": dict(huevos),  # diccionario con listas de tipo de huevo
        "total": total,
        "hora": datetime.now().strftime("%H:%M:%S")
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


