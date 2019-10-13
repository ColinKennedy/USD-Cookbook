# Quick Reference
### C++
#### Tracing

```cpp
void do_some_function_that_has_trace_enabled()
{
    TRACE_FUNCTION();
	// ...
    {
        TRACE_SCOPE("Inner Scope");
		// ... This scope is optional. It just helps keep trace results organized
	}
	// ...
}
```


#### Collecting / Reporting
```cpp
auto reporter = pxr::TraceReporter::GetGlobalReporter();

auto* collector = &pxr::TraceCollector::GetInstance();
collector->SetEnabled(true);
do_some_function_that_has_trace_enabled();
collector->SetEnabled(false);

reporter->Report(std::cout);
reporter->ReportTimes(std::cout);
std::ofstream outfile("report.json");
reporter->ReportChromeTracing(outfile);

// Optional clean-up
collector->Clear();
reporter->ClearTree();
```

### Python
#### Tracing
```python
@Trace.TraceFunction
def create_sdf_primspecs_normally():
	# ...
    with Trace.TraceScope("Inner Scope"):
		# ... This context is optional. It just helps keep trace results organized
	# ...
```


#### Collecting / Reporting
```python
reporter = Trace.Reporter.globalReporter  # This is a singleton object

collector = Trace.Collector()
collector.enabled = True
do_some_function_that_has_trace_enabled()
collector.enabled = False

reporter.Report()
reporter.ReportTimes()
reporter.ReportChromeTracingToFile("/tmp/some/report.json")

# Optional clean-up
collector.Clear()
reporter.ClearTree()
```


## Viewing A Report In Google Chrome
- Open Chrome
- Type "chrome://tracing" in the address bar
- Click the "Load" button
- Add the report.json that this project comes with or load your own file
- You should see a report on-screen that looks like this

![image](https://user-images.githubusercontent.com/10103049/66624613-ba587000-eba5-11e9-84f4-d895cb14b3ac.png)


## Scoping
TRACE_SCOPE seems to only be for organizational purposes and has no
other effect on tracing (aside its overhead).


## Things To Remember
TraceReporter is a singleton. You can use it to create reports anywhere
in your code. It also accumulates collected data. So if you want to
get the report of an individual function, it's best to clear out the
data before collecting any more. Otherwise, the report will show timing
information that doesn't come from the function that you're trying to
test.

`TraceReporter::Report` and `TraceReporter::ReportTimes` both get timing
information. `TraceReporter::ReportChromeTracing` is used to view
detailed, per-thread information about the called functions.


```

Each TraceEvent contains a TraceCategoryId. These ids allow for the events to be filtered. Events recorded by TRACE_ macros have their TraceCategoryId set to TraceCategory::Default.


Access to recorded TraceEvent objects is available through the TraceCollection class and TraceCollectionAvailable notice. When the TraceCollector produces data through the TraceCollector::CreateCollection() method, it will send a TraceCollectionAvailable notice. To access individual events in a TraceCollection instance, the TraceCollection::Visitor interface can be used. The TraceReporterBase class encapsulates logic for handling TraceCollectionAvailable notices.

```
