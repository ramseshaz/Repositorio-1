from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
import os
import json

app = Flask(__name__)
app.secret_key = 'clave_secreta_unefa'

# =========================
# CONFIGURACIÓN CORS
# =========================
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# Base de datos en memoria para el horario
horario_db = []

# =========================
# BASES DE DATOS SIMULADAS
# =========================
disponibilidad_profesores = []
horario_oficial = []
inscripciones_alumnos = [] # Guarda diccionarios {'cedula': '...', 'id_clase': 1}

# ================================
# RUTA PRINCIPAL (LOGIN Y VISTAS)
# ================================
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        tipo_usuario = request.form.get('tipo_usuario')
        cedula = request.form.get('cedula')
        password = request.form.get('password')

        if tipo_usuario and cedula and password:

            session['rol'] = tipo_usuario
            session['cedula'] = cedula

            if tipo_usuario == 'profesor':
                return redirect(url_for('profesor'))

            elif tipo_usuario == 'coordinador':
                return redirect(url_for('coordinador'))

            elif tipo_usuario == 'alumno':
                return redirect(url_for('alumno'))

    return render_template('login.html')

# =========================
# RUTAS DEL PROFESOR
# =========================
@app.route('/profesor')
def profesor():
    if session.get('rol') != 'profesor':
        return redirect(url_for('index'))

    cedula_actual = session.get('cedula')
    mi_disponibilidad = [
        d for d in disponibilidad_profesores
        if d['cedula'] == cedula_actual
    ]

    return render_template(
        'profesor.html',
        mis_datos=mi_disponibilidad
    )

# =========================
# RUTAS DEL COORDINADOR
# =========================
@app.route('/coordinador')
def coordinador():
    if session.get('rol') != 'coordinador':
        return redirect(url_for('index'))

    return render_template(
        'coordinador.html',
        disponibilidad=disponibilidad_profesores,
        horario=horario_oficial
    )

# =========================
# RUTAS DEL ALUMNO
# =========================
@app.route('/alumno')
def alumno():
    if session.get('rol') != 'alumno':
        return redirect(url_for('index'))

    cedula_actual = session.get('cedula')

    mis_clases_ids = [
        insc['id_clase']
        for insc in inscripciones_alumnos
        if insc['cedula'] == cedula_actual
    ]

    mis_clases = [
        clase for clase in horario_oficial
        if clase['id'] in mis_clases_ids
    ]

    return render_template(
        'alumno.html',
        horario_oficial=horario_oficial,
        mis_clases=mis_clases,
        mis_clases_ids=mis_clases_ids
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
