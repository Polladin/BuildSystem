cmake_minimum_required(VERSION 2.8)

include(../cmake_common/publish.cmake)
include(../cmake_common/export.cmake)

project(common_lib_project)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

set(INTERFACE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/interface_headers)

# -------------------- ADD LIB --------------------------------------
add_library(common_lib STATIC ${SOURCE_FILES} ${HEADER_FILES})

# -------------------- INCLUDE --------------------------------------
target_include_directories(common_lib PRIVATE "${INTERFACE_HEADERS}/common_lib")
target_include_directories(common_lib INTERFACE "${INTERFACE_HEADERS}")

# ------------------ SET FOLDER STRUCTURAL IN IDE ------------------------
set_property(TARGET common_lib PROPERTY FOLDER common_lib)

# ------------------ PUBLISH -------------------------------------
publish_to_archive("common_lib.zip"
				   "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/Debug"
				   "common_lib.lib"
				   "common_lib")

#publish_to_archive("common_lib_headears.zip"
#				   "${CMAKE_CURRENT_SOURCE_DIR}"
#				   "headers" )

