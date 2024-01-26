
#include <iostream>
#include "RobotInterface.h"
#include "CustomExceptions.h"
#include "Tasks.h"

#if !defined(USER_INTERFACE_H)
#define USER_INTERFACE_H

namespace UserInterface
{
    class UserInterface
    {
        private:
            Tasks::Tasks task;
            RobotInterface::RobotInterface* robotInterface;

        public:
            UserInterface(RobotInterface::RobotInterface* RI) : robotInterface(RI) {};
            ~UserInterface(){ delete robotInterface; };

            int DisplayMenu();
            void ParseCommand(int);
            bool VerifyInput(int, const char*);
    };
};


#endif // USER_INTERFACE_H
