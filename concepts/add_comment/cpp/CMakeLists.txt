cmake_minimum_required(VERSION 2.8.11)

project(add_comment)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "-Wno-deprecated ${CMAKE_CXX_FLAGS}")

# Make compile_commands.json in the build directory (useful for linter tools)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(USD_ROOT_DIR $ENV{USD_INSTALL_ROOT})
set(USD_INC_DIR ${USD_ROOT_DIR}/include)

link_directories($ENV{USD_INSTALL_ROOT}/lib)

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
	boost_python
	sdf
	tf
	usd
	usdGeom
	vt
)
