#include <iostream>
#include <thread>

#include "RobotInterface.h"
#include "CustomExceptions.h"
#include "Tasks.h"
#include <mutex>
#include <queue>
#include <condition_variable>
#include <atomic>
#include <chrono>

#if !defined(USER_INTERFACE_H)
#define USER_INTERFACE_H

namespace UserInterface
{
    class UserInterface
    {
        private:
            Tasks::Tasks task;
            std::shared_ptr<RobotInterface::RobotInterface> robotInterface;
            bool exitRequested = false;

            std::mutex queueMutex;
            std::mutex inputMutex;
            std::mutex coutMutex;
            std::mutex robotOperation;

            std::shared_ptr<std::thread> inputThread;
            std::shared_ptr<std::thread> writeThread;
            std::shared_ptr<std::thread> showInputSymbolThread;

            std::queue<int>  messageQueue;

            std::condition_variable  conditionVariable;
            std::condition_variable  robotOperationFinishedConditional;
            std::atomic<bool>        initialized;
            std::atomic<bool>        stopLoops;
            bool                     robotTaskFinished;

            // Robot Data
            std::vector<int> joints;
            XmlRpc::XmlRpcValue noArgs, result, oneArg, args;

            void DisplayMenu();
            void ParseCommand();
            bool VerifyInput(int, const char*);
            void Initialize();
            void Terminate();
            void InputLoop();

        public:
            UserInterface(std::shared_ptr<RobotInterface::RobotInterface> RI) : robotInterface(RI), robotTaskFinished(true){};
            ~UserInterface(){};

            void run();
    };
};


#endif // USER_INTERFACE_H
