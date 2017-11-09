import pytest

from pcic_metadata_standard import Prefixed


@pytest.mark.parametrize('prefix, prefix_separator, atomic_dataset', [
    (None, '$$', 'dummy'),
    ('', '$$', 'dummy'),
    ('xyz', '$$', 'dummy'),
    ('abc', '@', 'dummy'),
], indirect=['atomic_dataset'])
def test_prefixed_atomic(prefix, prefix_separator, atomic_dataset):
    prefixed = Prefixed(prefix, atomic_dataset)
    the_prefix = prefix + prefix_separator if prefix else ''
    assert {attr['name'] for attr in prefixed.attributes(prefix_separator)} == \
           {the_prefix + attr['name'] for attr in atomic_dataset.attributes()}

