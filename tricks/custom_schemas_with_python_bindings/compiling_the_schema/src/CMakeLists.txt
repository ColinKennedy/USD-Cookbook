# 4. Include/Link Everything
add_library(${USDPLUGIN_NAME}
    SHARED
        api.h
        complex.cpp
        complex.h
        paramsAPI.cpp
        paramsAPI.h
        simple.cpp
        simple.h
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
find_library(USD_USD usd HINTS ${USD_LIBRARY_DIRECTORY})

target_link_libraries(${USDPLUGIN_NAME}
    ${USD_USD}
)

set_target_properties(${USDPLUGIN_NAME} PROPERTIES PREFIX "")

target_compile_features(${USDPLUGIN_NAME}
    PUBLIC
        cxx_auto_type
)

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

set(USDPLUGIN_TARGETS_NAME TestoutTargets)
set(INSTALL_CONFIGURATION_DIRECTORY lib/cmake/TestoutSchemas)

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
    NAMESPACE testout::
    DESTINATION ${INSTALL_CONFIGURATION_DIRECTORY}
)

# 6. Create a Config.cmake file so that other C++ projects can use
# `find_package` to get the namespace that was exported in step #5
#
# Reference: https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right
#
include(CMakePackageConfigHelpers)

configure_package_config_file(${CMAKE_CURRENT_LIST_DIR}/cmake/TestoutConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/TestoutConfig.cmake
    INSTALL_DESTINATION ${INSTALL_CONFIGURATION_DIRECTORY}
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/TestoutConfig.cmake
    DESTINATION ${INSTALL_CONFIGURATION_DIRECTORY}
)

# XXX : We don't need to create a ConfigVersion.cmake
# file for this example. But if we did, we could use
# `write_basic_package_version_file` to do it, here.
#
# Reference: https://github.com/pabloariasal/modern-cmake-sample/blob/master/libjsonutils/CMakeLists.txt#L70-L74

# 7. Copy the schema header files so that other C++ projects can include them
#
# XXX : We need to install header files into an include directory.
# Otherwise, client C++ projects that include `testout::testout` will
# get this error when they try to run the `cmake` command:
#
# CMake Error in CMakeLists.txt:
#
#     Imported target "testout::testout" includes non-existent path
#
#     "/home/selecaoone/projects/usd_experiments/examples/tricks/custom_schemas_with_python_bindings/compiling_the_schema/build/install/include"
#
#     in its INTERFACE_INCLUDE_DIRECTORIES.  Possible reasons include: ...
#
install(
    FILES
        api.h
        complex.h
        paramsAPI.h
        simple.h
        tokens.h
    DESTINATION
        include
)

# 6. Add Python bindings for the schema plugin
set(USDPLUGIN_PYTHON_NAME _${USDPLUGIN_NAME})
set(MODULE_NAME Testout)

add_library(${USDPLUGIN_PYTHON_NAME}
    SHARED
        module.cpp
        moduleDeps.cpp
        wrapTokens.cpp
        wrapSimple.cpp
        wrapComplex.cpp
        wrapParamsAPI.cpp
)

# XXX : This line is critical. Without it, the Python binding will not
# see testout.so and you'll get an ImportError when you try to import
# _testout.so, like this:
#
# `ImportError: testout.so: cannot open shared object file: No such file or directory`
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
        MFB_PACKAGE_MODULE=testout.${MODULE_NAME}
)

target_link_libraries(${USDPLUGIN_PYTHON_NAME}
    ${USDPLUGIN_NAME}
)

set(PYTHON_PACKAGE_RELATIVE_PATH lib/python2.7/site-packages/testout)
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
