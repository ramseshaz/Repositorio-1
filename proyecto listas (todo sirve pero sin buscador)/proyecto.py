from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración manual de CORS para evitar librerías externas
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

# Función de lógica (Transformar y Ordenar)
def transformar_y_ordenar(lista_tomada):
    lista_procesada = []
    for linea in lista_tomada:
        limpio = linea.strip()
        if limpio:
            partes = limpio.split(",")
            if len(partes) >= 2:
                lista_procesada.append(partes)
    
    # Bubble Sort manual por el índice 1 (apellido)
    n = len(lista_procesada)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_procesada[j][1] > lista_procesada[j + 1][1]:
                lista_procesada[j], lista_procesada[j + 1] = lista_procesada[j + 1], lista_procesada[j]
    return lista_procesada

@app.route('/procesar', methods=['POST', 'OPTIONS'])
def procesar():
    if request.method == 'OPTIONS':
        return '', 200
        
    archivo = request.files.get('archivo')
    if not archivo:
        return jsonify(error="No se recibió archivo"), 400
    
    contenido = archivo.read().decode('utf-8')
    lineas = contenido.splitlines()
    
    resultado = transformar_y_ordenar(lineas)
    return jsonify(datos=resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)




















#funcion de editar cosas (ignorar por ahora)

def actualizar_dato(matriz, nombre_buscado, campo_a_cambiar, nuevo_valor):
    opciones_columnas = {
        "nombre": 0,
        "apellido": 1,
        "cedula": 2
    }
    
    for persona in matriz:
        if persona[0] == nombre_buscado:
            indice = opciones_columnas.get(campo_a_cambiar.lower())
            if indice is not None:
                persona[indice] = nuevo_valor
                return f"Se cambió {campo_a_cambiar} de {nombre_buscado}."
    
    return "Persona no encontrada."
















