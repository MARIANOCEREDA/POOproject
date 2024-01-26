#include "RobotInterface.h"

void RobotInterface::RobotInterface::RobotInterface::RobotInterface::SendMessage(XmlRpc::XmlRpcValue arg, XmlRpc::XmlRpcValue result, const char *tarea)
{
  xmlRpcClient->execute(tarea, arg, result);
  std::cout << "Mensaje servidor: "<< result << std::endl;
};

bool RobotInterface::RobotInterface::Connect()
{
  XmlRpc::XmlRpcValue noArgs, result;
  bool conn = xmlRpcClient->execute(task.CONNECT_TO_SERVER, noArgs, result);
  std::cout << result << std::endl;
  return conn;
}
