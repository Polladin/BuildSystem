cmake_minimum_required(VERSION 2.8)

project(common_net_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

message(STATUS "Header files : ${HEADER_FILES}")
message(STATUS "Source files : ${SOURCE_FILES}")

# -------------------- ADD LIB --------------------------------------
add_library(common_net STATIC ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(common_net PRIVATE "${INTERFACE_HEADERS}/${MODULE_PATH}/common_net")
target_include_directories(common_net INTERFACE "${INTERFACE_HEADERS}")

set_property(TARGET common_net PROPERTY FOLDER common)

# ------------------ PUBLISH -------------------------------------
#publish_target("common_net")
add_lib_to_publish("common_net")
string(CONCAT LIBS_TO_PUBLISH "${LIBS_TO_PUBLISH}" "common_net;")
