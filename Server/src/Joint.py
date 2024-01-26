import time


class Joint:

    def rotate(self):
        if (self.rotation_direction == "der"):
            self.total_angle = self.total_angle + self.rotation_angle
            time.sleep(0.5)

        elif (self.rotation_direction == "izq"):
            self.total_angle = self.total_angle - self.rotation_angle
            time.sleep(0.5)

    def __init__(self):

        self.rotation_angle = 0
        self.rotation_direction = "der"
        self.total_angle = 0
        self.speed = 0

        ##Tiempo de operacion de cada articulacion
        self.ONtime = []

        ##Tiempo de inicio de movimiento en cada articulacion.
        self.init_time = []
