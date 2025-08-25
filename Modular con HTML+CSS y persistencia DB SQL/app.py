# app.py


#Importo flash para conexión WEB y re para normalización de placas
from flask import Flask, render_template, request, redirect, url_for, flash
from administracion import AdministracionParqueo
from parqueo import Parqueo
from vehiculo import Vehiculo
import re


app = Flask(__name__)
app.secret_key = "Est03smiS3cr3tK3y$0L0P@r@m1Pr0Y3cT0"

# Instancias de admnistracion y parqueo
admin = AdministracionParqueo()
parqueo = Parqueo(admin)

# Diccionario para almacenar los atributos conocidos de vehículos ya registrados
vehiculos_conocidos = {}


def normalizar_placa(txt):
    if not txt:
        return ""
    return re.sub(r"\s+", "", txt).upper()

def etiqueta_humana(clave):
    if not clave:
        return ""
    pref = clave[:1].upper()
    num = clave[1:]
    try:
        n = int(num)
    except:
        n = int(num.lstrip("0") or "0")
    return f"{pref}{n}"

def contar_libres():
    libres_autos = sum(1 for v in parqueo.espacios.espacios_autos.values() if v is None)
    libres_motos = sum(1 for v in parqueo.espacios.espacios_motos.values() if v is None)
    return libres_autos, libres_motos

# Matriz para parqueo
def matriz_parqueo():
    filas = []
    
    # Espera
    fila_espera = []
    for k in sorted(parqueo.cola.espacios_cola.keys()):
        placa = parqueo.cola.espacios_cola[k]
        fila_espera.append({
            "label": etiqueta_humana(k),
            "placa": placa,
            "ocupado": placa is not None
        })
    filas.append(fila_espera)
    # Valet
    fila_valet = []
    for k in sorted(parqueo.valet.espacios_valet.keys()):
        placa = parqueo.valet.espacios_valet[k]
        fila_valet.append({
            "label": etiqueta_humana(k),
            "placa": placa,
            "ocupado": placa is not None
        })
    filas.append(fila_valet)
    # Motos
    fila_motos = []
    for k in sorted(parqueo.espacios.espacios_motos.keys()):
        placa = parqueo.espacios.espacios_motos[k]
        fila_motos.append({
            "label": etiqueta_humana(k),
            "placa": placa,
            "ocupado": placa is not None
        })
    filas.append(fila_motos)
    # Autos (filas de hasta 10)
    autos_items = []
    for k in sorted(parqueo.espacios.espacios_autos.keys()):
        placa = parqueo.espacios.espacios_autos[k]
        autos_items.append({
            "label": etiqueta_humana(k),
            "placa": placa,
            "ocupado": placa is not None
        })
    for i in range(0, len(autos_items), 10):
        filas.append(autos_items[i:i+10])
    return filas

def render_con_matriz(template, **context):
    libres_autos, libres_motos = contar_libres()
    contexto_base = {
        "titulo": "Parqueo ATH",
        "libres_autos": libres_autos,
        "libres_motos": libres_motos,
        "matriz": matriz_parqueo()
    }
    contexto_base.update(context)
    return render_template(template, **contexto_base)

# Defino Rutas WEB
@app.route("/", methods=["GET"])
def index():
    return render_con_matriz("index.html")

