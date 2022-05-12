#include "Cliente.h"

int main(int argc, char const *argv[]) {
  XmlRpcClient c = XmlRpcClient("127.0.0.1", 8891);
  Cliente *cli;
  cli = new Cliente();
  int seleccion;
  bool condicion = true;
  while (condicion) {
    seleccion = cli->MostrarMenu();
    cli->InterpretaComando(seleccion,c);
  }
}
