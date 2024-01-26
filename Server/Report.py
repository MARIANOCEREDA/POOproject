from RobotRRR import RobotRRR

class Report:

    def display(self, robot_object, rpc_server):
        at = []
        a = []
        ti = []
        tt = []

        for i in range(3):
            a.append(str(robot_object.angles[i]))
            at.append(str(robot_object.joints[i].total_angle))
            ti.append(str(robot_object.joints[i].init_time))
            tt.append(str(robot_object.joints[i].ONtime))

        speed_list = str(robot_object.joints[1].speed)
        if rpc_server == None:
            state= "Desconectado"
        else:
            conn_status =str(rpc_server.conn_status)
            if conn_status  == "1":
                state= "Conectado"
            else:
                state= "Desconectado"

        if robot_object.operation_mode == 0:
            mode = "Manual"
        elif robot_object.operation_mode == 1:
            mode = "Autonomo"
 
        if robot_object.gripper.status == 1:
            gripper_status = "Abierta"
        elif robot_object.gripper.status == 0:
            gripper_status = "Cerrada"

        return ("Reporte de Estado ROBOT"
        +"\nConexion:"+state
        +"\nModo de Operacion:"+ mode
        +"\nVelocidad Articulaciones:"+ speed_list
        +"\nEstado de la pinza:"+ gripper_status
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
