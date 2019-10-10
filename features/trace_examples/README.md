- C++ trace
- C++ trace scope
-- Python trace
-- Python trace scope

- Getting trace overhead
- report using Chrome

TRACE_SCOPE seems to only be for organizational purposes and has no
other effect on tracing (aside its overhead).


## Viewing A Report In Google Chrome
- Instructions here
- Provide an example report for people to load + view


## Things To Remember
If you want the TraceReporter to accumulate timing information across
multiple functions, you can call `TraceReporter::Report` repeatedly.
But if you want to test a function in-isolation, you need to run
`TraceReporter::ClearTree` first. Otherwise, old collected data will be
included in the final output.

`TraceReporter::Report` and `TraceReporter::ReportTimes` both get timing
information. `TraceReporter::ReportChromeTracing` is used to view
detailed, per-thread information about the called functions.


```

Each TraceEvent contains a TraceCategoryId. These ids allow for the events to be filtered. Events recorded by TRACE_ macros have their TraceCategoryId set to TraceCategory::Default.


Access to recorded TraceEvent objects is available through the TraceCollection class and TraceCollectionAvailable notice. When the TraceCollector produces data through the TraceCollector::CreateCollection() method, it will send a TraceCollectionAvailable notice. To access individual events in a TraceCollection instance, the TraceCollection::Visitor interface can be used. The TraceReporterBase class encapsulates logic for handling TraceCollectionAvailable notices.

```
