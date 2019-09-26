/*
 * A file that demonstrates the power of `pxr::ArResolverScopedCache`.
 *
 * Example:
 *    This first function run will be slowly because it isn't cached.
 *    Function was called "100000" times and took 306591 microseconds
 *    Now run the same function, this time with caching.
 *    Function was called "100000" times and took 20893 microseconds
 */


// IMPORT STANDARD LIBRARIES
#include <chrono>
#include <functional>
#include <string>

// IMPORT THIRD-PARTY LIBRARIES
#include <pxr/usd/ar/resolver.h>
#include <pxr/usd/ar/resolverScopedCache.h>


void timeit(std::function<void ()> function, int repeats, std::string const &name) {
    using namespace std::chrono;

    auto start = high_resolution_clock::now();

    for (unsigned int index = 0; index < repeats; ++index) {
        function();
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    std::cout
        << "Function was called \"" << repeats
        << "\" times and took " << duration.count() << " "
        << "microseconds \n";
}


int main() {
    auto& resolver = pxr::ArGetResolver();
    auto function = [&resolver]() { resolver.Resolve("foo"); };

    std::cout << "This first function run will be slowly because it isn't cached.\n";
    timeit(function, 100000, "Resolve without cache");

    std::cout << "Now run the same function, this time with caching.\n";
    {
        pxr::ArResolverScopedCache cache;
        timeit(function, 100000, "Resolve with cache");
    }

    return 0;
}
