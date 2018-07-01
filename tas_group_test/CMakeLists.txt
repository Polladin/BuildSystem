cmake_minimum_required(VERSION 2.8)

project(Telephony)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

set(IMPORTED_LIB_BY_SOURCES ${CMAKE_BINARY_DIR}/import)
set(SOURCES_FOR_DEPENDENCY_PROJECTS ${CMAKE_SOURCE_DIR})
set(PUBLISH_LIBS ${CMAKE_BINARY_DIR}/publish)

set(DIRECTORY_WITH_LIBS ${IMPORTED_LIB_BY_SOURCES}/libs)


# Imported params
set(IMPORT_HEADERS_DIR  ${CMAKE_BINARY_DIR}/import/headers)
set(IMPORT_LIBS_DIR     ${CMAKE_BINARY_DIR}/import/libs)

set(PUBLISH_FOLDER		${CMAKE_BINARY_DIR}/export)
file(MAKE_DIRECTORY 	${PUBLISH_FOLDER} ${IMPORT_HEADERS_DIR})

# ------------------- LIBRARY OUTPUT ----------------------------------
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${IMPORT_LIBS_DIR})

# ----------- Add subdirectory with projects to build from source --------------
foreach(src_name IN LISTS WITH_SOURCES)
    
    add_subdirectory(${SOURCES_FOR_DEPENDENCY_PROJECTS}/${src_name} ${IMPORTED_LIB_BY_SOURCES}/${src_name})
    
endforeach(src_name)