# Para Ingresar vehículo 
@app.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if request.method == "GET":
        placa = normalizar_placa(request.args.get("placa", ""))
        datos = vehiculos_conocidos.get(placa) if placa else None
        return render_con_matriz("ingresar.html", placa=placa, datos=datos, ticket=None, opciones=None)

    placa = normalizar_placa(request.form.get("placa", ""))
    if not placa:
        flash("Por favor digite una placa válida.")
        return redirect(url_for("ingresar"))

    tipo = request.form.get("tipo", "").strip().lower()
    marca = request.form.get("marca", "").strip()
    modelo = request.form.get("modelo", "").strip()
    color = request.form.get("color", "").strip()

    if placa in vehiculos_conocidos:
        known = vehiculos_conocidos[placa]
        tipo = known.get("tipo", tipo) or tipo
        marca = known.get("marca", marca) or marca
        modelo = known.get("modelo", modelo) or modelo
        color = known.get("color", color) or color

    if tipo not in admin.tipos_vehiculo:
        flash("Este tipo de vehículo no es aceptado.")
        return redirect(url_for("ingresar", placa=placa))

    if placa in parqueo.vehiculos_dentro:
        flash("Este vehículo ya está dentro del parqueo.")
        return redirect(url_for("ingresar", placa=placa))

    for v in parqueo.cola.cola_espera_autos:
        if v.placa == placa:
            flash("Este vehículo ya está en la cola de espera.")
            return redirect(url_for("ingresar", placa=placa))
    for v in parqueo.valet.valet_autos:
        if v.placa == placa:
            flash("Este vehículo ya está en valet.")
            return redirect(url_for("ingresar", placa=placa))

    vehiculo = Vehiculo(placa, tipo)
    if hasattr(vehiculo, "marca"):
        vehiculo.marca = marca
    if hasattr(vehiculo, "modelo"):
        vehiculo.modelo = modelo
    if hasattr(vehiculo, "color"):
        vehiculo.color = color

    espacio = parqueo.espacios.asignar_espacio_libre(tipo, placa)

    if tipo == "moto":
        if espacio is None:
            flash("El parqueo para motos está lleno. No hay cola de espera para motos.")
            return redirect(url_for("ingresar", placa=placa))
        parqueo.vehiculos_dentro[placa] = vehiculo
        vehiculos_conocidos[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "color": color}
        ticket = {"tipo_ticket": "ingreso", "placa": placa, "tipo": tipo, "hora_entrada": vehiculo.hora_entrada, "espacio": espacio, "extra": ""}
        return render_con_matriz("ingresar.html", placa="", datos=None, ticket=ticket, opciones=None)

    if espacio is not None:
        parqueo.vehiculos_dentro[placa] = vehiculo
        vehiculos_conocidos[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "color": color}
        ticket = {"tipo_ticket": "ingreso", "placa": placa, "tipo": tipo, "hora_entrada": vehiculo.hora_entrada, "espacio": espacio, "extra": ""}
        return render_con_matriz("ingresar.html", placa="", datos=None, ticket=ticket, opciones=None)

    espacio_valet_disponible = next((k for k, v in parqueo.valet.espacios_valet.items() if v is None), None)
    espacio_cola_disponible = next((k for k, v in parqueo.cola.espacios_cola.items() if v is None), None)

    if not espacio_valet_disponible and not espacio_cola_disponible:
        flash("Parqueo lleno, valet lleno y cola de espera llena. Intente más tarde.")
        return redirect(url_for("ingresar", placa=placa))

    opciones = []
    if espacio_valet_disponible:
        opciones.append("valet")
    if espacio_cola_disponible:
        opciones.append("espera")

    return render_con_matriz("ingresar.html", placa=placa, datos={"tipo": tipo, "marca": marca, "modelo": modelo, "color": color}, ticket=None, opciones=opciones)

@app.route("/ingresar/opcion", methods=["POST"])
def ingresar_opcion():
    placa = normalizar_placa(request.form.get("placa"))
    tipo = request.form.get("tipo")
    marca = request.form.get("marca", "")
    modelo = request.form.get("modelo", "")
    color = request.form.get("color", "")
    seleccion = request.form.get("seleccion")

    if not placa or seleccion not in ("valet", "espera"):
        flash("Solicitud inválida.")
        return redirect(url_for("ingresar"))

    vehiculo = Vehiculo(placa, tipo)
    if hasattr(vehiculo, "marca"):
        vehiculo.marca = marca
    if hasattr(vehiculo, "modelo"):
        vehiculo.modelo = modelo
    if hasattr(vehiculo, "color"):
        vehiculo.color = color

    if seleccion == "valet":
        espacio_asignado = parqueo.valet.agregar_valet(vehiculo)
        if espacio_asignado is None:
            flash("No se pudo asignar el vehículo a valet. Intente luego.")
            return redirect(url_for("ingresar"))
        vehiculos_conocidos[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "color": color}
        ticket = {"tipo_ticket": "ingreso", "placa": placa, "tipo": tipo, "hora_entrada": vehiculo.hora_entrada, "espacio": espacio_asignado, "extra": "(Deja llaves)"}
        return render_con_matriz("ingresar.html", placa="", datos=None, ticket=ticket, opciones=None)

    if seleccion == "espera":
        espacio_asignado = parqueo.cola.agregar_cola_espera(vehiculo)
        if espacio_asignado is None:
            flash("No se pudo agregar a la cola de espera. Intente luego.")
            return redirect(url_for("ingresar"))
        vehiculos_conocidos[placa] = {"tipo": tipo, "marca": marca, "modelo": modelo, "color": color}
        ticket = {"tipo_ticket": "cola", "placa": placa, "tipo": tipo, "hora_entrada": vehiculo.hora_entrada, "espacio": espacio_asignado, "extra": "(Cola de espera)"}
        return render_con_matriz("ingresar.html", placa="", datos=None, ticket=ticket, opciones=None)

    flash("Opción inválida.")
    return redirect(url_for("ingresar"))

