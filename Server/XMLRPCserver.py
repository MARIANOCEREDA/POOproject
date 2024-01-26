from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
from AutoMode import AutoMode
from Report import Report
from RobotRRR import RobotRRR
import socket
import time

class ServerXMLRPC:

    server = None
    RPCport = 8891

    def __init__(self, robot_object:RobotRRR, report_object:Report, port:int = RPCport):
        ##Estado de conexion: 0->desconectado / 1->conectado
        self.conn_status = 0
        self.robot_object = robot_object
        self.report_object = report_object
        self.ListaArgs = []
        self.port = port

        while True:
            try:
                self.server = SimpleXMLRPCServer(("localhost", self.port), allow_none = True)
                if self.port != port:
                    print("Server RPC en puerto no estandar {%d}" % self.port)
                break

            except socket.error as e:
                if e.errno == 98:
                    self.port+=1
                    continue
                else:
                    print("Problema al iniciar el Servidor")
                    raise

        #Registramos las funciones
        self.server.register_function(self.do_setModo,"setoperation_mode")
        self.server.register_function(self.do_setAngles,"setAngulos")
        self.server.register_function(self.do_setRotationDirection,"setSentidoGiro")
        self.server.register_function(self.do_turnRobotOn,"encenderRobot")
        self.server.register_function(self.do_setSpeed,"setVelocidad")
        self.server.register_function(self.do_move,"mover")
        self.server.register_function(self.do_moveOrigin,"reset")
        self.server.register_function(self.do_showReport,"mostrarReporte")
        self.server.register_function(self.do_getConnectionStatus,"conexionServidor")


        #Lanzamiento del Servidor
        self.thread = Thread(target = self.run_server)
        self.thread.start()
        
        print("RPC iniciado en port: ", str(self.server.server_address))
        self.conn_status = 1

    def run_server(self) -> None:
        self.server.serve_forever()

    def shutdown(self) -> None:
        self.server.shutdown()
        self.thread.join()
        print("Desconectado")

    def do_setModo(self, operation_mode) -> str:
        
        if self.robot_object.status == 1:
            if operation_mode == 0:
                self.ListaArgs.append(self.ListaArg("Modo Operacion Manual"))
                print("Modo manual seteado")
                self.robot_object.setOperationMode(operation_mode)
                
            elif operation_mode == 1:
                self.robot_object.setOperationMode(operation_mode)
                self.ListaArgs.append(self.ListaArg("Modo Operacion Autónomo"))
                print("Modo autónomo seteado")
                autoMode = AutoMode(self.robot_object, self.ListaArgs)
                autoMode.readFile()
                autoMode.parseLines()
                
            message = "Recibido"
            
        elif self.robot_object.status == 0:
            message = "El Robot se encuentra apagado, debe encenderlo"
            
        return message

    def do_setAngles(self, a1:float, a2:float, a3:float) -> str:
        self.robot_object.setAngles(a1, a2, a3)
        self.ListaArgs.append(self.ListaArg("Set Angulo Articulaciones"))
        return "Recibido"

    def do_setRotationDirection(self, s1:str, s2:str, s3:str) -> str:
        input_direction = [s1, s2, s3]
        output_direction = []
        
        for i in range(3):
            if input_direction[i] == 1:
                output_direction.append("der")
                
            elif input_direction[i] == 0:
                output_direction.append("izq")
                
        self.robot_object.setRotationDirection(output_direction[0], output_direction[1], output_direction[2])
        self.ListaArgs.append(self.ListaArg("Set Giro Articulaciones "))
        
        return "Recibido"

    def do_turnRobotOn(self, status) -> str:
        
        if status == 0:
            self.robot_object.setStatus(status)
            self.ListaArgs.append(self.ListaArg("Robot Apagado"))
            
        elif status == 1 :
            self.robot_object.setStatus(int(status))
            self.ListaArgs.append(self.ListaArg("Robot Encendido"))
            
        return "Recibido"

    def do_setSpeed(self, speed:float) -> str:
        self.robot_object.setSpeed(speed)
        self.ListaArgs.append(self.ListaArg("Set Velocidad"))
        return "Recibido"

    def do_move(self, action_gripper) -> str:
        
        if self.robot_object.status == 1:
            self.robot_object.MoveJoint()
            self.robot_object.MoveGripper(action_gripper)
            self.ListaArgs.append(self.ListaArg("Movimiento Realizado"))
            
        elif self.robot_object.status == 0:
            return "El robot se encuentra apagado (estado = 0), no se puede realizar el movimiento"
        
        return "Recibido"

    def do_moveOrigin(self) -> str:
        self.robot_object.MoveOrigin()
        self.ListaArgs.append(self.ListaArg("Homing"))
        return "Recibido"

    def do_showReport(self) -> str:
        self.ListaArgs.append(self.ListaArg("Reporte Pedido"))
        sumlista="".join(self.ListaArgs)
        return (str(self.report_object.display(self.robot_object, self))
        +"\n\n>>>>>> Lista de Ordenes Recibidas <<<<<<\n"+ sumlista)

    def do_getConnectionStatus(self) -> str:
        return "Servidor: Conectado"

    def ListaArg(self, order_type) -> str:
        return (time.strftime("%a, %d %b %Y %H:%M:%S") +": [Cliente] "+ order_type +"\n")
