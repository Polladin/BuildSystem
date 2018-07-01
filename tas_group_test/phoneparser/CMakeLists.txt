cmake_minimum_required(VERSION 2.8)

include(../cmake_common/publish.cmake)
include(../cmake_common/export.cmake)

project(phoneparser_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

set(INTERFACE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/interface_headers)

# -------------------- ADD LIB --------------------------------------
add_library(phoneparser STATIC ${SOURCE_FILES} ${HEADER_FILES})

# -------------------- INCLUDE --------------------------------------
target_include_directories(phoneparser PRIVATE "${INTERFACE_HEADERS}/phoneparser")
target_include_directories(phoneparser INTERFACE "${INTERFACE_HEADERS}")

# ------------------ SET FOLDER STRUCTURAL IN IDE ------------------------
set_property(TARGET phoneparser PROPERTY FOLDER phoneparser)

export_headers("phoneparser" "phoneparser")