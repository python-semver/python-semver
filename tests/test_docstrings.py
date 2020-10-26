import inspect

import pytest

import semver


def getallfunctions(module=semver):
    def getfunctions(_module):
        for _, func in inspect.getmembers(_module, inspect.isfunction):
            # Make sure you only investigate functions from our modules:
            if not func.__name__.startswith("_") and func.__module__.startswith(
                _module.__name__
            ):
                yield func

    def getmodules(_module):
        for _, m in inspect.getmembers(_module, inspect.ismodule):
            if m.__package__.startswith(_module.__package__):
                yield m

    for ff in getfunctions(module):
        yield ff
    # for mm in getmodules(module):
    #    for ff in getfunctions(mm):
    #        yield ff


SEMVERFUNCS = [func for func in getallfunctions()]


@pytest.mark.parametrize(
    "func", SEMVERFUNCS, ids=[func.__name__ for func in SEMVERFUNCS]
)
def test_fordocstrings(func):
    assert func.__doc__, "Need a docstring for function %r from module %r" % (
        func.__name__,
        func.__module__,
    )
