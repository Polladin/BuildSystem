cmake_minimum_required(VERSION 2.8)

include(../cmake_common/publish.cmake)
include(../cmake_common/export.cmake)

project(common_project)

set(MODULE_PATH "common")
set(INTERFACE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/interface_headers)
set(LIBS_TO_PUBLISH "")

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/common_net)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/http)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/libTCPPinger)


set(FILES_TO_EXPORT "common_net.lib;libTCPPinger.lib;client.lib;server.lib" )

set(DEPENDS_FOR_PUBLISH "common_net server client libTCPPinger")
			
publish_to_archive("common.zip"
				   "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/Debug"
				   "${FILES_TO_EXPORT}"
				   "${DEPENDS_FOR_PUBLISH}")
