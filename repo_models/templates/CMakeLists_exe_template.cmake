cmake_minimum_required(VERSION 2.8)

project(%PROJECT_NAME%)


set(IMPORTED_LIB_BY_SOURCES ${CMAKE_BINARY_DIR}/import)
set(SOURCES_FOR_DEPENDENCY_PROJECTS ${CMAKE_SOURCE_DIR}/..)

set(LIBRARY_OUTPUT_DIRECTORY ${IMPORTED_LIB_BY_SOURCES}/libs)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${IMPORTED_LIB_BY_SOURCES}/libs)

# Include api by sources
%INCLUDE_SUBDIRECTORY%

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

message(STATUS "Header files : ${HEADER_FILES}")
message(STATUS "Source files : ${SOURCE_FILES}")


# -------------------- ADD FOLDER TO FIND LIBS ----------------------
link_directories(${LIBRARY_OUTPUT_DIRECTORY})

# -------------------- ADD TARGET --------------------------------------
add_executable(%TARGET% ${SOURCE_FILES} ${HEADER_FILES})

# -------------------- ADD FOLDER WITH LIBS INCLUDES -----------------
%TARGET_INCLUDE_DIRS%

# -------------------- LINKING --------------------------------------
target_link_libraries(%TARGET% %LINKED_LIBS%)
