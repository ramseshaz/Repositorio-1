lista_edades=[ ]

print("Ingrese las edades, escriba (calcular) para iniciar):")
while True:
    llevador = input()
    if llevador == "calcular":
        break    
    lista_edades.append(int(llevador))

contador = 0
Vmax = 0 
Vmin = 0

for edad in lista_edades:
    contador = contador + 1 
    if contador == 1:
        Vmax = edad
        Vmin = edad
    else:       
        if edad > Vmax:
            Vmax = edad
        if edad < Vmin:
            Vmin = edad


print("La edad más alta es:", Vmax)
print("La edad más baja es:", Vmin)