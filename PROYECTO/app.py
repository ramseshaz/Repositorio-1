from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
import os
import json
import bcrypt

app = Flask(__name__)
app.secret_key = 'clave_secreta_unefa'

# =========================
# FUNCION DICCIONARIOS
# =========================

def leer_json(nombre_archivo):

    if not os.path.exists(nombre_archivo):

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump({}, archivo)

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(nombre_archivo, datos):

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# =========================
# CONFIGURACIÓN CORS
# =========================
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# =========================
# FUNCIÓN DE VALIDACIÓN JSON
# =========================
def validar_credenciales(rol, cedula, password):
    archivos = {
        'alumno': 'alumnos.json',
        'profesor': 'profesores.json',
        'coordinador': 'coordinadores.json'
    }
    
    nombre_archivo = archivos.get(rol)
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(directorio_actual, nombre_archivo)
    
    if not nombre_archivo or not os.path.exists(ruta_completa):
        print(f"ERROR: No se encontró el archivo en {ruta_completa}")
        return False
        
    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        try:
            usuarios = json.load(archivo)
        except json.JSONDecodeError:
            print(f"ERROR: El archivo {nombre_archivo} tiene un formato JSON inválido")
            return False

    cedula_limpia = cedula.strip()
    print(f"Intentando loguear: Rol={rol}, Cedula={cedula_limpia}")

    if cedula_limpia in usuarios:
        hash_guardado = usuarios[cedula_limpia].get('password', '')
        
        try:
            if bcrypt.checkpw(password.encode('utf-8'), hash_guardado.encode('utf-8')):
                print("¡LOGIN EXITOSO!")
                return True
            else:
                print("ERROR: La contraseña es incorrecta.")
        except ValueError:
            print("ERROR: El hash guardado en el JSON no es válido para bcrypt.")
            return False
    else:
        print(f"ERROR: La cédula {cedula_limpia} no existe en {nombre_archivo}")

    return False

# ================================
# RUTA PRINCIPAL (LOGIN Y VISTAS)
# ================================
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None # Variable para enviar mensajes de error al HTML

    if request.method == 'POST':

        tipo_usuario = request.form.get('tipo_usuario')
        cedula = request.form.get('cedula')
        password = request.form.get('password')

        # Asegúrate de verificar también que exista el password
        if tipo_usuario and cedula and password:

            if validar_credenciales(tipo_usuario, cedula, password):
                
                session['rol'] = tipo_usuario
                session['cedula'] = cedula

                if tipo_usuario == 'profesor':
                    return redirect(url_for('profesor'))

                elif tipo_usuario == 'coordinador':
                    return redirect(url_for('coordinador'))

                elif tipo_usuario == 'alumno':
                    return redirect(url_for('alumno'))
            else:
                error = "Datos incorrectos o usuario no registrado."

    return render_template('login.html', error=error)

# =========================
# RUTAS DEL PROFESOR
# =========================
@app.route("/profesor")
def profesor():

    if session.get("rol") != "profesor":
        return redirect(url_for("index"))

    cedula = session["cedula"]

    disponibilidades = leer_json("disponibilidades.json")
    materias = leer_json("materias.json")

    mis_datos = []

    for disponibilidad in disponibilidades.values():

        if disponibilidad["cedula"] == cedula:
            mis_datos.append(disponibilidad)

    return render_template(
        "profesor.html",
        materias=materias,
        mis_datos=mis_datos
    )

@app.route("/profesor/disponibilidad", methods=["POST"])
def guardar_disponibilidad():

    if session.get("rol") != "profesor":
        return redirect(url_for("index"))

    disponibilidades = leer_json("disponibilidades.json")

    for disponibilidad in disponibilidades.values():

        if disponibilidad["cedula"] == session["cedula"] and disponibilidad["dia"] == request.form["dia"]:

            if (
                request.form["hora_inicio"] < disponibilidad["hora_fin"]
                and request.form["hora_fin"] > disponibilidad["hora_inicio"]
            ):
                return "Ese horario se solapa con otro que ya registraste."

    nuevo_id = str(len(disponibilidades) + 1)

    disponibilidades[nuevo_id] = {

        "id": nuevo_id,

        "cedula": session["cedula"],

        "materia": request.form["materia"],

        "dia": request.form["dia"],

        "hora_inicio": request.form["hora_inicio"],

        "hora_fin": request.form["hora_fin"]

    }

    guardar_json("disponibilidades.json", disponibilidades)

    return redirect(url_for("profesor"))


# =========================
# RUTAS DEL COORDINADOR
# =========================
@app.route("/coordinador")
def coordinador():

    if session.get("rol") != "coordinador":
        return redirect(url_for("index"))

    disponibilidades = leer_json("disponibilidades.json")
    horario = leer_json("horario_oficial.json")
    materias = leer_json("materias.json")
    profesores = leer_json("profesores.json")

    return render_template(
        "coordinador.html",
        disponibilidad=disponibilidades,
        horario=horario,
        materias=materias,
        profesores=profesores
    )

