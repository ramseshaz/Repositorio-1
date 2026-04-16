while True:
    try:
        A = float(input("Ingrese un valor primer valor: "))
        break
    except ValueError:
        print("Solo se permiten numeros, intenta otra vez")


#bucle 1
while True:
    print("Hasta ahora el total es:", A)
    #bucle 2
    while True:
        R = input("Seleccione que operación desea realizar (1)Suma, (2)Resta, (3)Multiplicación, (4)División, (s)Salir: ")
        if R.lower() in ['1', '2', '3', '4', 's']:
            break      
        else:
            print("Intente otra vez con uno de los valores indicados")
    #bucle 2 

    if R.lower() == 's':
        print("el resultado final es: ",A)
        break


    #bucle 3
    while True:
        try:
            B = float(input("Ingrese el siguiente valor "))
            break
        except ValueError:
            print("Solo se permiten numeros, intenta otra vez")
    #bucle 3


    if R == '1':
        A = A + B
    elif R == '2':
        A = A - B
    elif R == '3':
        A = A * B
    elif R == '4':
        if B != 0:
            A = A / B
        else:
            print("ERROR: No se puede dividir entre 0.")
#bucle 1
