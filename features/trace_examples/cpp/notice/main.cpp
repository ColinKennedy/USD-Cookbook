#include "pxr/base/trace/collector.h"
#include "pxr/base/trace/reporterBase.h"
#include "pxr/base/trace/reporterDataSourceCollector.h"
#include <atomic>
#include <map>


PXR_NAMESPACE_USING_DIRECTIVE

// Custom Trace category.
struct CustomPerfCounterCategory
{
    // TraceCollector function calls using this category will store events with this TraceCategoryId.
    static constexpr TraceCategoryId GetId() {
        return TraceCategory::CreateTraceCategoryId("CustomPerfCounter");
    }
    // TraceCollector function calls using this category will store events only if this function return true.
    static bool IsEnabled() {
        return _isEnabled.load(std::memory_order_acquire);
    }
    static void Enable() {
        _isEnabled.store(true, std::memory_order_release);
    }
    static void Disable() {
        _isEnabled.store(false, std::memory_order_release);
    }
private:
    static std::atomic<bool> _isEnabled;
};
// Helper macros
#define CUSTOM_PERF_COUNTER(name, value) \
    _CUSTOM_PERF_COUNTER_INSTANCE(__LINE__, name, value)
#define _CUSTOM_PERF_COUNTER_INSTANCE(inst, name, value) \
    static constexpr TraceStaticKeyData customCounterKey ## inst (name); \
    TraceCollector::GetInstance().RecordCounterDelta<CustomPerfCounterCategory>(customCounterKey ## inst, value);

// Custom Trace reporter.
class CustomTraceEventProcessor :
    public TraceReporterBase, TraceCollection::Visitor {
public:
    CustomTraceEventProcessor(DataSourcePtr dataSource) : TraceReporterBase(std::move(dataSource)) {}
    void Update() {
        //Call base class update to get the latest data from TraceCollector.
        _Update();
    }
    // TraceCollection::Visitor interface
    // Only visit events marked with the custom category.
    virtual bool AcceptsCategory(TraceCategoryId id) override {
        return id == CustomPerfCounterCategory::GetId();
    }
    // Accumulate counter deltas.
    virtual void OnEvent(
        const TraceThreadId&, const TfToken& k, const TraceEvent& e) override {
        if (e.GetType() == TraceEvent::EventType::CounterDelta) {
            _counters[k] += e.GetCounterValue();
        }
    }
    virtual void OnBeginCollection() override {}
    virtual void OnEndCollection() override {}
    virtual void OnBeginThread(const TraceThreadId&) override {}
    virtual void OnEndThread(const TraceThreadId&) override {}
protected:
    // This will be called by the TraceReporterBase::_Update() for each
    // TraceCollection received.
    void _ProcessCollection(const CollectionPtr& collection) override {
        // Iterate over the TraceCollection using the TraceCollection::Visitor
        // interface.
        collection->Iterate(*this);
    }
    std::map<TfToken, double> _counters;
};
// Instrumented code
void Foo()
{
    CUSTOM_PERF_COUNTER("Foo Counter",1);
}
std::atomic<bool> CustomPerfCounterCategory::_isEnabled(false);
int main(int argc, char *argv[])
{
    // Register a name with the id.
    TraceCategory::GetInstance().RegisterCategory(
        CustomPerfCounterCategory::GetId(), "CustomPerfCounter");
    // Make sure an instance of the processor is available to receive notices.
    CustomTraceEventProcessor eventProcessor {
        TraceReporterDataSourceCollector::New()};
    // Enable the recording of events for the category.
    CustomPerfCounterCategory::Enable();
    // Call instrumented code.
    Foo();
    // Disable the recording of events for the category.
    CustomPerfCounterCategory::Disable();
    // Process the recorded events.
    eventProcessor.Update();
}
