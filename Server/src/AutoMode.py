from RobotRRR import RobotRRR
import time


class AutoMode:

    def __init__(self, robot_object: RobotRRR, arguments_list):

        self.file_content = []
        self.robot_object = robot_object
        self.arguments_list = arguments_list

    def readFile(self):

        with open("util/modoAutonomo.txt", "r") as file:
            self.file_content = file.readlines()

    def parseLines(self):

        print(self.file_content[0][0:8])

        if self.file_content[0][0:8] == "encender":
            self.robot_object.status = 1
            self.arguments_list.append(
                self.ListaArg("Robot Encendido [MODO AUTONOMO]")
                )

        elif self.file_content[0][0:7] == "apagar":
            self.robot_object.status = 0
            self.arguments_list.append(
                self.ListaArg("Robot Apagado [MODO AUTONOMO]")
                )

        self.robot_object.setAngles(
            int(self.file_content[1]), int(self.file_content[2]),
            int(self.file_content[3])
            )
        self.arguments_list.append(
            self.ListaArg("Set Angulos Articulaciones [MODO AUTONOMO] ")
            )
        self.robot_object.setVelocidad(self.file_content[4])
        self.arguments_list.append(
            self.ListaArg("Set Velocidad [MODO AUTONOMO]")
            )

        s1REC = self.file_content[5]
        s2REC = self.file_content[6]
        s3REC = self.file_content[7]

        self.robot_object.setRotationDirection(
            s1REC[0:3], s2REC[0:3], s3REC[0:3]
            )
        self.arguments_list.append(
            self.ListaArg("Set Giro Articulaciones [MODO AUTONOMO]")
            )

        if self.file_content[8][0:5] == "abrir":
            self.robot_object.MoveGripper(1)
            self.arguments_list.append(
                self.ListaArg("Pinza abierta [MODO AUTONOMO]")
                )
        elif self.file_content[8][0:6] == "cerrar":
            self.robot_object.MoverPinza(0)
            self.arguments_list.append(
                self.ListaArg("Pinza cerrada [MODO AUTONOMO]")
                )

        self.robot_object.MoveJoint()
        self.arguments_list.append(
            self.ListaArg("Movimiento Realizado [MODO AUTONOMO]")
            )

        if self.file_content[9][0:11] == "moverOrigen":
            self.robot_object.MoverOrigen()
            self.arguments_list.append(self.ListaArg("Homing [MODO AUTONOMO]"))

    def ListaArg(self, order_type):
        return (
            "[" + time.strftime("%a, %d %b %Y %H:%M:%S") + "]:      " +
            order_type + "\n"
            )
