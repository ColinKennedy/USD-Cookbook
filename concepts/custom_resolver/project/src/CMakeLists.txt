# 4. Include/Link everything
set(PLUGIN_NAME URIResolver)

link_directories(${USD_LIBRARY_DIR})


set(
	SRC
		resolver.cpp
)

add_library(${PLUGIN_NAME}
    SHARED
		${SRC}
)

find_package(PythonLibs REQUIRED)

target_link_libraries(${PLUGIN_NAME}
    PUBLIC

		libboost_python.so
		libar.so
)

target_include_directories(
	${PLUGIN_NAME}
		SYSTEM
			PRIVATE
				${USD_INCLUDE_DIR}

			PUBLIC
				${PYTHON_INCLUDE_PATH}
)

install(
    TARGETS
        ${PLUGIN_NAME}
	DESTINATION
		.
)

install(
    FILES
		plugInfo.json
    DESTINATION
        ./resources
)
