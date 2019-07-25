project(custom_resolver)

cmake_minimum_required(VERSION 3.1)

list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_SOURCE_DIR}/cmake")

find_package(USD REQUIRED)

set(CMAKE_CXX_STANDARD 11)

# TODO : Remove this later
set(USD_ROOT_DIR /usr/local/USD-19.07)
set(USD_LIB_DIR ${USD_ROOT_DIR}/lib)
set(USD_INC_DIR ${USD_ROOT_DIR}/include)

# Make compile_commands.json in the build directory (useful for linter tools)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(-Wno-deprecated)
# add_compile_options(-Wall -DBUILD_OPTLEVEL_OPT -DBUILD_COMPONENT_SRC_PREFIX="")

add_subdirectory(src)