@app.route("/coordinador/crear_clase", methods=["POST"])
def crear_clase():

    if session.get("rol") != "coordinador":
        return redirect(url_for("index"))

    horario = leer_json("horario_oficial.json")

    nuevo_id = str(len(horario) + 1)

    horario[nuevo_id] = {

        "id": nuevo_id,

        "materia": request.form["materia"],

        "profesor": request.form["profesor"],

        "dia": request.form["dia"],

        "hora_inicio": request.form["hora_inicio"],

        "hora_fin": request.form["hora_fin"]

    }

    guardar_json("horario_oficial.json", horario)

    return redirect(url_for("coordinador"))

# =========================
# RUTAS DEL ALUMNO
# =========================
@app.route("/alumno")
def alumno():

    if session.get("rol") != "alumno":
        return redirect(url_for("index"))

    horario = leer_json("horario_oficial.json")
    inscripciones = leer_json("inscripciones.json")

    cedula = session["cedula"]

    if cedula not in inscripciones:
        inscripciones[cedula] = {}

    mis_clases_ids = list(inscripciones[cedula].keys())

    mis_clases = []

    for id_clase in mis_clases_ids:

        if id_clase in horario:
            mis_clases.append(horario[id_clase])

    return render_template(

        "alumno.html",

        horario_oficial=horario,

        mis_clases=mis_clases,

        mis_clases_ids=mis_clases_ids

    )

@app.route("/alumno/inscribir/<id_clase>")
def inscribir(id_clase):

    if session.get("rol") != "alumno":
        return redirect(url_for("index"))

    horario = leer_json("horario_oficial.json")
    inscripciones = leer_json("inscripciones.json")

    cedula = session["cedula"]

    if cedula not in inscripciones:
        inscripciones[cedula] = {}

    if id_clase in inscripciones[cedula]:
        return redirect(url_for("alumno"))

    inscripciones[cedula][id_clase] = True

    guardar_json("inscripciones.json", inscripciones)

    return redirect(url_for("alumno"))

@app.route("/alumno/retirar/<id_clase>")
def retirar(id_clase):

    inscripciones = leer_json("inscripciones.json")

    cedula = session["cedula"]

    if (
        cedula in inscripciones
        and id_clase in inscripciones[cedula]
    ):
        del inscripciones[cedula][id_clase]

    guardar_json("inscripciones.json", inscripciones)

    return redirect(url_for("alumno"))

# =========================
# EXPORTAR PDF (HORARIO)
# =========================

