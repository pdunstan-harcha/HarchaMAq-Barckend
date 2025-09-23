import sys
from werkzeug.security import generate_password_hash  


def hash_password(password):
    """Hashes a password using a secure method."""
    # Use pbkdf2:sha256 which is a good default. Salt length of 8 is standard.
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python hash_password.py <tu_contraseña>")
        sys.exit(1)

    password_to_hash = sys.argv[1]
    hashed_password = hash_password(password_to_hash)

    print(f"Contraseña original: {password_to_hash}")
    print(f"Contraseña hasheada: {hashed_password}")
    print("\nCopia y pega la contraseña hasheada en la columna 'CLAVE' de la tabla 'USUARIOS' en la base de datos.")
