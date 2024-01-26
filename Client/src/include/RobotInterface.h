#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>

#include "XmlRpc.h"
#include "Tasks.h"
#include "CustomExceptions.h"

#if !defined(ROBOT_INTERFACE_H)
#define ROBOT_INTERFACE_H

namespace RobotInterface
{
  class RobotInterface
  {

  private:
    Tasks::Tasks task;
    XmlRpc::XmlRpcClient* xmlRpcClient;

  public:
    RobotInterface(XmlRpc::XmlRpcClient* c) : xmlRpcClient(c) {}; 
    ~RobotInterface(){ delete xmlRpcClient; };

    void SendMessage(XmlRpc::XmlRpcValue, XmlRpc::XmlRpcValue, const char*);
    bool Connect();

  };

}


#endif // ROBOT_INTERFACE_H



