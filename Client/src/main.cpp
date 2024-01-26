#include "RobotInterface.h"
#include "UserInterface.h"

#define HOST "127.0.0.1"
#define PORT 8891

int main(int argc, char const *argv[])
{

  XmlRpc::XmlRpcClient* xmlRpcClient = new XmlRpc::XmlRpcClient(HOST, PORT);
  RobotInterface::RobotInterface* robotInterface = new RobotInterface::RobotInterface(xmlRpcClient);
  UserInterface::UserInterface userInterface(robotInterface);
  
  int selection;

  while (true)
  {
    selection = userInterface.DisplayMenu();
    userInterface.ParseCommand(selection);
  }

}
