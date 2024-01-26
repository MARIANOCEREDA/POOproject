from consolaServidor import consolaServidor
from RobotRRR import RobotRRR
from Reporte import Reporte

if __name__ == '__main__':
    objetoRobot = RobotRRR()
    objetoReporte = Reporte()
    uncli = consolaServidor(objetoRobot,objetoReporte)
    uncli.prompt = '>> '
    uncli.cmdloop('Ingrese comandos: ')
