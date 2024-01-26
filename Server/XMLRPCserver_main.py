from Console import Console
from RobotRRR import RobotRRR
from Report import Report

if __name__ == '__main__':
    robot = RobotRRR()
    report = Report()
    uncli = Console(robot, report)
    uncli.prompt = '>> '
    uncli.cmdloop('Ingrese comandos: ')
