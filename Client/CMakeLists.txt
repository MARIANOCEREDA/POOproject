cmake_minimum_required(VERSION 3.18)

project(
    "RobotXMLRPCClient"
    VERSION 1.0.0
    LANGUAGES C CXX)

# Global CMake variables are set here
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


option(ENABLE_DOC "Create Doxygen Documentation" ON)

include_directories(
    ${CMAKE_SOURCE_DIR}/lib/XmlRpc
    ${CMAKE_SOURCE_DIR}/src/include
)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/")

if (ENABLE_DOC)
    include(Docs)
endif()

add_subdirectory(lib/XmlRpc)
add_subdirectory(src)
