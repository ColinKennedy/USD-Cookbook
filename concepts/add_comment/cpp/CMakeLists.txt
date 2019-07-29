cmake_minimum_required(VERSION 2.8.11)

project(add_comment)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "-Wno-deprecated ${CMAKE_CXX_FLAGS}")

# Make compile_commands.json in the build directory (useful for linter tools)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(USD_ROOT_DIR $ENV{USD_INSTALL_ROOT})
set(USD_INC_DIR ${USD_ROOT_DIR}/include)

find_library(USD_PYTHON boost_python HINTS $ENV{USD_INSTALL_ROOT}/lib)
find_library(USD_SDF sdf HINTS $ENV{USD_INSTALL_ROOT}/lib)
find_library(USD_TF tf HINTS $ENV{USD_INSTALL_ROOT}/lib)
find_library(USD_USD usd HINTS $ENV{USD_INSTALL_ROOT}/lib)
find_library(USD_USDGEOM usdGeom HINTS $ENV{USD_INSTALL_ROOT}/lib)
find_library(USD_VT vt HINTS $ENV{USD_INSTALL_ROOT}/lib)

add_executable(run_it
	main.cpp
)

find_package(PythonLibs)

target_include_directories(run_it
PUBLIC
	${USD_INC_DIR}
	${PYTHON_INCLUDE_PATH}
)

target_link_libraries(
run_it
	${PYTHON_LIBRARY}
	${USD_PYTHON}
	${USD_SDF}
	${USD_TF}
	${USD_USD}
	${USD_USDGEOM}
	${USD_VT}
)