# Para Sacar vehículo 
@app.route("/salir", methods=["GET", "POST"])
def salir():
    if request.method == "GET":
        return render_con_matriz("salir.html", placa="", salida_ticket=None, ingreso_ticket=None)

    placa = normalizar_placa(request.form.get("placa", ""))
    if not placa:
        flash("Por favor digite una placa válida.")
        return redirect(url_for("salir"))

    resultado = parqueo.sacar_vehiculo(placa, web_mode=True)

    salida_registro = resultado.get("registro_salida")
    ingreso_info = resultado.get("ingreso_desde_cola")

    salida_ticket = None
    ingreso_ticket = None

    if salida_registro:
        salida_ticket = {
            "tipo_ticket": "salida",
            "placa": salida_registro.placa,
            "tipo": salida_registro.tipo,
            "hora_entrada": salida_registro.hora_entrada,
            "hora_salida": salida_registro.hora_salida,
            "total": salida_registro.total_pagado
        }

    if ingreso_info:
        v = ingreso_info["vehiculo"]
        esp = ingreso_info["espacio"]
        ingreso_ticket = {
            "tipo_ticket": "ingreso",
            "placa": v.placa,
            "tipo": v.tipo,
            "hora_entrada": v.hora_entrada,
            "espacio": esp
        }

    #Muestro opción para pasar de espera a valet
    pendientes = parqueo.mover_espera_a_valet(interactive=False)
    if pendientes:
        flash("Se liberó un espacio de valet. Puedes mover un vehículo de la cola a valet.")
        # no redirect automático: mostramos los tickets y la matriz; el usuario puede ir a mover_espera
    return render_con_matriz("salir.html", placa="", salida_ticket=salida_ticket, ingreso_ticket=ingreso_ticket)

#Muestro tickets y matriz sin redirigir
@app.route("/reingresar_calle", methods=["POST"])
def reingresar_calle():
    reingresos = parqueo.reingresar_calle()
    if reingresos:
        msgs = ", ".join([r["placa"] for r in reingresos])
        flash(f"Se reingresaron a valet: {msgs}")
    else:
        flash("No se reingresó ningún vehículo (verifique espacios).")
    return redirect(url_for("index"))

# Resto de rutas (espacios, cola, mover_espera, etc.)
@app.route("/espacios", methods=["GET"])
def espacios():
    listado = []
    # Filas de matriz (Calle ya no lo uso, pero lo dejé acá para ajuste próximo)
    for clave, placa in parqueo.calle.items():
        listado.append({"tipo": "Calle", "clave": clave.upper(), "placa": placa, "estado": "Ocupado" if placa else "Libre"})
    for clave, placa in parqueo.valet.espacios_valet.items():
        listado.append({"tipo": "Valet", "clave": etiqueta_humana(clave), "placa": placa, "estado": "Ocupado" if placa else "Libre"})
    for clave, placa in parqueo.cola.espacios_cola.items():
        listado.append({"tipo": "Espera", "clave": etiqueta_humana(clave), "placa": placa, "estado": "Ocupado" if placa else "Libre"})
    for clave, placa in parqueo.espacios.espacios_motos.items():
        listado.append({"tipo": "Moto", "clave": etiqueta_humana(clave), "placa": placa, "estado": "Ocupado" if placa else "Libre"})
    for clave, placa in parqueo.espacios.espacios_autos.items():
        listado.append({"tipo": "Auto", "clave": etiqueta_humana(clave), "placa": placa, "estado": "Ocupado" if placa else "Libre"})
    return render_con_matriz("espacios.html", listado=listado)

@app.route("/cola", methods=["GET"])
def cola():
    cola_list = [{"pos": i+1, "placa": v.placa, "tipo": v.tipo} for i, v in enumerate(parqueo.cola.cola_espera_autos)]
    return render_con_matriz("cola.html", cola_list=cola_list)

@app.route("/mover_espera", methods=["GET"])
def mover_espera():
    pendientes = parqueo.mover_espera_a_valet(interactive=False)
    return render_con_matriz("mover_espera.html", pendientes=pendientes)

@app.route("/mover_espera/mover", methods=["POST"])
def mover_espera_mover():
    placa = normalizar_placa(request.form.get("placa", ""))
    if not placa:
        flash("Placa inválida.")
        return redirect(url_for("mover_espera"))
    espacio = parqueo.aceptar_espera_a_valet(placa)
    if espacio:
        flash(f"Vehículo {placa} movido a valet (espacio {etiqueta_humana(espacio)}).")
    else:
        flash("No se pudo mover a valet (espacio ocupado o placa no encontrada).")
    return redirect(url_for("mover_espera"))

