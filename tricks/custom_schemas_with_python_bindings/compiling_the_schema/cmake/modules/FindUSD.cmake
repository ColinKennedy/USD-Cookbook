if(EXISTS $ENV{USD_INSTALL_ROOT}/pxrConfig.cmake)
	include($ENV{USD_INSTALL_ROOT}/pxrConfig.cmake)
	set(USD_PLUGINS_DIR $ENV{USD_INSTALL_ROOT}/plugin/usd)
	set(USD_PYTHONPATH $ENV{USD_INSTALL_ROOT}/lib/python)
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(USD
	DEFAULT_MSG
	PXR_INCLUDE_DIRS
	PXR_LIBRARIES
)
