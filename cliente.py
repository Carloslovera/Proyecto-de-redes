# cliente.py
import requests

URL_BASE = "http://127.0.0.1:5000"

def menu():
    while True:
        print("\n--- CLIENTE DE CONSOLA ---")
        print("1. Registrarse")
        print("2. Iniciar Sesión")
        print("3. Ver Página de Tareas (HTML)")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar()
        elif opcion == '2':
            login()
        elif opcion == '3':
            ver_tareas()
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

def registrar():
    print("\n-- Registro --")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    
    response = requests.post(f"{URL_BASE}/registro", json={
        "usuario": usuario,
        "contraseña": contraseña
    })
    print("Respuesta del servidor:", response.json())

def login():
    print("\n-- Login --")
    usuario = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")
    
    response = requests.post(f"{URL_BASE}/login", json={
        "usuario": usuario,
        "contraseña": contraseña
    })
    print("Respuesta del servidor:", response.json())

def ver_tareas():
    print("\n-- Consultando Tareas --")
    response = requests.get(f"{URL_BASE}/tareas")
    print("Código de estado:", response.status_code)
    print("Contenido HTML recibido:\n", response.text)

if __name__ == '__main__':
    menu()