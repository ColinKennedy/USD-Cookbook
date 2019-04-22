cmake_minimum_required(VERSION 2.8.11)

project(variant_set_in_stronger_layer)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "-Wno-deprecated ${CMAKE_CXX_FLAGS}")

# Make compile_commands.json in the build directory (useful for linter tools)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(USD_ROOT_DIR /usr/local/USD-19.05)
set(USD_LIB_DIR ${USD_ROOT_DIR}/lib)
set(USD_INC_DIR ${USD_ROOT_DIR}/include)

add_executable(variant_set
	main.cpp
)

find_package(PythonLibs)

target_include_directories(variant_set
PUBLIC
	${USD_INC_DIR}
	${PYTHON_INCLUDE_PATH}
)

target_link_libraries(
variant_set
	${USD_LIB_DIR}/libboost_python.so
	${USD_LIB_DIR}/libusd.so
	${USD_LIB_DIR}/libusdGeom.so
	${USD_LIB_DIR}/libtf.so
	${USD_LIB_DIR}/libsdf.so
	${USD_LIB_DIR}/libvt.so
	${PYTHON_LIBRARY}
)
