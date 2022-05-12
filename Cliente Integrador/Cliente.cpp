#include "Cliente.h"

int Cliente::MostrarMenu(){
  int seleccion;
  try{
  cout << "---------------------------------------------------------------" << '\n';
  cout << "*--> SELECCIONE LA OPERACIÓN QUE DESEA REALIZAR <--*" << endl;
  cout << ">> 0- Estado de conexion del servidor "<<endl;
  cout << ">> 1- Setear modo de operacion | 0->Manual / 1->Automatico "<<endl;
  cout << ">> 2- Encender o Apagar robot  | 0->Apagar / 1->Encender "<<endl;
  cout << ">> 3- Setear angulo y sentido giro de articulaciones"<<endl;
  cout << ">> 4- Setear velocidad de articulaciones" <<endl;
  cout << ">> 5- Mover el robot y setear operacion de la pinza | 0->Cerrar / 1->Abrir"<<endl;
  cout << ">> 6- Mover Robot a posicion de origen"<<endl;
  cout << ">> 7- Solicitar reporte"<<endl;
  cout << ">> 8- Salir"<<endl;
  cout << "---------------------------------------------------------------" << '\n';
  cin >> seleccion;
  if (seleccion <0 || seleccion>8){
    throw ErrorSeleccion();
  }
  }catch(ErrorSeleccion){
    cout << "Debe ingresar un numero entre 1  y 8"<<endl;
    cout << "---------------------------------------------------------------" << '\n';
  }
  return seleccion;
};

void Cliente::InterpretaComando(int seleccion,XmlRpcClient c){
int entrada,art1,art2,art3;
XmlRpcValue noArgs, result, oneArg,Args;
const char *tarea;
string tareaSTR;
try{
    switch (seleccion) {
      case 0:
          tarea = "conexionServidor";
          if(c.execute("conexionServidor",noArgs,result)){
            cout << "Mensaje servidor: "<<result << '\n';
          }else{
            cout << "Servidor desconectado" <<endl;
          }
          break;
      case 1:
          cout << ">> Modo de Operacion: "<<endl;
          cin >> entrada;
          oneArg[0]=entrada;
          tarea = "setModoOperacion";
          tareaSTR = "setModoOperacion";
          if (this->VerificarEntrada(entrada,tareaSTR)) {
              this->EnviarMensaje(oneArg,result,tarea,c);
          }else{
            throw ErrorEntrada();
          }
          break;
      case 2:
          cout << ">> Encender/Apagar robot: "<<endl;
          cin >> entrada;
          oneArg[0]=entrada;
          tarea = "encenderRobot";
          tareaSTR = "encenderRobot";
          if (this->VerificarEntrada(entrada,tareaSTR)) {
              this->EnviarMensaje(oneArg,result,tarea,c);
          }else{
            throw ErrorEntrada();
          }
          break;
      case 3:
          cout << ">> Ingrese los angulos de las 3 articulaciones: "<<endl;
          cin >> art1;
          cin >> art2;
          cin >> art3;
          Args[0]= art1;
          Args[1]= art2;
          Args[2]= art3;
          tarea = "setAngulos";
          this->EnviarMensaje(Args,result,tarea,c);
          cout << ">> Ingrese sentidos de giro de las 3 articulaciones (1->derecha / 0->izquierda): "<<endl;
          cin >> art1;
          cin >> art2;
          cin >> art3;
          Args[0]= art1;
          Args[1]= art2;
          Args[2]= art3;
          tarea = "setSentidoGiro";
          this->EnviarMensaje(Args,result,tarea,c);
          break;
      case 4:
          cout << ">> Ingrese la velocidad de las articulaciones: "<<endl;
          cin >> entrada;
          oneArg[0]= entrada;
          tarea = "setVelocidad";
          this->EnviarMensaje(oneArg,result,tarea,c);
          break;
      case 5:
          cout << ">> Mover y Abrir/Cerrar pinza: "<<endl;
          cin >> entrada;
          oneArg[0]= entrada;
          tarea = "mover";
          tareaSTR = "mover";
          if (this->VerificarEntrada(entrada,tareaSTR)) {
              this->EnviarMensaje(oneArg,result,tarea,c);
          }else{
            throw ErrorEntrada();
          }
          break;
      case 6:
          tarea = "reset";
          this->EnviarMensaje(noArgs,result,tarea,c);
          break;
      case 7:
          tarea = "mostrarReporte";
          this->EnviarMensaje(noArgs,result,tarea,c);
          break;
      case 8:
          cout << "Ha salido del programa"<<endl;
          exit(1);
      default:
          break;
    }
  }catch(ErrorEntrada){
    cout << "-----------ERROR---------------" << '\n';
    cout << "Debe ingresar un comando válido" << '\n';
    cout << "-------------------------------" << '\n';
  }
}

bool Cliente::VerificarEntrada(int entrada, string tareaSTR){
  bool condicion = false;
  if (tareaSTR == "setModoOperacion" || tareaSTR == "encenderRobot" || tareaSTR == "mover") {
    switch (entrada) {
      case 0:
      case 1:
      condicion = true;
      break;
      default:
      break;
    }
  }
  return condicion;
};

void Cliente::EnviarMensaje(XmlRpcValue arg,XmlRpcValue result,const char *tarea,XmlRpcClient c){
  c.execute(tarea,arg,result);
  cout << "Mensaje servidor: "<< result <<endl;
};
