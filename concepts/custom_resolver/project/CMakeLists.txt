# TODO finish this
project(custom_resolver)

cmake_minimum_required(VERSION 3.1)

list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_SOURCE_DIR}/cmake")

find_package(USD REQUIRED)

set(CMAKE_CXX_STANDARD 11)

# Make compile_commands.json in the build directory (useful for linter tools)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(-Wno-deprecated)  # This is just to avoid some spammy warnings

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
	set(CMAKE_INSTALL_PREFIX "./install" CACHE PATH "..." FORCE)
endif()

add_subdirectory(src)
