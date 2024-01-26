from Joint import Joint
from Gripper import Gripper
import time

class RobotRRR:
    '''
    '''

    def __init__(self):

        ##Tiempo total (suma de cada una de cada operacion)
        self.total_time = 0

        ##Lista comandos: rellena con los ángulos recibidos desde el cliente
        self.angles = [0,0,0]
        self.rotation_direction = ["der","der","der"]

        ##Modo de operacion: 0-> manual / 1-> automatico
        self.operation_mode = 0

        ##Velocidad de operacion:
        self.speed = 0

        ##Estado: 0->apagado / 1->encendido
        self.status = 0

        ##Array de joints
        self.joints=[]
        for i in range(3):
            self.joints.append(Joint())

        self.gripper = Gripper()
        self.duration_time = None

    def setStatus(self, status):
        self.status = status

    def setOperationMode(self, op_mode):
        self.operation_mode = op_mode

    def setAngles(self, a1, a2, a3):
        self.angles = [a1, a2, a3]
        for i in range(3):
            self.joints[i].rotation_direction = self.angles[i]

    def setRotationDirection(self,s1,s2,s3):
        self.rotation_direction = [s1,s2,s3]
        for i in range(3):
            self.joints[i].rotation_direction = self.rotation_direction[i]

    def setSpeed(self, speed:float) -> None:
        self.speed = speed
        for i in range(3):
            self.joints[i].speed = speed

    def MoveGripper(self, action:int) -> None:
        self.gripper.status =  action
        
        if action == 1:
            self.gripper.open()

        if action == 0:
            self.gripper.close()

    def MoveJoint(self) -> None:
        for i in range(3):
            self.joints[i].init_time.append(time.strftime("%a, %d %b %Y %H:%M:%S"))
            init_time = time.time()
            self.joints[i].rotate()
            end_time = time.time()
            self.joints[i].ONtime.append(init_time - end_time)

    def MoveOrigin(self):
        total_angle = []

        for i in range(3):
            total_angle.append(self.joints[i].total_angle)
            if total_angle[i] < 0:
                self.joints[i].rotation_direction = "der"
            elif total_angle[i] > 0:
                self.joints[i].rotation_direction = "izq"

            time_init = time.time()
            self.joints[i].rotate()
            time_end = time.time()
            
            self.joints[i].ONtime.append(time_end - time_init)
