from flask import Flask, request, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io

app = Flask(__name__)

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
# FUNCIÓN DE ORDENAMIENTO
# =========================
def transformar_y_ordenar(lista_tomada):
    lista_procesada = []

    for linea in lista_tomada:
        limpio = linea.strip()

        if limpio:
            partes = limpio.split(",")

            if len(partes) >= 3:
                lista_procesada.append(partes)

    # Bubble Sort por apellido
    n = len(lista_procesada)

    for i in range(n):
        for j in range(0, n - i - 1):

            if lista_procesada[j][1] > lista_procesada[j + 1][1]:
                lista_procesada[j], lista_procesada[j + 1] = lista_procesada[j + 1], lista_procesada[j]

    return lista_procesada

# =========================
# RUTA PROCESAR
# =========================
@app.route('/procesar', methods=['POST'])
def procesar():

    archivo = request.files.get('archivo')

    if not archivo:
        return jsonify(error="No se recibió archivo"), 400

    contenido = archivo.read().decode('utf-8')
    lineas = contenido.splitlines()

    resultado = transformar_y_ordenar(lineas)

    return jsonify(datos=resultado)

# =========================
# RUTA PDF
# =========================
@app.route('/descargar_pdf', methods=['POST'])
def descargar_pdf():

    archivo = request.files.get('archivo')

    if not archivo:
        return jsonify(error="No se recibió archivo"), 400

    contenido = archivo.read().decode('utf-8')
    lineas = contenido.splitlines()

    datos = transformar_y_ordenar(lineas)

    # Crear PDF en memoria
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    # =========================
    # ENCABEZADO CON LOGO
    # =========================

    # Logo UNEFA
    pdf.drawImage(
        "images.png",
        40,                 # posición X
        height - 130,       # posición Y
        width=90,
        height=90,
        mask='auto'
    )

    # Título principal
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(160, height - 60, "UNIVERSIDAD NACIONAL")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(160, height - 85, "EXPERIMENTAL POLITÉCNICA")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(160, height - 110, "DE LA FUERZA ARMADA")

    # Línea decorativa
    pdf.line(40, height - 140, 550, height - 140)

    # Nombre del documento
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(200, height - 170, "LISTA DE ASISTENCIA")

    # =========================
    # TABLA
    # =========================
    tabla_datos = [["Nombre", "Apellido", "Cédula"]]

    for persona in datos:
        tabla_datos.append([
            persona[0],
            persona[1],
            persona[2]
        ])

    tabla = Table(tabla_datos, colWidths=[150, 150, 150])

    estilo = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    tabla.setStyle(estilo)

    tabla.wrapOn(pdf, width, height)
    tabla.drawOn(pdf, 50, height - 500)

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="lista_asistencia.pdf",
        mimetype='application/pdf'
    )

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
















