import time


class Gripper:

    def __init__(self):
        self.status = 0

    def open(self):
        time.sleep(0.5)

    def close(self):
        time.sleep(0.5)
