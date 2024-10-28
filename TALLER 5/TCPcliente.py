from socket import *

servidorNombre = "127.0.0.1"
servidorPuerto = 12000
clienteSocket = socket(AF_INET, SOCK_STREAM)
clienteSocket.connect((servidorNombre,servidorPuerto))
mensaje = input("Ingrese un mensaje:")
clienteSocket.send(bytes(mensaje, "utf-8"))
mensajeRespuesta = clienteSocket.recv(1024)
print("Respuesta:\n" + str(mensajeRespuesta, "utf-8"))
clienteSocket.close()