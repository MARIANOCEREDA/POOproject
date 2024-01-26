#include "UserInterface.h"


void UserInterface::UserInterface::Terminate()
{
  stopLoops = true;
  conditionVariable.notify_one();
};


void UserInterface::UserInterface::DisplayMenu()
{
    std::unique_lock<std::mutex> lck(coutMutex);

    std::cout << "---------------------------------------------------------------" << std::endl;
    std::cout << "*--> SELECCIONE LA OPERACIÓN QUE DESEA REALIZAR <--*" <<  std::endl;
    std::cout << ">> 0- Estado de conexion del servidor "<< std::endl;
    std::cout << ">> 1- Setear modo de operacion | 0->Manual / 1->Automatico "<< std::endl;
    std::cout << ">> 2- Encender o Apagar robot  | 0->Apagar / 1->Encender "<< std::endl;
    std::cout << ">> 3- Setear angulo y sentido giro de articulaciones"<< std::endl;
    std::cout << ">> 4- Setear velocidad de articulaciones" << std::endl;
    std::cout << ">> 5- Mover el robot y setear operacion de la pinza | 0->Cerrar / 1->Abrir"<< std::endl;
    std::cout << ">> 6- Mover Robot a posicion de origen"<< std::endl;
    std::cout << ">> 7- Solicitar reporte"<< std::endl;
    std::cout << ">> 8- Mostrar Menu" << std::endl;
    std::cout << ">> 9- Salir"<< std::endl;
    std::cout << "---------------------------------------------------------------" << std::endl;

    lck.unlock();
};

void UserInterface::UserInterface::InputLoop()
{
    int selection = -1;

    while(!stopLoops)
    {
      std::unique_lock<std::mutex> lckRobotOperation(robotOperation);
      robotOperationFinishedConditional.wait(lckRobotOperation, [this] {
        return robotTaskFinished;
      });

      std::cout << ">> ";
      std::cin >> selection;

      robotTaskFinished = false;
      lckRobotOperation.unlock();

      if ((selection < 0 || selection > 9) && selection != -1)
      {
        std::cerr << ">> Entrada Invalida: Debe estar entre 1 y 8." << std::endl;
      }
      else
      {
        std::unique_lock<std::mutex> lck(queueMutex);
        messageQueue.push(selection);
        conditionVariable.notify_one();
      }

      selection = -1;
  }
}

void UserInterface::UserInterface::ParseCommand()
{

  int input = 0;
  std::vector<int> joints(3);
  XmlRpc::XmlRpcValue noArgs, result, oneArg, args;

  while(!stopLoops)
  {
    std::unique_lock<std::mutex> lckQueue(queueMutex);
    conditionVariable.wait(lckQueue, [this] {
      return !messageQueue.empty();
    });

    if(!messageQueue.empty())
    {
      int selection = messageQueue.front();
      messageQueue.pop();

      std::unique_lock<std::mutex> lckRobotOperation(robotOperation);

      try
      {
        switch (selection)
        {
          case 0:

              if(robotInterface->Connect())
              {
                std::cout << ">> Mensaje servidor: Connection is OK" << std::endl;
              }
              else
              {
                std::cout << ">> Servidor desconectado" << std::endl;
              }

              break;

          case 1:
              std::cout << ">> Modo de Operacion: "<< std::endl;

              std::cout << "--> ";

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
              
              std::cout << "--> ";
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
                std::cout << "--> ";
                std::cin >> input;
                joints.push_back(input);
                args[i] = input;
              }

              robotInterface->SendMessage(args, result, task.SET_ANGLES);

              std::cout << ">> Ingrese sentidos de giro de las 3 articulaciones (1->derecha / 0->izquierda): "<< std::endl;
              
              for (int i = 0; i < 3; i++)
              {
                std::cout << "--> ";
                std::cin >> input;

                if(!(input == 0 || input == 1))
                {
                  std::cout << "Los valores deben ser 0 o 1" << std::endl;
                  i--;
                }
                else
                {
                  joints.push_back(input);
                  args[i] = input;
                }

              }

              robotInterface->SendMessage(args, result, task.SET_ROTATION_DIR);

              break;

          case 4:
              std::cout << ">> Ingrese la velocidad de las articulaciones: "<< std::endl;
              
              std::cout << "--> ";
              std::cin >> input;
              oneArg[0] = input;

              robotInterface->SendMessage(oneArg, result, task.SET_SPEED);

              break;

          case 5:
              std::cout << ">> Mover y Abrir/Cerrar pinza: "<< std::endl;
              
              std::cout << "--> ";
              std::cin >> input;
              oneArg[0] = input;

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
              DisplayMenu();
              break;

          case 9:
              exitRequested = true;
              Terminate();
              std::cout << ">> Ha salido del programa"<< std::endl;
              exit(1);

          default:
              break;
        }
      }
      catch(const CustomExceptions::InputError& e)
      {
        std::cerr << "---------------------------------" << std::endl;
        std::cerr << e.what() << std::endl;
        std::cerr << "---------------------------------" << std::endl;
      }

      joints.clear();
      robotTaskFinished = true;
      robotOperationFinishedConditional.notify_one();
      lckRobotOperation.unlock();
    }

    lckQueue.unlock();
  }
}

void UserInterface::UserInterface::Initialize()
{
  if(!initialized)
  {
    inputThread = std::make_shared<std::thread>(&UserInterface::InputLoop, this);
    writeThread = std::make_shared<std::thread>(&UserInterface::ParseCommand, this);

    inputThread->join();
    writeThread->join();

    initialized = true;
    stopLoops = false;
  }

};

bool UserInterface::UserInterface::VerifyInput(int input, const char* task)
{
  return true ? (input == 0 || input == 1) : false;
};

void UserInterface::UserInterface::run()
{
  int selection;
  bool exitRequested = false;
  
  DisplayMenu();
  Initialize();
}