get_filename_component(CUSTOM_SCHEMAS_DIRECTORY "${CMAKE_CURRENT_LIST_FILE}" PATH)

find_package(PythonLibs REQUIRED)

if(NOT TARGET star::star)
    include("${CUSTOM_SCHEMAS_DIRECTORY}/StarTargets.cmake")
endif()
