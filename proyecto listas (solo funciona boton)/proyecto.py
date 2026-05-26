from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/procesar-archivo', methods=['POST'])
def procesar_archivo():
    # Recibimos el archivo enviado desde el frontend
    archivo = request.files['archivo']
    
    if archivo:
        # Leemos el contenido sin usar tkinter
        contenido = archivo.read().decode('utf-8')
        lineas = contenido.splitlines()
        
        # Aquí procesas tus 'lineas' como quieras
        return jsonify(mensaje="Archivo procesado", lineas_detectadas=len(lineas))
    
    return jsonify(error="No se recibió archivo"), 400

if __name__ == '__main__':
    app.run(debug=True)




#comenzamos a trabajar con la lista
#abajo analiza y guarda cada caracter de una linea de texto
for analizador in lista_tomada:
    #abajo limpia todos los espacios, solo tomando los caracteres
    limpio = analizador.strip() 
    #si no encuentra nada en una linea la ignora
    if limpio:
        #al detectar una coma la corta para la lista de listas o crear la matriz
        sublista = limpio.split(",")             
lista1.append(sublista)



matriz = lista1
# Algoritmo de ordenamiento manual (Bubble Sort)
n = len(matriz)
for i in range(n):
    for j in range(0, n - i - 1):
        # Comparamos el segundo elemento de cada sublista (índice 1)
        if matriz[j][1] > matriz[j + 1][1]:
            # Intercambiamos las sublistas completas si el orden no es correcto
            auxiliar = matriz[j]
            matriz[j] = matriz[j + 1]
            matriz[j + 1] = auxiliar



#.............................................................................................................
# Mapeo de opciones a índices de la matriz
opciones_columnas = {
    "nombre": 0,
    "apellido": 1,
    "cedula": 2
}
def actualizar_dato(nombre_buscado, campo_a_cambiar, nuevo_valor):
    # 1. Buscamos a la persona
    for persona in matriz:
        if persona[0] == nombre_buscado:
            # 2. Obtenemos el índice correcto según la elección del usuario
            indice = opciones_columnas.get(campo_a_cambiar.lower())
            
            if indice is not None:
                persona[indice] = nuevo_valor
                return f"Se cambió {campo_a_cambiar} de {nombre_buscado}."
    
    return "Persona no encontrada."
#....................................................................................







