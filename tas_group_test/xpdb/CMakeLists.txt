cmake_minimum_required(VERSION 2.8)

include(../cmake_common/publish.cmake)
include(../cmake_common/export.cmake)

project(xpdb_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

set(INTERFACE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/interface_headers)

# -------------------- ADD LIB --------------------------------------
add_library(xpdb STATIC ${SOURCE_FILES} ${HEADER_FILES})

target_include_directories(xpdb PRIVATE "${INTERFACE_HEADERS}/xpdb")
target_include_directories(xpdb INTERFACE "${INTERFACE_HEADERS}")

target_link_libraries(xpdb utils)

set_property(TARGET xpdb PROPERTY FOLDER xpdb)

export_headers("xpdb" "xpdb")
