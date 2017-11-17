import pytest

from pcic_metadata_standard import Prefixed
from pcic_metadata_standard.visitors import AttributeListVisitor


@pytest.mark.parametrize('prefix, prefix_separator, atomic_dataset', [
    (None, '$$', 'dummy'),
    ('', '$$', 'dummy'),
    ('xyz', '$$', 'dummy'),
    ('abc', '@', 'dummy'),
], indirect=['atomic_dataset'])
def test_prefixed_atomic(prefix, prefix_separator, atomic_dataset):
    prefixed = Prefixed(prefix=prefix, metadata_set=atomic_dataset)
    attribute_list_visitor = AttributeListVisitor(prefix_separator)
    prefixed.accept(attribute_list_visitor)

    the_prefix = prefix + prefix_separator if prefix else ''
    assert {attr['name'] for attr in attribute_list_visitor.attributes} == \
           {the_prefix + attr['name'] for attr in atomic_dataset.attributes}
