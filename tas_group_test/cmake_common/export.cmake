

function (export_headers target_name module_path)

	# execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink "${CMAKE_CURRENT_SOURCE_DIR}/headers" "${IMPORT_HEADERS_DIR}/${module_path}")
	 
	# message (STATUS ">>> ${IMPORT_HEADERS_DIR}/${module_path} ${CMAKE_CURRENT_SOURCE_DIR}/headers")
	# execute_process(COMMAND mklink "/D" "${IMPORT_HEADERS_DIR}/${module_path}" "${CMAKE_CURRENT_SOURCE_DIR}/headers")

	#file(GLOB HEADER_FILES_TO_EXPORT ${CMAKE_CURRENT_SOURCE_DIR}/headers/*.h)
    #
	#file(MAKE_DIRECTORY ${IMPORT_HEADERS_DIR}/${module_path})
	#
	#add_custom_command(TARGET ${target_name} PRE_BUILD 
	#						COMMAND ${CMAKE_COMMAND} -E copy ${HEADER_FILES_TO_EXPORT} 
	#														 ${IMPORT_HEADERS_DIR}/${module_path}/.
	#)

endfunction()