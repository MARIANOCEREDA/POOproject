import time

class Articulacion(object):

    def girar(self):
        if (self.sentidoGiro == "der"):
            self.anguloTotal = self.anguloTotal + self.anguloRotacion
            time.sleep(0.5)
        elif (self.sentidoGiro == "izq"):
            self.anguloTotal = self.anguloTotal - self.anguloRotacion
            time.sleep(0.5)

    def __init__(self):
        self.anguloRotacion = 0
        self.sentidoGiro = "der"
        self.anguloTotal = 0
        self.velocidad = 0
        ##Tiempo de operacion de cada articulacion
        self.tiempoON = []
        ##Tiempo de inicio de movimiento en cada articulacion.
        self.tiempoDeInicio = []
        pass
