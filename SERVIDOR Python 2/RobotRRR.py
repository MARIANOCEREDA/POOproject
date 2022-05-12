from Articulacion import Articulacion
from Pinza import Pinza
import time

class RobotRRR():
    def __init__(self):
        ##Tiempo total (suma de cada una de cada operacion)
        self.tiempoTotal = 0
        ##Lista comandos: rellena con los ángulos recibidos desde el cliente
        self.listaAngulos = [0,0,0]
        self.listaSentidosGiro = ["der","der","der"]
        ##Modo de operacion: 0-> manual / 1-> automatico
        self.modoOperacion = 0
        ##Velocidad de operacion:
        self.velocidad = 0
        ##Estado: 0->apagado / 1->encendido
        self.estado = 0
        ##Array de arrayArticulaciones
        self.arrayArticulaciones=[]
        for i in range(3):
            self.arrayArticulaciones.append(Articulacion())
        self.numeroVinculo = None
        self.eslabon = None
        self.pinza = Pinza()
        self.tiempoDuracion = None

    def setEstado(self,estado):
        self.estado = estado

    def setModoOperacion(self,modoOperacion):
        self.modoOperacion = modoOperacion

    def setAngulos(self,a1,a2,a3):
        self.listaAngulos = [a1,a2,a3]
        for i in range(3):
            self.arrayArticulaciones[i].anguloRotacion = self.listaAngulos[i]

    def setSentidoGiro(self,s1,s2,s3):
        self.listaSentidosGiro = [s1,s2,s3]
        for i in range(3):
            self.arrayArticulaciones[i].sentidoGiro = self.listaSentidosGiro[i]

    def setVelocidad(self,velocidad):
        self.velocidad = velocidad
        for i in range(3):
            self.arrayArticulaciones[i].velocidad = velocidad

    def MoverPinza(self,accionPinza):
        self.pinza.estadoPinza =  accionPinza
        if accionPinza == 1:
            self.pinza.abrir()
        if accionPinza == 0:
            self.pinza.cerrar()

    def MoverArticulacion(self):
        for i in range(3):
            self.arrayArticulaciones[i].tiempoDeInicio.append(time.strftime("%a, %d %b %Y %H:%M:%S"))
            tiempoInicio = time.time()
            self.arrayArticulaciones[i].girar()
            tiempoFinal = time.time()
            self.arrayArticulaciones[i].tiempoON.append(tiempoFinal-tiempoInicio)

    def MoverOrigen(self):
        anguloTotal = []
        for i in range(3):
            anguloTotal.append(self.arrayArticulaciones[i].anguloTotal)
            if anguloTotal[i] < 0:
                self.arrayArticulaciones[i].sentidoGiro = "der"
            elif anguloTotal[i] > 0:
                self.arrayArticulaciones[i].sentidoGiro = "izq"
            tiempoInicio = time.time()
            self.arrayArticulaciones[i].girar()
            tiempoFinal = time.time()
            self.arrayArticulaciones[i].tiempoON.append(tiempoFinal-tiempoInicio)
