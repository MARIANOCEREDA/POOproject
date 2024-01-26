#include <iostream>
#include <string>

#if !defined(TASKS_H)
#define TASKS_H

namespace Tasks
{
    struct Tasks
    {
        const char* CONNECT_TO_SERVER = "conexionServidor";
        const char* SET_OPERATION_MODE = "setModoOperacion";
        const char* TURN_ON_ROBOT = "encenderRobot";
        const char* SET_ANGLES = "setAngulos";
        const char* SET_ROTATION_DIR = "setSentidoGiro";
        const char* SET_SPEED = "setVelocidad";
        const char* MOVE = "mover";
        const char* RESET = "reset";
        const char* SHOW_REPORT = "mostrarReporte";
    };

};


#endif // MACRO

