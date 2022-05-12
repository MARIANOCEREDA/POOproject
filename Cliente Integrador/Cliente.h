#include <iostream>
#include <stdlib.h>
#include <string>
using namespace std;
#include "XmlRpc.h"
using namespace XmlRpc;


class Cliente{
public:
  int MostrarMenu();
  void InterpretaComando(int,XmlRpcClient);
  void EnviarMensaje(XmlRpcValue,XmlRpcValue,const char*,XmlRpcClient);
  bool VerificarEntrada(int,string tareaSTR);
};

class ErrorSeleccion{};
class ErrorEntrada{};
