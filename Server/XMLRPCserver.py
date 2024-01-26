from xmlrpc.server import SimpleXMLRPCServer
from threading import Thread
from ModoAutonomo import ModoAutonomo
import socket
import time

class ServerXMLRPC():
    server = None
    RPCport = 8891

    def __init__(self,objetoRobot,objetoReporte,port = RPCport):
        ##Estado de conexion: 0->desconectado / 1->conectado
        self.estadoDeConexion = 0
        self.objetoRobot = objetoRobot
        self.objetoReporte = objetoReporte
        self.ListaArgs=[]
        self.puerto = port
        while True:
            try:
                self.server = SimpleXMLRPCServer(("localhost", self.puerto),allow_none = True)
                if self.puerto != port:
                    print("Server RPC en puerto no estandar {%d}" % self.puerto)
                break
            except socket.error as e:
                if e.errno == 98:
                    self.puerto+=1
                    continue
                else:
                    print("Problema al iniciar el Servidor")
                    raise

        #Registramos las funciones
        self.server.register_function(self.do_setModo,"setModoOperacion")
        self.server.register_function(self.do_setAngulos,"setAngulos")
        self.server.register_function(self.do_setSentidoGiro,"setSentidoGiro")
        self.server.register_function(self.do_encenderRobot,"encenderRobot")
        self.server.register_function(self.do_setVelocidad,"setVelocidad")
        self.server.register_function(self.do_mover,"mover")
        self.server.register_function(self.do_moverOrigen,"reset")
        self.server.register_function(self.do_mostrarReporte,"mostrarReporte")
        self.server.register_function(self.do_conexionServidor,"conexionServidor")


        #Lanzamiento del Servidor
        self.thread = Thread(target = self.run_server)
        self.thread.start()
        print("RPC iniciado en puerto",str(self.server.server_address))
        self.estadoDeConexion = 1

    def run_server(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.thread.join()
        return print("Desconectado")

        ###############################################################
        #####################OPERACIONES REGISTRADAS###################
        ###############################################################

    def do_setModo(self,modoOperacion):
        if self.objetoRobot.estado == 1:
            if modoOperacion == 0:
                self.ListaArgs.append(self.ListaArg("Modo Operacion Manual"))
                print("Modo manual seteado")
                self.objetoRobot.setModoOperacion(modoOperacion)
            elif modoOperacion == 1:
                self.objetoRobot.setModoOperacion(modoOperacion)
                self.ListaArgs.append(self.ListaArg("Modo Operacion Autónomo"))
                print("Modo autónomo seteado")
                modoAutonomo = ModoAutonomo(self.objetoRobot,self.ListaArgs)
                modoAutonomo.leerFichero()
                modoAutonomo.interpretarLineas()
            retorno = "Recibido"
        elif self.objetoRobot.estado == 0:
            retorno = "El Robot se encuentra apagado, debe encenderlo"
        return retorno

    def do_setAngulos(self,a1,a2,a3):
        self.objetoRobot.setAngulos(a1,a2,a3)
        self.ListaArgs.append(self.ListaArg("Set Angulo Articulaciones"))
        return "Recibido"

    def do_setSentidoGiro(self,s1,s2,s3):
        sentidoEntrada = [s1,s2,s3]
        sentidoSalida = []
        for i in range(3):
            if sentidoEntrada[i] == 1:
                sentidoSalida.append("der")
            elif sentidoEntrada[i] == 0:
                sentidoSalida.append("izq")
        self.objetoRobot.setSentidoGiro(sentidoSalida[0],sentidoSalida[1],sentidoSalida[2])
        self.ListaArgs.append(self.ListaArg("Set Giro Articulaciones "))
        return "Recibido"

    def do_encenderRobot(self,estado):
        if estado == 0:
            self.objetoRobot.setEstado(estado)
            self.ListaArgs.append(self.ListaArg("Robot Apagado"))
        elif estado == 1 :
            self.objetoRobot.setEstado(int(estado))
            self.ListaArgs.append(self.ListaArg("Robot Encendido"))
        return "Recibido"

    def do_setVelocidad(self,velocidad):
        self.objetoRobot.setVelocidad(velocidad)
        self.ListaArgs.append(self.ListaArg("Set Velocidad"))
        return "Recibido"

    def do_mover(self,accionPinza):
        if self.objetoRobot.estado == 1:
            self.objetoRobot.MoverArticulacion()
            self.objetoRobot.MoverPinza(accionPinza)
            self.ListaArgs.append(self.ListaArg("Movimiento Realizado"))
        elif self.objetoRobot.estado == 0:
            return "El robot se encuentra apagado (estado = 0), no se puede realizar el movimiento"
        return "Recibido"

    def do_moverOrigen(self):
        self.objetoRobot.MoverOrigen()
        self.ListaArgs.append(self.ListaArg("Homing"))
        return "Recibido"

    def do_mostrarReporte(self):
        self.ListaArgs.append(self.ListaArg("Reporte Pedido"))
        sumlista="".join(self.ListaArgs)
        return (str(self.objetoReporte.mostrarDatos(self.objetoRobot,self))
        +"\n\n>>>>>> Lista de Ordenes Recibidas <<<<<<\n"+sumlista)

    def do_conexionServidor(self):
        return "Servidor: Conectado"

    def ListaArg(self,ordertype):
        return (time.strftime("%a, %d %b %Y %H:%M:%S") +": [Cliente] "+ordertype+"\n")
