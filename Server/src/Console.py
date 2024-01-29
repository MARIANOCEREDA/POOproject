from cmd import Cmd
import sys
from XMLRPCserver import ServerXMLRPC
from AutoMode import AutoMode
import time


class Console(Cmd):

    def __init__(self, robot_object, report_object):
        Cmd.__init__(self)
        self.robot_object = robot_object
        self.report_object = report_object
        self.rpc_server = None
        self.ListaArgs = []

    def do_exit(self, value):
        """"Argumento: true -> Desconecta de un dispositivo interno y sale del programa."""
        if value == "true":
            self.rpc_server.shutdown()
            raise sys.exit()

    def do_rpc(self, value):
        """"Inicia/Detiene el servidor según el valor dado (true-> conecta el servidor \n false-> desconecta el servidor)."""
        if value == "true":
            if self.rpc_server is None:
                self.rpc_server = ServerXMLRPC(
                    self.robot_object, self.report_object
                ) 
                #este objeto inicia el servidor y se da a conocer
                self.ListaArgs.append(self.ListaArg("Servidor Iniciado"))

        elif value == "false":
            if self.rpc_server is not None:
                self.rpc_server.shutdown()
                self.rpc_server = None
                self.ListaArgs.append(self.ListaArg("Servidor Apagado"))

            ###############################################################
            #####################OPERACIONES REGISTRADAS###################
            ###############################################################

    def do_setMode(self, operation_mode):
        """Argumentos: 0->Modo Manual / 1-> Modo Autonomo"""
        if operation_mode == "0":
            self.robot_object.operation_mode = 0
            self.ListaArgs.append(self.ListaArg("Modo Operacion Manual"))

            print("Modo manual seteado")

            self.robot_object.setOperationMode(int(operation_mode))

        elif operation_mode == "1":
            self.robot_object.setOperationMode(int(operation_mode))
            self.ListaArgs.append(self.ListaArg("Modo Operacion Autónomo"))
            print("Modo autónomo seteado")
            autoMode = AutoMode(self.robot_object, self.ListaArgs)
            autoMode.readFile()
            autoMode.parseLines()

    def do_setAngles(self, value):
        """Argumento: true - Setea los angulos de las 3 articulaciones y la pinza"""
        a = []
        s = []
        for i in range(3):
            entrada1 = int(input("Angulo articulacion " + str(i) + " : \n"))
            a.append(entrada1)
            self.ListaArgs.append(
                self.ListaArg("Set Angulo Articulacion " + str(i)))
            entrada2 = input(
                "Sentido articulacion (der->derecha / izq->izquierda) " +
                str(i) + " : \n")
            s.append(entrada2)
            self.ListaArgs.append(
                self.ListaArg("Set Giro Articulacion " + str(i)))
        self.robot_object.setAngles(a[0], a[1], a[2])
        self.robot_object.setRotationDirection(s[0], s[1], s[2])

    def do_turnRobotOn(self, status):
        """Argumentos: 0->Apagar / 1->Encender"""
        if status == "0":
            self.robot_object.setStatus(int(status))
            self.ListaArgs.append(self.ListaArg("Robot Apagado"))
            
        elif status == "1":
            self.robot_object.setStatus(int(status))
            self.ListaArgs.append(self.ListaArg("Robot Encendido"))

    def do_setSpeed(self, speed):
        """Argumento: velocidad en rad/s"""
        self.robot_object.setSpeed(int(speed))
        self.ListaArgs.append(self.ListaArg("Set Velocidad"))

    def do_move(self, gripper_action):
        """Argumento: 0-> cerrar pinza / 1-> abrir pinza - mueve el robot a la posicion prefijada"""
        if self.robot_object.status == 1:
            self.robot_object.MoveJoint()
            self.robot_object.MoveGripper(int(gripper_action))
            self.ListaArgs.append(self.ListaArg("Movimiento Realizado"))

        elif self.robot_object.status == 0:
            print(
                "El robot se encuentra apagado, para moverlo debe encenderlo")

    def do_moveOrigin(self, value):
        """Argumento: true - mueve el robot a la posicion de origen"""
        self.robot_object.MoveOrigin()
        self.ListaArgs.append(self.ListaArg("Homing"))

    def do_showReport(self, value):
        """Muestra el reporte general del robot: Angulos - Velocidad - Tiempos de Operación"""
        self.ListaArgs.append(self.ListaArg("Reporte Pedido"))
        sumlista = "".join(self.ListaArgs)
        sumlista2 = ""
        if self.rpc_server is not None:
            sumlista2 = "".join(self.rpc_server.ListaArgs)
        return print(
            self.report_object.display(self.robot_object, self.rpc_server) +
            "\n\n>>>>>> Lista de Ordenes Recibidas <<<<<<\n" + sumlista +
            "\n\n>>>>>>      CLIENTE     <<<<<<\n" + sumlista2)

    def do_status(self, value):
        """Devuelve el estado de conexion del servidor"""
        if self.rpc_server == None:
            print("Estado servidor : Desconectado")
        else:
            print("Estado servidor : Conectado")

    def ListaArg(self, order_type):
        return ("[" + time.strftime("%a, %d %b %Y %H:%M:%S") + "]:      " +
                order_type + "\n")