@app.route("/consultar", methods=["GET", "POST"])
def consultar():
    if request.method == "GET":
        return render_con_matriz("consultar.html", placa="", resultado=None)
    placa = normalizar_placa(request.form.get("placa", ""))
    if not placa:
        flash("Por favor digite una placa válida.")
        return redirect(url_for("consultar"))
    resultado = None
    if placa in parqueo.vehiculos_dentro:
        for k, v in parqueo.espacios.espacios_autos.items():
            if v == placa:
                resultado = f"El vehículo con placa {placa} está en el parqueo (Espacio {etiqueta_humana(k)})."
                break
    if not resultado:
        for k, v in parqueo.valet.espacios_valet.items():
            if v == placa:
                resultado = f"El vehículo con placa {placa} está en valet (Espacio {etiqueta_humana(k)})."
                break
    if not resultado:
        for k, v in parqueo.cola.espacios_cola.items():
            if v == placa:
                resultado = f"El vehículo con placa {placa} está en la cola de espera (Espacio {etiqueta_humana(k)})."
                break
    if not resultado:
        for clave, placa_calle in parqueo.calle.items():
            if placa_calle == placa:
                resultado = f"El vehículo con placa {placa} está temporalmente en {clave.upper()} (calle)."
                break
    if not resultado:
        resultado = f"El vehículo con placa {placa} no está en el parqueo, valet ni en la cola."
    datos = vehiculos_conocidos.get(placa)
    return render_con_matriz("consultar.html", placa=placa, resultado=resultado, datos=datos)

@app.route("/historial", methods=["GET", "POST"])
def historial():
    if request.method == "GET":
        return render_con_matriz("historial.html", placa="", registros=None)
    placa = normalizar_placa(request.form.get("placa", ""))
    if not placa:
        flash("Por favor digite una placa válida.")
        return redirect(url_for("historial"))
    registros = parqueo.historial.buscar_por_placa(placa)
    regs = []
    for r in registros:
        regs.append({"placa": r.placa, "tipo": r.tipo, "entrada": r.hora_entrada, "salida": r.hora_salida, "total": r.total_pagado})
    return render_con_matriz("historial.html", placa=placa, registros=regs)

@app.route("/admin", methods=["GET", "POST"])
def admin_view():
    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "cambiar_autos":
            try:
                nuevo = int(request.form.get("cantidad_autos", "0"))
                admin.cambiar_espacios_autos(nuevo)
                parqueo.actualizar_espacios()
                flash("Cantidad de espacios para autos actualizada.")
            except:
                flash("Valor inválido.")
        elif accion == "cambiar_motos":
            try:
                nuevo = int(request.form.get("cantidad_motos", "0"))
                admin.cambiar_espacios_motos(nuevo)
                parqueo.actualizar_espacios()
                flash("Cantidad de espacios para motos actualizada.")
            except:
                flash("Valor inválido.")
        elif accion == "tarifa_auto":
            try:
                nueva = int(request.form.get("tarifa_auto", "0"))
                admin.cambiar_tarifa("auto", nueva)
                flash("Tarifa de auto actualizada.")
            except:
                flash("Valor inválido.")
        elif accion == "tarifa_moto":
            try:
                nueva = int(request.form.get("tarifa_moto", "0"))
                admin.cambiar_tarifa("moto", nueva)
                flash("Tarifa de moto actualizada.")
            except:
                flash("Valor inválido.")
        elif accion == "cobro":
            metodo = request.form.get("metodo_cobro", "horas")
            admin.cambiar_cobro(metodo == "fraccionado")
            flash("Método de cobro actualizado.")
        return redirect(url_for("admin_view"))
    return render_con_matriz("admin.html", config={"autos": admin.cantidad_espacios_autos, "motos": admin.cantidad_espacios_motos, "tarifa_auto": admin.tarifas.get("auto", 0), "tarifa_moto": admin.tarifas.get("moto", 0), "cobro_fraccionado": admin.cobro_fraccionado})

@app.route("/buscar", methods=["GET"])
def buscar():
    placa = normalizar_placa(request.args.get("placa", ""))
    if not placa:
        return redirect(url_for("ingresar"))
    return redirect(url_for("ingresar", placa=placa))

@app.context_processor
def utilidades():
    return {"url_menu": url_for("index")}

if __name__ == "__main__":
    app.run(debug=True)
