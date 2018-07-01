
#
#
function (publish_to_archive archive_name from_folder files_to_archive depends_for_publish)

	if (DEFINED PUBLISH_FOLDER)

#		add_custom_command(TARGET common_lib POST_BUILD
#			COMMAND ${CMAKE_COMMAND} -E chdir "${from_folder}"
#					${CMAKE_COMMAND} -E tar "cfv" "${PUBLISH_FOLDER}/${archive_name}" --format=zip
#											"${files_to_archive}")	

		string(CONCAT TARGET_NAME_TO_PUBLISH "publish_" "${archive_name}")
		
		message(STATUS "archive_name : ${archive_name}")
		message(STATUS "from_folder : ${from_folder}")
		message(STATUS "PUBLISH : ${files_to_archive}")
		message(STATUS "depends_for_publish : ${depends_for_publish}")
		
		add_custom_target(${TARGET_NAME_TO_PUBLISH} ALL 
			COMMAND ${CMAKE_COMMAND} -E chdir "${from_folder}"
					${CMAKE_COMMAND} -E tar "cfv" "${PUBLISH_FOLDER}/${archive_name}" --format=zip --
											${files_to_archive}
			DEPENDS ${depends_for_publish})
		
	endif()

endfunction()

#
#
function (export_lib_files module_name files_to_archive)

	if (DEFINED PUBLISH_FOLDER)

		add_custom_command(TARGET ${module_name} POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E chdir "${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/Debug"
					${CMAKE_COMMAND} -E tar "cfv" "${PUBLISH_FOLDER}/${module_name}.zip" --format=zip
											"${files_to_archive}")	
	endif()

endfunction()

#
#
function (export_header_files module_name)

	if (DEFINED PUBLISH_FOLDER)

		add_custom_command(TARGET ${module_name} POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E chdir "${CMAKE_CURRENT_SOURCE_DIR}"
					${CMAKE_COMMAND} -E tar "cfv" "${PUBLISH_FOLDER}/${module_name}_headers.zip" --format=zip
											"headers")	
	endif()

endfunction()

#
#
function (publish_target target_name)
	
	export_lib_files("${target_name}" "${target_name}.lib")
	#export_header_files("${target_name}")
	
endfunction()

#
#
function (add_lib_to_publish lib_name)
	
	string(CONCAT LIBS_TO_PUBLISH "${LIBS_TO_PUBLISH}" "${lib_name} ;")

endfunction()


#
#
function (publish_libs)
	
	message(STATUS ">>> INSTALL : ${LIBS_TO_PUBLISH}")

endfunction()