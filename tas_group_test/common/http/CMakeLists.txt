cmake_minimum_required(VERSION 2.8)

project(http_project)

set(BU_MODULE_PATH "${MODULE_PATH}")
string(CONCAT MODULE_PATH "${MODULE_PATH}" "/http")

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/client)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/server)

set(MODULE_PATH "${BU_MODULE_PATH}")

