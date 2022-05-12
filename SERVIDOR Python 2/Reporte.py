from RobotRRR import RobotRRR
from XMLRPCserver import ServerXMLRPC

class Reporte():

    def mostrarDatos(self,objetoRobot,rpc_server):
        at = []
        a = []
        ti = []
        tt = []
        for i in range(3):
            a.append(str(objetoRobot.listaAngulos[i]))
            at.append(str(objetoRobot.arrayArticulaciones[i].anguloTotal))
            ti.append(str(objetoRobot.arrayArticulaciones[i].tiempoDeInicio))
            tt.append(str(objetoRobot.arrayArticulaciones[i].tiempoON))

        velocidad = str(objetoRobot.arrayArticulaciones[1].velocidad)
        if rpc_server == None:
            state= "Desconectado"
        else:
            estadoConexion=str(rpc_server.estadoDeConexion)
            if estadoConexion == "1":
                state= "Conectado"
            else:
                state= "Desconectado"

        if objetoRobot.modoOperacion == 0:
            modo = "Manual"
        elif objetoRobot.modoOperacion == 1:
            modo = "Autonomo"
 
        if objetoRobot.pinza.estadoPinza == 1:
            estadoP = "Abierta"
        elif objetoRobot.pinza.estadoPinza == 0:
            estadoP = "Cerrada"

        return ("Reporte de Estado ROBOT"
        +"\nConexion:"+state
        +"\nModo de Operacion:"+modo
        +"\nVelocidad Articulaciones:"+velocidad
        +"\nEstado de la pinza:"+estadoP
        +"\n>>>>>> Articulacion 1 <<<<<<"
        +"\n\tAngulo Rotado:"+a[0]
        +"\n\tAngulo Total:"+at[0]
        +"\n\tTiempo Inicio Movimiento:"+ti[0]
        +"\n\tTiempo En Movimiento:"+tt[0]
        +"\n\n>>>>>> Articulacion 2 <<<<<<"
        +"\n\tAngulo Rotado:"+a[1]
        +"\n\tAngulo Total:"+at[1]
        +"\n\tTiempo Inicio Movimiento:"+ti[1]
        +"\n\tTiempo En Movimiento:"+tt[1]
        +"\n\n>>>>>> Articulacion 3 <<<<<<"
        +"\n\tAngulo Rotado:"+a[2]
        +"\n\tAngulo Total:"+at[2]
        +"\n\tTiempo Inicio Movimiento:"+ti[2]
        +"\n\tTiempo En Movimiento:"+tt[2])
