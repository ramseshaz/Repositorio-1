print("Recuerde que debe ingresar en ia el siguiente pront para la foto de la lista:")
print("convierte la foto a un archivo.txt, donde cada persona con sus datos se encuentre en una linea y cada dato separado por una coma sin espacio")
print("De lo contrario no funcionara bien la conversión")
    

#codigo para seleccionar archivo
from tkinter import filedialog
print("iniciando el programa...")
print("Selecciones el archivo deseado...")

ruta_del_archivo = filedialog.askopenfilename(
    title="Elige tu archivo de texto",
    filetypes=[("Archivos de texto", "*.txt")]
)

if ruta_del_archivo:
    lista1 = []
   
    with open(ruta_del_archivo, "r", encoding="utf-8") as archivo:
        lista_tomada = archivo.readlines()
#hasta aqui


#comenzamos a trabajar con la lista
#abajo analiza y guarda cada caracte de una linea de texto
    for analizador in lista_tomada:
        #abajo limpia todos los espacios, solo tomando los caracteres
        limpio = analizador.strip() 
        #si no encuentra nada en una linea la ignora
        if limpio:
            #al detectar una coma la corta para la lista de listas o crear la matriz
            sublista = limpio.split(",") 
            
            
            lista1.append(sublista)


    print("Lista:\n")
    print(lista1)