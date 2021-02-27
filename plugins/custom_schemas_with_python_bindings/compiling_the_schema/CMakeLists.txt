# 1. Requirements
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(test-out VERSION 0.1.0 LANGUAGES CXX)

# 2.Configuration
set(CMAKE_INSTALL_PREFIX "./install" CACHE PATH "..." FORCE)

# 3. Boilerplate
set(USDPLUGIN_NAME testout)
find_package(PythonLibs 2.7 REQUIRED)  # Needed for `PYTHON_INCLUDE_PATH`
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)

add_subdirectory(src)
