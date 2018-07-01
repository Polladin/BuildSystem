cmake_minimum_required(VERSION 2.8)

include(../cmake_common/publish.cmake)
include(../cmake_common/export.cmake)

project(utils_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

set(INTERFACE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/interface_headers)

# -------------------- ADD LIB --------------------------------------
add_library(utils STATIC ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(utils PRIVATE "${INTERFACE_HEADERS}/utils")
target_include_directories(utils INTERFACE "${INTERFACE_HEADERS}")

target_link_libraries(utils common_lib phoneparser)

set_property(TARGET utils PROPERTY FOLDER utils)

export_headers("utils" "utils")
