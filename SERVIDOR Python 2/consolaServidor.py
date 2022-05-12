from cmd import Cmd
import sys
from XMLRPCserver import ServerXMLRPC
from ModoAutonomo import ModoAutonomo
import time

class consolaServidor(Cmd):

    def __init__(self,objetoRobot,objetoReporte):
        Cmd.__init__(self)
        self.objetoRobot = objetoRobot
        self.objetoReporte = objetoReporte
        self.rpc_server = None
        self.ListaArgs=[]

    def do_exit(self,value):
        """"Argumento: true -> Desconecta de un dispositivo interno y sale del programa."""
        if value == "true":
            raise sys.exit()

    def do_rpc(self, value):
        """"Inicia/Detiene el servidor según el valor dado (true-> conecta el servidor \n false-> desconecta el servidor)."""
        if value == "true":
            if self.rpc_server is None:
                self.rpc_server = ServerXMLRPC(self.objetoRobot,self.objetoReporte)  #este objeto inicia el servidor y se da a conocer
                self.ListaArgs.append(self.ListaArg("Servidor Iniciado"))
        elif value == "false":
            if self.rpc_server is not None:
                self.rpc_server.shutdown()
                self.rpc_server = None
                self.ListaArgs.append(self.ListaArg("Servidor Apagado"))

            ###############################################################
            #####################OPERACIONES REGISTRADAS###################
            ###############################################################

    def do_setModo(self,modoOperacion):
        """Argumentos: 0->Modo Manual / 1-> Modo Autonomo"""
        if modoOperacion == "0":
            self.objetoRobot.modoOperacion = 0
            self.ListaArgs.append(self.ListaArg("Modo Operacion Manual"))
            print("Modo manual seteado")
            self.objetoRobot.setModoOperacion(int(modoOperacion))
        elif modoOperacion == "1":
            self.objetoRobot.setModoOperacion(int(modoOperacion))
            self.ListaArgs.append(self.ListaArg("Modo Operacion Autónomo"))
            print("Modo autónomo seteado")
            modoAutonomo = ModoAutonomo(self.objetoRobot,self.ListaArgs)
            modoAutonomo.leerFichero()
            modoAutonomo.interpretarLineas()

    def do_setAngulos(self,value):
        """Argumento: true - Setea los angulos de las 3 articulaciones y la pinza"""
        a = []
        s = []
        for i in range(3):
            entrada1 = int(input("Angulo articulacion "+str(i)+" : \n"))
            a.append(entrada1)
            self.ListaArgs.append(self.ListaArg("Set Angulo Articulacion "+str(i)))
            entrada2 = input("Sentido articulacion (der->derecha / izq->izquierda) "+str(i)+" : \n")
            s.append(entrada2)
            self.ListaArgs.append(self.ListaArg("Set Giro Articulacion "+str(i)))
        self.objetoRobot.setAngulos(a[0],a[1],a[2])
        self.objetoRobot.setSentidoGiro(s[0],s[1],s[2])

    def do_encenderRobot(self,estado):
        """Argumentos: 0->Apagar / 1->Encender"""
        if estado == "0":
            self.objetoRobot.setEstado(int(estado))
            self.ListaArgs.append(self.ListaArg("Robot Apagado"))
        elif estado == "1" :
            self.objetoRobot.setEstado(int(estado))
            self.ListaArgs.append(self.ListaArg("Robot Encendido"))

    def do_setVelocidad(self,velocidad):
        """Argumento: velocidad en rad/s"""
        self.objetoRobot.setVelocidad(int(velocidad))
        self.ListaArgs.append(self.ListaArg("Set Velocidad"))

    def do_mover(self,accionPinza):
        """Argumento: 0-> cerrar pinza / 1-> abrir pinza - mueve el robot a la posicion prefijada"""
        if self.objetoRobot.estado == 1:
            self.objetoRobot.MoverArticulacion()
            self.objetoRobot.MoverPinza(int(accionPinza))
            self.ListaArgs.append(self.ListaArg("Movimiento Realizado"))
        elif self.objetoRobot.estado == 0:
            print("El robot se encuentra apagado, para moverlo debe encenderlo")

    def do_moverOrigen(self,value):
        """Argumento: true - mueve el robot a la posicion de origen"""
        self.objetoRobot.MoverOrigen()
        self.ListaArgs.append(self.ListaArg("Homing"))

    def do_mostrarReporte(self,value):
        """Muestra el reporte general del robot: Angulos - Velocidad - Tiempos de Operación"""
        self.ListaArgs.append(self.ListaArg("Reporte Pedido"))
        sumlista="".join(self.ListaArgs)
        sumlista2=""
        if self.rpc_server is not None:
            sumlista2="".join(self.rpc_server.ListaArgs)
        return print(self.objetoReporte.mostrarDatos(self.objetoRobot,self.rpc_server)
        +"\n\n>>>>>> Lista de Ordenes Recibidas <<<<<<\n"+sumlista+"\n\n>>>>>>      CLIENTE     <<<<<<\n"+sumlista2)

    def do_estado(self,value):
        """Devuelve el estado de conexion del servidor"""
        if self.rpc_server == None:
            print("Estado servidor : Desconectado")
        else:
            print("Estado servidor : Conectado")

    def ListaArg(self,ordertype):
        return ("["+time.strftime("%a, %d %b %Y %H:%M:%S") +"]:      "+ordertype+"\n")
