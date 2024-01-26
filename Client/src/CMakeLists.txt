set(HEADER_FILES
    ${CMAKE_SOURCE_DIR}/src/include/RobotInterface.h
    ${CMAKE_SOURCE_DIR}/src/include/UserInterface.h
    ${CMAKE_SOURCE_DIR}/src/include/Tasks.h
    ${CMAKE_SOURCE_DIR}/src/include/CustomExceptions.h
)

set(SOURCE_FILES
    ${CMAKE_SOURCE_DIR}/src/main.cpp
    ${CMAKE_SOURCE_DIR}/src/RobotInterface.cpp
    ${CMAKE_SOURCE_DIR}/src/UserInterface.cpp
)

add_executable(${PROJECT_NAME} ${SOURCE_FILES} ${HEADER_FILES})

target_link_libraries(${PROJECT_NAME} PUBLIC XMLRPC)