#include "RobotInterface.h"
#include "UserInterface.h"
#include <thread>

#define HOST "127.0.0.1"
#define PORT 8891

int main(int argc, char const *argv[])
{

  XmlRpc::XmlRpcClient* xmlRpcClient = new XmlRpc::XmlRpcClient(HOST, PORT);
  std::shared_ptr<RobotInterface::RobotInterface> robotInterface = std::make_shared<RobotInterface::RobotInterface>(xmlRpcClient);
  UserInterface::UserInterface userInterface(robotInterface);

  userInterface.run();

}
