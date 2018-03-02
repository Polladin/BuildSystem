cmake_minimum_required(VERSION 2.8)

project(%PROJECT_NAME%)

# ------------------- SOURCES ------------------------------------------
file(GLOB HEADER_FILES          src/*.h)
file(GLOB SOURCE_FILES          src/*.cpp)

message(STATUS "Header files : ${HEADER_FILES}")
message(STATUS "Source files : ${SOURCE_FILES}")

# -------------------- ADD LIB --------------------------------------
add_library(%LIB_NAME% STATIC ${SOURCE_FILES} ${HEADER_FILES})

%TARGET_LINK_LIBRARIES%

set_property(TARGET %LIB_NAME% PROPERTY FOLDER %PROJECT_FOLDER_NAME%)
