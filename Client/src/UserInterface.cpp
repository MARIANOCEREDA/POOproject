#include "UserInterface.h"

int UserInterface::UserInterface::DisplayMenu()
{
  int selection;

  try{

    std::cout << "---------------------------------------------------------------" << '\n';
    std::cout << "*--> SELECCIONE LA OPERACIÓN QUE DESEA REALIZAR <--*" <<  std::endl;
    std::cout << ">> 0- Estado de conexion del servidor "<< std::endl;
    std::cout << ">> 1- Setear modo de operacion | 0->Manual / 1->Automatico "<< std::endl;
    std::cout << ">> 2- Encender o Apagar robot  | 0->Apagar / 1->Encender "<< std::endl;
    std::cout << ">> 3- Setear angulo y sentido giro de articulaciones"<< std::endl;
    std::cout << ">> 4- Setear velocidad de articulaciones" << std::endl;
    std::cout << ">> 5- Mover el robot y setear operacion de la pinza | 0->Cerrar / 1->Abrir"<< std::endl;
    std::cout << ">> 6- Mover Robot a posicion de origen"<< std::endl;
    std::cout << ">> 7- Solicitar reporte"<< std::endl;
    std::cout << ">> 8- Salir"<< std::endl;
    std::cout << "---------------------------------------------------------------" << '\n';
    std::cin >> selection;

    if (selection < 0 || selection > 8)
    {
      throw CustomExceptions::ErrorSelection();
    }

  }
  catch(const CustomExceptions::ErrorSelection& e)
  {
    std::cerr << "-----------ERROR---------------" << '\n';
    std::cerr << e.what() << '\n';
    std::cerr << "-------------------------------" << '\n';
  }

  return selection;

};

void UserInterface::UserInterface::ParseCommand(int selection)
{

int input = 0;
std::vector<int> joints;

XmlRpc::XmlRpcValue noArgs, result, oneArg, args;

try{

    switch (selection)
    {
      case 0:
          if(robotInterface->Connect())
          {
            std::cout << "Mensaje servidor: Connection is OK"<< '\n';
          }
          else
          {
            std::cout << "Servidor desconectado" << std::endl;
          }
          break;

      case 1:
          std::cout << ">> Modo de Operacion: "<< std::endl;
          std::cin >> input;
          oneArg[0] = input;

          if(VerifyInput(input, task.SET_OPERATION_MODE))
          {
            robotInterface->SendMessage(oneArg, result, task.SET_OPERATION_MODE);
          }
          else
          {
            throw CustomExceptions::InputError();
          }
          break;

      case 2:
          std::cout << ">> Encender/Apagar robot: "<< std::endl;
          std::cin >> input;
          oneArg[0] = input;

          if (VerifyInput(input, task.TURN_ON_ROBOT))
          {
              robotInterface->SendMessage(oneArg, result, task.TURN_ON_ROBOT);
          }
          else
          {
            throw CustomExceptions::InputError();
          }
          break;

      case 3:
          std::cout << ">> Ingrese los angulos de las 3 articulaciones: "<< std::endl;

          for (int i = 0; i < 3; i++)
          {
            std::cin >> joints[i];
            args[i] = joints[i];
          }

          robotInterface->SendMessage(args, result, task.SET_ANGLES);

          std::cout << ">> Ingrese sentidos de giro de las 3 articulaciones (1->derecha / 0->izquierda): "<< std::endl;
          
          for (int i = 0; i < 3; i++)
          {
            std::cin >> joints[i];
            args[i] = joints[i];
          }

          robotInterface->SendMessage(args, result, task.SET_ROTATION_DIR);
          break;

      case 4:
          std::cout << ">> Ingrese la velocidad de las articulaciones: "<< std::endl;
          std::cin >> input;
          oneArg[0] = input;

          robotInterface->SendMessage(oneArg, result, task.SET_SPEED);
          break;

      case 5:
          std::cout << ">> Mover y Abrir/Cerrar pinza: "<< std::endl;
          std::cin >> input;
          oneArg[0]= input;


          if (VerifyInput(input, task.MOVE))
          {
              robotInterface->SendMessage(oneArg, result, task.MOVE);
          }
          else
          {
            throw CustomExceptions::InputError();
          }
          break;

      case 6:
          robotInterface->SendMessage(noArgs, result, task.RESET);
          break;

      case 7:
          robotInterface->SendMessage(noArgs,result, task.SHOW_REPORT);
          break;

      case 8:
          std::cout << "Ha salido del programa"<< std::endl;
          exit(1);

      default:
          break;

    }
  }
  catch(const CustomExceptions::InputError& e)
  {
    std::cerr << "-----------ERROR---------------" << '\n';
    std::cerr << e.what() << '\n';
    std::cerr << "-------------------------------" << '\n';
  }

}

bool UserInterface::UserInterface::VerifyInput(int input, const char* task)
{
  return true ? (input == 0 || input == 1) : false;
};