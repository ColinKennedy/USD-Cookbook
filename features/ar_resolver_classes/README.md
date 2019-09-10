


# - The order of the resolver context determines the resolve order of paths
# - it does not affect resolves with USD files in a stage though. Probably because stages have their own scopedcontext / resolvercontext built internally
# - if you want a proper remapper, you'd need to write a custom resolver (such as rdo_replace_resolver or a resolver that (at minimum) reads environment variables)


# TODO :
# Check if AR resolver cache can get back the cached paths
# Check if there's any speed different loading the same stage repeatedly this way
# ar "package-relative-path?"
