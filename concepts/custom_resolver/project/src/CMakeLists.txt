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

find_package(PythonLibs)

target_link_libraries(${PLUGIN_NAME}
    PUBLIC

    ${PYTHON_LIBRARY}
    ${USD_LIB_DIR}/libboost_python.so
)

target_include_directories(
	${PLUGIN_NAME}
		SYSTEM
			PRIVATE

			"${USD_INCLUDE_DIR}"

        PUBLIC
            ${USD_INC_DIR}
            ${PYTHON_INCLUDE_PATH}
)

set(DESTINATION_INSTALL /home/selecaoone/projects/usd_experiments/examples/concepts/custom_resolver/project/build/testout)

install(
    TARGETS
        ${PLUGIN_NAME}
    DESTINATION
        ${DESTINATION_INSTALL}
)

install(
    FILES
		plugInfo.json
    DESTINATION
        ${DESTINATION_INSTALL}/resources/
)

# install(
#     FILES
# 		README.md
#     DESTINATION
# 		docs
# )
