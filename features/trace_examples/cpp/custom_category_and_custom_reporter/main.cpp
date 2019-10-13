// IMPORT STANDARD LIBRARIES
#include <iostream>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/base/tf/notice.h>
#include <pxr/base/tf/refBase.h>
#include <pxr/base/tf/token.h>
#include <pxr/base/tf/weakBase.h>
#include <pxr/base/trace/category.h>
#include <pxr/base/trace/collection.h>
#include <pxr/base/trace/event.h>
#include <pxr/base/trace/reporter.h>
#include <pxr/base/trace/staticKeyData.h>
#include <pxr/base/trace/threads.h>
#include <pxr/base/trace/trace.h>
#include <pxr/usd/usd/stage.h>

PXR_NAMESPACE_USING_DIRECTIVE


// Declare a custom Trace category
struct PerfCategory {
    static constexpr pxr::TraceCategoryId GetId() {
        return pxr::TraceCategory::CreateTraceCategoryId("CustomPerfCounter");
    }
    static bool IsEnabled() { return pxr::TraceCollector::IsEnabled(); }
};


// XXX : Notice - this class does not inherit from `TraceReporterBase` or a subclass
TF_DECLARE_WEAK_AND_REF_PTRS(PerfReporter);
class PerfReporter :
    public TraceCollection::Visitor, public TfRefBase, public TfWeakBase  {
public:
    using self = PerfReporter;

    PerfReporter() {
        TfNotice::Register(TfCreateWeakPtr(this), &self::_OnCollection);
    }
    virtual bool AcceptsCategory(TraceCategoryId id) override {
        return id == PerfCategory::GetId();
    }

    virtual void OnEvent(
        const TraceThreadId&, const TfToken& k, const TraceEvent& e) override {
        if (e.GetType() != TraceEvent::EventType::CounterDelta) {
            return;
        }

        std::string key = k.GetString();
        CounterTable::iterator it = counters.find(key);
        if (it == counters.end()) {
            counters.insert({key, e.GetCounterValue()});
        } else {
            it->second += e.GetCounterValue();
        }
        printf("Perf counter event: %s %f\n", key.c_str(), e.GetCounterValue());
    }

    // Callbacks that are not used
    virtual void OnBeginCollection() override {}
    virtual void OnEndCollection() override {}
    virtual void OnBeginThread(const TraceThreadId&) override {}
    virtual void OnEndThread(const TraceThreadId&) override {}

    bool HasCounter(const std::string& key) const {
        return counters.find(key) != counters.end();
    }
    double GetCounterValue(const std::string& key) {
        return counters[key];
    }

private:
    void _OnCollection(const TraceCollectionAvailable& notice) {
        notice.GetCollection()->Iterate(*this);
    }

    using CounterTable = std::map<std::string, double>;
    CounterTable counters;
};


int main()
{
    auto* category = &pxr::TraceCategory::GetInstance();

    // Register a name with the id.
    pxr::TraceCategory::GetInstance().RegisterCategory(PerfCategory::GetId(), "CustomPerfCounter");
    // Record a counter delta event with the CustomPerfCounterCategory.
    auto* collector = &pxr::TraceCollector::GetInstance();
    // XXX : `reporter` must be created before
    //       `pxr::TraceCollector::CreateCollection` is called. Otherwise, it
    //       won't run `OnEvent`.
    //
    auto reporter = TfCreateRefPtr(new PerfReporter());

    constexpr static pxr::TraceStaticKeyData scope("TestScope");

    std::string first_counter {"first_counter"};
    // `second_counter` isn't used but is included for comparision
    std::string second_counter {"second_counter"};
    collector->SetEnabled(true);
    collector->BeginScope<PerfCategory>(scope);
    int value1 = 1;
    int value2 = 3;
    collector->RecordCounterDelta<PerfCategory>(first_counter, value1);
    collector->EndScope<PerfCategory>(scope);
    // XXX : Notice - since we don't implement any kind of scoping rule
    //       for our reporter, it doesn't matter if `RecordCounterDelta` is
    //       called inside of our scope. The end result will still print `4`
    //       (the combination of `value1` and `value2`).
    //
    collector->RecordCounterDelta<PerfCategory>(first_counter, value2);
    collector->CreateCollection();
    collector->SetEnabled(false);

    std::cout << std::boolalpha;
    std::cout << first_counter << " - has counter: " << reporter->HasCounter(first_counter) << '\n';
    std::cout << first_counter << ": " << reporter->GetCounterValue(first_counter) << '\n';
    std::cout
        << first_counter
        << " has a value of " << value1 + value2 << ": "
        << (reporter->GetCounterValue(first_counter) == value1 + value2)
        << '\n';
    std::cout << second_counter << " - has counter: " << reporter->HasCounter(second_counter) << '\n';
    std::cout << second_counter << ": " << reporter->GetCounterValue(second_counter) << '\n';
}
