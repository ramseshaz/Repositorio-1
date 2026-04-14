

print("Bienvenido a la calculadora")
A = float(input("introduzca el primer valor: "))
B = float(input("introduzca el primer valor: "))

print("Puede realizar las siguientes operaciones: ")
print("1. Suma ")
print("2. Resta ")
print("3. Multiplicación ")
print("4. División ")
R = input("¿Que operación desea realizar? ")

if R == "1":
    resultado = {A + B} 
    print("el resultado es:", resultado)

elif R == "2":
    resultado = {A - B} 
    print("el resultado es:", resultado)

elif R == "3":
    resultado = {A * B} 
    print("el resultado es:", resultado)

elif R == "4":
    if B != 0:
        resultado = {A / B} 
        print("el resultado es:", resultado)
    else:
        print("no valido")
else:
    print("Opción no valida")
