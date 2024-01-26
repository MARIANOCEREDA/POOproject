cmake_minimum_required(VERSION 3.18)

project(
    "XMLRPC"
    VERSION 1.0.0
    LANGUAGES C CXX)

# Global CMake variables are set here
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(HEADER_FILES
    XmlRpc.h
    XmlRpcClient.h
    XmlRpcDispatch.h
    XmlRpcException.h
    XmlRpcServer.h
    XmlRpcServerConnection.h 
    XmlRpcServerMethod.h 
    XmlRpcSocket.h
    XmlRpcSource.h
    XmlRpcUtil.h 
    XmlRpcValue.h
    base64.h
)

set(SOURCE_FILES
    XmlRpcClient.cpp
    XmlRpcDispatch.cpp
    XmlRpcServer.cpp
    XmlRpcServerConnection.cpp 
    XmlRpcServerMethod.cpp 
    XmlRpcSocket.cpp
    XmlRpcSource.cpp 
    XmlRpcUtil.cpp
    XmlRpcValue.cpp
    main.cpp
)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
