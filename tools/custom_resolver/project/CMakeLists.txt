# 1. Requirements
project(custom_resolver)
cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # This line is optional. It's just for certain IDEs to use

# 2.Configuration
list(INSERT CMAKE_MODULE_PATH 0 "${CMAKE_SOURCE_DIR}/cmake")
set(CMAKE_INSTALL_PREFIX "./install" CACHE PATH "..." FORCE)
add_compile_options(-Wno-deprecated)  # This is just to avoid some spammy warnings

# 3. Boilerplate
find_package(USD REQUIRED)

add_subdirectory(src)
