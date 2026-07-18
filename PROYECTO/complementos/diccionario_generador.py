import os
import json

def txt_a_json():
    print("--- Conversor de TXT a JSON ---")
    # 1. Le pedimos al usuario el nombre del archivo
    archivo_entrada = input("Ingresa el nombre del archivo .txt (ejemplo: 'alumnos.txt' o solo 'alumnos'): ")
    
    # 2. Nos aseguramos de que tenga la extensión .txt para evitar errores
    if not archivo_entrada.endswith('.txt'):
        archivo_entrada += '.txt'
        
    # 3. Generamos automáticamente el nombre del archivo .json
    archivo_salida = archivo_entrada.replace('.txt', '.json')

    usuarios = {}
    
    # Calculamos la ruta exacta
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_txt = os.path.join(directorio_actual, archivo_entrada)
    ruta_json = os.path.join(directorio_actual, archivo_salida)
    
    try:
        # 4. Leemos el archivo de texto ingresado
        with open(ruta_txt, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, 1):
                datos = linea.strip().split(",")
                
                # Sigue esperando 3 datos: cédula, nombre, contraseña
                if len(datos) != 3:
                    continue
                
                cedula = datos[0]
                nombre = datos[1]
                password = datos[2]
                
                usuarios[cedula] = {
                    "nombre": nombre,
                    "password": password
                }
        
        # 5. Ordenamos por cédula y creamos el JSON
        if usuarios:
            usuarios_ordenados = {k: usuarios[k] for k in sorted(usuarios.keys(), key=lambda x: int(x))}
            
            with open(ruta_json, "w", encoding="utf-8") as archivo_json:
                json.dump(usuarios_ordenados, archivo_json, indent=4, ensure_ascii=False)
                
            print(f"\n¡Éxito! Se ha creado el archivo '{archivo_salida}' con {len(usuarios_ordenados)} registros.")
        else:
            print("\nEl archivo estaba vacío o ninguna línea tenía el formato correcto (cédula, nombre, contraseña).")
            
    except FileNotFoundError:
        print(f"\nError: No se encontró el archivo '{archivo_entrada}' en la carpeta.")
        print(f"Ruta buscada: {ruta_txt}")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")

# Ejecutamos el programa
txt_a_json()