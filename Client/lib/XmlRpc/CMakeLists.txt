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
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpc.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcClient.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcDispatch.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcException.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcServer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcServerConnection.h 
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcServerMethod.h 
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcSocket.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcSource.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcUtil.h 
    ${CMAKE_CURRENT_SOURCE_DIR}/include/XmlRpcValue.h
    ${CMAKE_CURRENT_SOURCE_DIR}/include/base64.h
)

set(SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcClient.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcDispatch.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcServer.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcServerConnection.cpp 
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcServerMethod.cpp 
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcSocket.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcSource.cpp 
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcUtil.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/XmlRpcValue.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
)

add_library(${PROJECT_NAME} SHARED ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
