cmake_minimum_required(VERSION 2.8)

include(../cmake_common/publish.cmake)

project(tas_project)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(IMPORTED_LIB_BY_SOURCES ${CMAKE_BINARY_DIR}/import)
set(SOURCES_FOR_DEPENDENCY_PROJECTS ${CMAKE_SOURCE_DIR}/..)

set(LIBRARY_OUTPUT_DIRECTORY ${IMPORTED_LIB_BY_SOURCES}/libs)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${IMPORTED_LIB_BY_SOURCES}/libs)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

message(STATUS "Header files : ${HEADER_FILES}")
message(STATUS "Source files : ${SOURCE_FILES}")


# -------------------- ADD FOLDER TO FIND LIBS ----------------------
link_directories(${LIBRARY_OUTPUT_DIRECTORY})

# -------------------- ADD TARGET --------------------------------------
add_executable(tas ${SOURCE_FILES} ${HEADER_FILES})

# -------------------- ADD FOLDER WITH LIBS INCLUDES -----------------
target_include_directories(tas PUBLIC ${IMPORT_HEADERS_DIR})

# -------------------- LINKING --------------------------------------
target_link_libraries(tas common_lib xpdb phoneparser common_net client server libTCPPinger)


add_custom_command(TARGET tas 
                   POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:tas> ${PUBLISH_LIBS})
