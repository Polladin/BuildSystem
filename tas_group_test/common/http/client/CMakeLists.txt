cmake_minimum_required(VERSION 2.8)

project(client_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

message(STATUS "Header files : ${HEADER_FILES}")
message(STATUS "Source files : ${SOURCE_FILES}")

# -------------------- ADD LIB --------------------------------------
add_library(client STATIC ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(client PRIVATE "${INTERFACE_HEADERS}/${MODULE_PATH}/client")
target_include_directories(client INTERFACE "${INTERFACE_HEADERS}")

set_property(TARGET client PROPERTY FOLDER common)

# ------------------ PUBLISH -------------------------------------
#publish_target("client")
add_lib_to_publish("client")
