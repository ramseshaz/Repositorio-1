# Lista de edades =
edades = [20, 23, 23, 21, 20, 21, 22, 19, 19, 20, 21, 23, 20, 21, 20, 23]

print("LISTA COMPLETA CON POSICIONES")
print("=" * 30) 

# Mostrar lista con posiciones usando for
print( "Usando for:")
for i in range(len(edades)):
    print(f"  [{i}] = {edades[i]}")
 
print("\nUsando while:")
i = 0
while i < len(edades):
    print(f"  [{i}] = {edades[i]}")
    i = i + 1

print("\n" + "=" * 30)
print("BUSQUEDA DE EDAD ESPECIFICA")

# Buscar edad especifica
edad_objetivo = 20
print(f"\nBuscando edad: {edad_objetivo}")
print("posiciones encontrada:")

encontradas = 0
i = 0
while i < len(edades):
    if edades[i] == edad_objetivo:
        print(f"  Posicion [{i}]")
        encontradas = encontradas + 1
    i = i + 1

print(f"Total de veces que aparece {edad_objetivo}: {encontradas}")    

































