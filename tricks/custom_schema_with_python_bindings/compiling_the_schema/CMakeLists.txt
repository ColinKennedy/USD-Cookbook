cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

project(test-out VERSION 0.1.0 LANGUAGES CXX)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)

set(CMAKE_INSTALL_PREFIX "./install" CACHE PATH "..." FORCE)

# 3. Boilerplate
set(USDPLUGIN_NAME testout)
find_package(USD REQUIRED)

add_subdirectory(src)
