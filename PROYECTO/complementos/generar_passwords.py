import bcrypt

password = input("Ingrese la contraseña: ")

password_hash = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
)

print("\nHash generado:\n")
print(password_hash.decode("utf-8"))