from xmlrpc.server import SimpleXMLRPCServer
from util.logger import get_logger
from threading import Thread
from AutoMode import AutoMode
from Report import Report
from RobotRRR import RobotRRR
import socket
import time

logger = get_logger("ServerXMLRPC")


class ServerXMLRPC:

    server = None
    RPCport = 8891

    def __init__(self,
                 robot_object: RobotRRR,
                 report_object: Report,
                 port: int = RPCport):
        ##Estado de conexion: 0->desconectado / 1->conectado
        self.conn_status = 0
        self.robot_object = robot_object
        self.report_object = report_object
        self.ListaArgs = []
        self.port = port
        self.running = False
        
        self.init_server(port)

        #Registramos las funciones
        self.server.register_function(self.do_setModo, "setModoOperacion")
        self.server.register_function(self.do_setAngles, "setAngulos")
        self.server.register_function(self.do_setRotationDirection,
                                      "setSentidoGiro")
        self.server.register_function(self.do_turnRobotOn, "encenderRobot")
        self.server.register_function(self.do_setSpeed, "setVelocidad")
        self.server.register_function(self.do_move, "mover")
        self.server.register_function(self.do_moveOrigin, "reset")
        self.server.register_function(self.do_showReport, "mostrarReporte")
        self.server.register_function(self.do_getConnectionStatus,
                                      "conexionServidor")

        #Lanzamiento del Servidor
        self.thread = Thread(target=self.run_server)
        self.thread.start()

        logger.info("RPC iniciado en port: %s", str(self.server.server_address))
        self.conn_status = 1
        
    def init_server(self, port):
        "Instancia el servidor XMLRPC en el puerto adecuado."
        try_n = 0
        
        while True:
            try:
                self.server = SimpleXMLRPCServer(("localhost", self.port),
                                                    allow_none=True)
                
                
                if self.port != port:
                    logger.error("Server RPC en puerto no estandar {%d}", self.port)
                
                break
                    
            except socket.error as e:
                
                try_n+=1
                if try_n > 5:
                    break
                
                if e.errno == 98:
                    self.port+=1
                    logger.info("Problema al iniciar el Servidor, puerto no disponible")
                else:
                    logger.error("Problema al iniciar el Servidor")
                    raise
            

    def run_server(self) -> None:
        self.running = True
        self.server.serve_forever()

    def shutdown(self) -> None:
        
        if self.running is True:
            self.running = False
            self.server.shutdown()
            self.thread.join()
            logger.info("Servidor Desconectado")
        
        else:
            logger.info("Server is not running")

    def do_setModo(self, operation_mode) -> str:

        if self.robot_object.status == 1:
            if operation_mode == 0:
                self.ListaArgs.append(self.ListaArg("Modo Operacion Manual"))
                message = "Modo Manual Seteado"
                self.robot_object.setOperationMode(operation_mode)

            elif operation_mode == 1:
                self.robot_object.setOperationMode(operation_mode)
                self.ListaArgs.append(self.ListaArg("Modo Operacion Autónomo"))
                message = "Modo Autonomo Seteado"
                autoMode = AutoMode(self.robot_object, self.ListaArgs)
                autoMode.readFile()
                autoMode.parseLines()

        elif self.robot_object.status == 0:
            message = "El Robot se encuentra apagado, debe encenderlo"

        return message

    def do_setAngles(self, a1: float, a2: float, a3: float) -> str:
        self.robot_object.setAngles(a1, a2, a3)
        self.ListaArgs.append(self.ListaArg("Set Angulo Articulaciones"))
        return "Angulos configurados."

    def do_setRotationDirection(self, s1: str, s2: str, s3: str) -> str:
        input_direction = [s1, s2, s3]
        output_direction = []

        for i in range(3):
            if input_direction[i] == 1:
                output_direction.append("der")

            elif input_direction[i] == 0:
                output_direction.append("izq")

        self.robot_object.setRotationDirection(output_direction[0],
                                               output_direction[1],
                                               output_direction[2])
        self.ListaArgs.append(self.ListaArg("Set Giro Articulaciones "))

        return "Dirección de Rotación Seteada."

    def do_turnRobotOn(self, status) -> str:

        if status == 0:
            self.robot_object.setStatus(status)
            self.ListaArgs.append(self.ListaArg("Robot Apagado"))
            message = "Robot Apagado"

        elif status == 1:
            self.robot_object.setStatus(int(status))
            self.ListaArgs.append(self.ListaArg("Robot Encendido"))
            message = "Robot Encendido"

        return message

    def do_setSpeed(self, speed: float) -> str:
        self.robot_object.setSpeed(speed)
        self.ListaArgs.append(self.ListaArg("Set Velocidad"))
        return "Velocidad Seteada"

    def do_move(self, action_gripper) -> str:

        if self.robot_object.status == 1:
            self.robot_object.MoveJoint()
            self.robot_object.MoveGripper(action_gripper)
            self.ListaArgs.append(self.ListaArg("Movimiento Realizado"))

        elif self.robot_object.status == 0:
            return "El robot se encuentra apagado (estado = 0), no se puede realizar el movimiento"

        return "Robot Movilizado."

    def do_moveOrigin(self) -> str:
        self.robot_object.MoveOrigin()
        self.ListaArgs.append(self.ListaArg("Homing"))
        return "Robot en Posición de Origen"

    def do_showReport(self) -> str:
        self.ListaArgs.append(self.ListaArg("Reporte Pedido"))
        sumlista = "".join(self.ListaArgs)
        return (str(self.report_object.display(self.robot_object, self)) +
                "\n\n>>>>>> Lista de Ordenes Recibidas <<<<<<\n" + sumlista)

    def do_getConnectionStatus(self) -> str:
        return "Servidor: Conectado"

    def ListaArg(self, order_type) -> str:
        return (time.strftime("%a, %d %b %Y %H:%M:%S") + ": [Cliente] " +
                order_type + "\n")
