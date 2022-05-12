from xmlrpc.client import ServerProxy
import sys

if __name__ == '__main__':
    servidor = ServerProxy("http://localhost:8891")

    modo = input("Ingrese el modo de Operacion: 0-Manual / 1-Automatico: \n")
    servidor.setModoOperacion(modo)
    listaAngulos = []

    for i in range(3):
        entradaAngulo = int(input("Ingrese el angulo de la Articulacion:\n"))
        listaAngulos.append(entradaAngulo)

    entradaPinza = int(input("Ingrese el angulo de la pinza: \n"))
    listaAngulos.append(entradaPinza)
    servidor.setAngulos(listaAngulos[0],listaAngulos[1],listaAngulos[2],listaAngulos[3])

    velocidad = int(input("Ingrese la velocidad de giro de las articulaicones: \n"))
    servidor.setVelocidad(velocidad)

    accionPinza = int(input("Ingrese: 0-> Cerrar Pinza / 1-> Abrir pinza \n"))
    servidor.mover(accionPinza)

    servidor.generarReporte()