@app.route("/alumno/exportar_pdf")
def exportar_pdf():
    # 1. Validación de sesión y carga de datos
    if session.get("rol") != "alumno":
        return redirect(url_for("index"))

    cedula = session["cedula"]
    
    # Cargar todos los JSON necesarios
    horario = leer_json("horario_oficial.json")
    inscripciones = leer_json("inscripciones.json")
    alumnos = leer_json("alumnos.json")
    profesores = leer_json("profesores.json")
    materias = leer_json("materias.json")
    
    mis_clases_ids = list(inscripciones.get(cedula, {}).keys())
    mis_clases = [horario[id_clase] for id_clase in mis_clases_ids if id_clase in horario]

    # Extraer el nombre del estudiante de alumnos.json
    info_alumno = alumnos.get(cedula, {})
    nombre_estudiante = info_alumno.get("nombre", "Estudiante Desconocido")

    # --- FUNCIÓN AUXILIAR ---
    def time_to_mins(t_str):
        h, m = map(int, t_str.strip().split(':'))
        return h * 60 + m

    # 2. Crear buffer de memoria para el PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- AGREGAR LOGO DE LA UNIVERSIDAD ---
    # Buscamos la carpeta template en el directorio actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_logo = os.path.join(directorio_actual, "template", "images.png")
    
    if os.path.exists(ruta_logo):
        # Dibuja la imagen en la esquina superior derecha
        c.drawImage(ruta_logo, width - 110, height - 90, width=70, height=70, preserveAspectRatio=True, mask='auto')

    # --- ENCABEZADO ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "UNEFA")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 55, "COMPROBANTE DE INSCRIPCIÓN")
    c.drawString(40, height - 70, "NÚCLEO CARACAS | 1-2026")

    # --- DATOS DEL ESTUDIANTE ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, height - 100, f"CÉDULA (V): {cedula}")
    # Convertimos a mayúsculas para mantener el estilo
    c.drawString(40, height - 115, f"ESTUDIANTE: {nombre_estudiante.upper()}")
    c.drawString(40, height - 130, "PROGRAMA: INGENIERÍA DE SISTEMAS DIURNO")

    # --- TABLA 1: LISTA DE ASIGNATURAS INSCRITAS ---
    datos_asignaturas = [["N°", "ASIGNATURAS", "DOCENTE"]]
    for i, clase in enumerate(mis_clases, start=1):
        
        # Mapeo del Profesor (Cédula - Nombre)
        id_prof = clase.get('profesor', '')
        if id_prof in profesores:
            nombre_prof = profesores[id_prof].get('nombre', '')
            texto_prof = f"{id_prof} - {nombre_prof}"
        else:
            texto_prof = id_prof # Respaldo si ya estaba guardado con el nombre

        # Mapeo de la Materia (Código - Nombre)
        id_mat = clase.get('materia', '')
        info_mat = materias.get(id_mat, id_mat)
        
        # Validación flexible por si materias.json guarda un dict o un string directamente
        if isinstance(info_mat, dict):
            nombre_mat = info_mat.get('nombre', id_mat)
        else:
            nombre_mat = info_mat
            
        texto_mat = f"{id_mat} - {nombre_mat}" if id_mat in materias else id_mat

        datos_asignaturas.append([str(i), texto_mat, texto_prof])
        
    tabla_asignaturas = Table(datos_asignaturas, colWidths=[30, 250, 240])
    tabla_asignaturas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    
    ancho_t1, alto_t1 = tabla_asignaturas.wrap(width, height)
    y_pos_t1 = height - 150 - alto_t1
    tabla_asignaturas.drawOn(c, 40, y_pos_t1)

    # --- TABLA 2: MATRIZ DE HORARIO (CUADRÍCULA 45 MINUTOS) ---
    datos_matriz = [["ENT/SAL", "LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]]
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_abreviados = ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"]
    
    hora_actual = 7 * 60 
    hora_fin_limite = 20 * 60 + 30 
    bloques_horas = []

    while hora_actual < hora_fin_limite:
        h_inicio = f"{hora_actual // 60:02d}:{hora_actual % 60:02d}"
        hora_siguiente = hora_actual + 45
        h_fin = f"{hora_siguiente // 60:02d}:{hora_siguiente % 60:02d}"
        bloques_horas.append((h_inicio, h_fin, hora_actual, hora_siguiente))
        hora_actual = hora_siguiente

    for h_inicio, h_fin, min_inicio, min_fin in bloques_horas:
        fila = [f"{h_inicio}-{h_fin}"]
        for dia_idx, dia_abrev in enumerate(dias_abreviados):
            materia_celda = ""
            for clase in mis_clases:
                dia_clase = clase.get('dia', '').upper()[:3]
                if dia_clase == dia_abrev or clase.get('dia') == dias_semana[dia_idx]:
                    clase_inicio = time_to_mins(clase['hora_inicio'])
                    clase_fin = time_to_mins(clase['hora_fin'])
                    
                    if clase_inicio <= min_inicio and min_fin <= clase_fin:
                        # Extraemos el texto mapeado al igual que arriba para mostrar Código - Nombre
                        id_mat_grid = clase.get('materia', '')
                        info_mat_grid = materias.get(id_mat_grid, id_mat_grid)
                        if isinstance(info_mat_grid, dict):
                            nombre_mat_grid = info_mat_grid.get('nombre', id_mat_grid)
                        else:
                            nombre_mat_grid = info_mat_grid
                        materia_celda = f"{id_mat_grid} - {nombre_mat_grid}" if id_mat_grid in materias else id_mat_grid
                        break 
            fila.append(materia_celda)
        datos_matriz.append(fila)

    tabla_matriz = Table(datos_matriz, colWidths=[60, 66, 66, 66, 66, 66, 66, 66])
    tabla_matriz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 5), # Letra ajustada a 5 para que Código y Materia entren en la celda
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    
    ancho_t2, alto_t2 = tabla_matriz.wrap(width, height)
    y_pos_t2 = y_pos_t1 - 15 - alto_t2
    tabla_matriz.drawOn(c, 40, y_pos_t2)

    # --- TEXTO LEGAL Y PIE DE PÁGINA ---
    c.setFont("Helvetica", 6)
    texto_legal = "La UNEFA, conforme con lo establecido en el artículo 46 del Decreto con rango, valor y fuerza de Ley de Simplificación de trámites Administrativos, hace constar que el ciudadano mencionado es estudiante activo."
    texto_legal2 = "Para la autenticación del presente documento consultar al correo verificacioninscripcion@unefa.edu.ve"
    
    c.drawString(40, 50, texto_legal)
    c.drawString(40, 40, texto_legal2)

    c.save()
    
    # 3. Retornar el PDF
    buffer.seek(0)
    return send_file(
        buffer, 
        as_attachment=True, 
        download_name=f"Comprobante_Inscripcion_{cedula}.pdf", 
        mimetype='application/pdf'
    )

# =========================
# CERRAR SESIÓN
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
