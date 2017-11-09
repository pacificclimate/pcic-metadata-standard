import pytest
from pkg_resources import resource_filename

from pcic_metadata_standard import load_atomics


@pytest.mark.parametrize('atomic_dataset, attr_names', [
    ('pcic_common_subset', '''
            contact
            Conventions
            creation_date
            domain
            frequency
            institute_id
            institution
            modeling_realm
            product
            project_id
            table_id
            title
            tracking_id
        '''.split()
    ),
], indirect=['atomic_dataset'])
def test_atomic(atomic_dataset, attr_names):
    attributes = atomic_dataset.attributes()
    assert isinstance(attributes, list)
    assert all(fieldname in attribute
               for attribute in attributes
               for fieldname in ('name', 'source', 'required', 'comments'))
    assert [attr['name'] for attr in attributes] == attr_names


def test_load_atomics():
    atomics = load_atomics(resource_filename(__name__, 'data/atomic'))
    assert set(atomics.keys()) >= {'test_dummy', 'test_pcic_common_subset'}
    assert all(atomic.name == key for key, atomic in atomics.items())

