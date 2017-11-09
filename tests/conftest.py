from pytest import fixture
from pkg_resources import resource_filename

from pcic_metadata_standard import Atomic

def atomic(name):
    filepath = resource_filename(
        __name__, 'data/atomic/test_{}.csv'.format(name))
    return Atomic(name, filepath)


@fixture
def atomic_dummy():
    return atomic('dummy')


@fixture
def atomic_pcic_common_subset():
    return atomic('pcic_common_subset')


@fixture
def atomic_dataset(request):
    return atomic(request.param)


@fixture
def atomics(request):
    print(request.param)
    return { name: atomic(name) for name in request.param }

