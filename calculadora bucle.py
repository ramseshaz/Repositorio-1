A = float(input("Ingrese el primer valor "))

while True:
    print("\nel total es:", A)
    R = input("Seleccione que operación desea realizar (1)Suma, (2)Resta, (3)Multiplicación, (4)División, (s)Salir: ")

#bucle de validación    
    while True:
        R = input("Seleccione que operación desea realizar (1)Suma, (2)Resta, (3)Multiplicación, (4)División, (s)Salir: ")
        
        if R.lower() in ['1', '2', '3', '4', 's']:
            break  
        else:
            print("Opción no válida. Por favor, elige del 1 al 4 o 's'.")
#############################################################################################################################################   
    
    if R.lower() == 's':
        break 

    
    
    
    B = float(input("Ingrese el siguiente valor "))

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
            print("ERROR: no se puede dividir entre 0 ")
    else: 
        print("Error, intentelo nuevamente") 
print("\nOperacion realizada" , A)       



    