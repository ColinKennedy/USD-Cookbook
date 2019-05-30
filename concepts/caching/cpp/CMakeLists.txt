cmake_minimum_required(VERSION 3.10)
project(usd_cacheing)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(
    Main_SRCS
	    main.cpp
)

include_directories(${CMAKE_SOURCE_DIR})
add_executable(usd_cacheing ${Main_SRCS})

install(TARGETS usd_cacheing DESTINATION bin)
