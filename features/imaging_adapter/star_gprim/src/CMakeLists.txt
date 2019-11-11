# 4. Include/Link Everything
add_library(${USDPLUGIN_NAME}
    SHARED
        api.h
        star.cpp
        star.h
        tokens.cpp
        tokens.h
)

set(USD_INCLUDE_DIRECTORY $ENV{USD_INSTALL_ROOT}/include)

target_include_directories(${USDPLUGIN_NAME}
    PRIVATE
        ${PYTHON_INCLUDE_PATH}
        ${USD_INCLUDE_DIRECTORY}
)

set(USD_LIBRARY_DIRECTORY $ENV{USD_INSTALL_ROOT}/lib)
find_library(USD_TF tf HINTS ${USD_LIBRARY_DIRECTORY})
find_library(USD_USD usd HINTS ${USD_LIBRARY_DIRECTORY})
find_library(USD_USDGEOM usdGeom HINTS ${USD_LIBRARY_DIRECTORY})

target_link_libraries(${USDPLUGIN_NAME}
    ${USD_TF}
    ${USD_USDGEOM}
    ${USD_USD}
)

set_target_properties(${USDPLUGIN_NAME} PROPERTIES PREFIX "")

configure_file(
    plugInfo.json
    ${CMAKE_BINARY_DIR}/plugInfo.json
    @ONLY)

install(
    TARGETS ${USDPLUGIN_NAME}
    LIBRARY DESTINATION plugin/usd
)

install(
    FILES ${CMAKE_BINARY_DIR}/plugInfo.json
    DESTINATION plugin/usd/${USDPLUGIN_NAME}/resources
)

set(USDPLUGIN_TARGETS_NAME StarTargets)
set(INSTALL_CONFIGURATION_DIRECTORY lib/cmake/StarSchemas)

# 5. Export a namespace for this library so other C++ projects can use it
# Reference: https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right/
#
install(
    TARGETS ${USDPLUGIN_NAME}
    EXPORT ${USDPLUGIN_TARGETS_NAME}
    LIBRARY DESTINATION lib
    INCLUDES DESTINATION include
)

install(
    EXPORT ${USDPLUGIN_TARGETS_NAME}
    FILE ${USDPLUGIN_TARGETS_NAME}.cmake
    NAMESPACE star::
    DESTINATION ${INSTALL_CONFIGURATION_DIRECTORY}
)

# 6. Create a Config.cmake file so that other C++ projects can use
# `find_package` to get the namespace that was exported in step #5
#
# Reference: https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right
#
include(CMakePackageConfigHelpers)

configure_package_config_file(${CMAKE_CURRENT_LIST_DIR}/cmake/StarConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/StarConfig.cmake
    INSTALL_DESTINATION ${INSTALL_CONFIGURATION_DIRECTORY}
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/StarConfig.cmake
    DESTINATION ${INSTALL_CONFIGURATION_DIRECTORY}
)

install(
    FILES
        star.h
        tokens.h
    DESTINATION
        include
)

# 6. Add Python bindings for the schema plugin
set(USDPLUGIN_PYTHON_NAME _${USDPLUGIN_NAME})
set(MODULE_NAME Star)

add_library(${USDPLUGIN_PYTHON_NAME}
    SHARED
        module.cpp
        moduleDeps.cpp
        wrapTokens.cpp
		wrapStar.cpp
)

# XXX : This line is critical. Without it, the Python binding will not
# see star.so and you'll get an ImportError when you try to import
# _star.so, like this:
#
# `ImportError: star.so: cannot open shared object file: No such file or directory`
#
# Make sure this path is always correct when building
#
set_target_properties(${USDPLUGIN_PYTHON_NAME}
  PROPERTIES
  INSTALL_RPATH "$ORIGIN/../../../../../plugin/usd"
)

target_include_directories(${USDPLUGIN_PYTHON_NAME}
    PRIVATE
        ${PYTHON_INCLUDE_PATH}
        ${USD_INCLUDE_DIRECTORY}
)

# On OSX "dylib" does not work to import python module
# TODO: windows support
set_target_properties(${USDPLUGIN_PYTHON_NAME} PROPERTIES SUFFIX ".so")

set_target_properties(${USDPLUGIN_PYTHON_NAME}
    PROPERTIES
        PREFIX ""
)

# XXX : These lines "find" the Python package
target_compile_definitions(${USDPLUGIN_PYTHON_NAME}
    PRIVATE
        MFB_PACKAGE_NAME=${USDPLUGIN_NAME}
        MFB_ALT_PACKAGE_NAME=${USDPLUGIN_NAME}
        MFB_PACKAGE_MODULE=star.${MODULE_NAME}
)

target_link_libraries(${USDPLUGIN_PYTHON_NAME}
    ${USDPLUGIN_NAME}
)

set(PYTHON_PACKAGE_RELATIVE_PATH lib/python2.7/site-packages/star)
set(INSTALL_PYTHONPACKAGE_DIR  ${PYTHON_PACKAGE_RELATIVE_PATH})
set(INSTALL_WRAPPER_DIR ${INSTALL_PYTHONPACKAGE_DIR}/${MODULE_NAME})

install(
    TARGETS ${USDPLUGIN_PYTHON_NAME}
    DESTINATION ${INSTALL_WRAPPER_DIR}
)

install(
    FILES __packageinit__.py
    DESTINATION ${INSTALL_PYTHONPACKAGE_DIR}
    RENAME __init__.py
)

install(
    FILES __init__.py
    DESTINATION ${INSTALL_WRAPPER_DIR}
)
