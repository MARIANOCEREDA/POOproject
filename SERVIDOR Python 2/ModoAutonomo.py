from RobotRRR import RobotRRR
import time

class ModoAutonomo():
    def __init__(self,objetoRobot,ListaArgs):
        self.lineasArchivo = []
        self.objetoRobot = objetoRobot
        self.ListaArgs = ListaArgs

    def leerFichero(self):
        self.fichero = open("modoAutonomo.txt", "r")
        self.lineasArchivo = self.fichero.readlines()
        self.fichero.close()

    def interpretarLineas(self):
        print(self.lineasArchivo[0][0:8])
        if self.lineasArchivo[0][0:8] == "encender":
            self.objetoRobot.estado = 1
            self.ListaArgs.append(self.ListaArg("Robot Encendido [MODO AUTONOMO]"))
        elif self.lineasArchivo[0][0:7] == "apagar":
            self.objetoRobot.estado = 0
            self.ListaArgs.append(self.ListaArg("Robot Apagado [MODO AUTONOMO]"))
        self.objetoRobot.setAngulos(int(self.lineasArchivo[1]),int(self.lineasArchivo[2]),int(self.lineasArchivo[3]))
        self.ListaArgs.append(self.ListaArg("Set Angulos Articulaciones [MODO AUTONOMO] "))
        self.objetoRobot.setVelocidad(self.lineasArchivo[4])
        self.ListaArgs.append(self.ListaArg("Set Velocidad [MODO AUTONOMO]"))
        s1REC = self.lineasArchivo[5]
        s2REC = self.lineasArchivo[6]
        s3REC = self.lineasArchivo[7]
        self.objetoRobot.setSentidoGiro(s1REC[0:3],s2REC[0:3],s3REC[0:3])
        self.ListaArgs.append(self.ListaArg("Set Giro Articulaciones [MODO AUTONOMO]"))
        if self.lineasArchivo[8][0:5] == "abrir":
            self.objetoRobot.MoverPinza(1)
            self.ListaArgs.append(self.ListaArg("Pinza abierta [MODO AUTONOMO]"))
        elif self.lineasArchivo[8][0:6] == "cerrar":
            self.objetoRobot.MoverPinza(0)
            self.ListaArgs.append(self.ListaArg("Pinza cerrada [MODO AUTONOMO]"))
        self.objetoRobot.MoverArticulacion()
        self.ListaArgs.append(self.ListaArg("Movimiento Realizado [MODO AUTONOMO]"))
        if self.lineasArchivo[9][0:11] == "moverOrigen":
            self.objetoRobot.MoverOrigen()
            self.ListaArgs.append(self.ListaArg("Homing [MODO AUTONOMO]"))

    def ListaArg(self,ordertype):
        return ("["+time.strftime("%a, %d %b %Y %H:%M:%S") +"]:      "+ordertype+"\n")
