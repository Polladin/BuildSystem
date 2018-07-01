cmake_minimum_required(VERSION 2.8)

project(libTCPPinger_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

message(STATUS "Header files : ${HEADER_FILES}")
message(STATUS "Source files : ${SOURCE_FILES}")

# -------------------- ADD LIB --------------------------------------
add_library(libTCPPinger STATIC ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(libTCPPinger PRIVATE "${INTERFACE_HEADERS}/${MODULE_PATH}/libTCPPinger")
target_include_directories(libTCPPinger INTERFACE "${INTERFACE_HEADERS}")

set_property(TARGET libTCPPinger PROPERTY FOLDER common)

add_lib_to_publish("libTCPPinger")
