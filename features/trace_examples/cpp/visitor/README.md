### Explanation For Why This Project Is Here
You may notice that this project basically just the example that Pixar
provides. It's added here though because the example doesn't compile
as-is. A few changes were made to get it to work

- `dataSource` was changed to a `DataSourcePtr` object, to match what TraceReporterBase expects.
- The TraceReporterBase constructor is called using `std::move(dataSource)` (to avoid a deleted constructor compiler error)
- Added a missing `#include "pxr/base/trace/reporterDataSourceCollector.h"` line
