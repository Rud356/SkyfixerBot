try:
    import uvloop  # noqa: this is a speedup for unix os
    uvloop.install()

except ImportError:
    pass
