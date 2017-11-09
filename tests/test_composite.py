import pytest

from pcic_metadata_standard import \
    Atomic, Composite, Prefixed, \
    create_metadata_sets


def test_composite(atomic_dummy, atomic_pcic_common_subset):
    composite = Composite(
        (None, atomic_dummy),
        ('pfx', atomic_pcic_common_subset),
    )
    assert all(isinstance(component, Prefixed)
               for component in composite.components())


@pytest.mark.parametrize('atomics, composite_defns', [
    (['dummy', 'pcic_common_subset'],
     [
         {'foo': [
             {'prefix': None, 'include': 'dummy'}
         ]},
         {'bar': [
             {'prefix': 'pfx', 'include': 'dummy'}
         ]},
         {'qux': [
             {'include': 'dummy'},
             {'prefix': 'pfx', 'include': 'dummy'},
             {'prefix': 'other', 'include': 'pcic_common_subset'},
         ]},
     ]),
], indirect=['atomics'])
def test_create_metadata_sets(atomics, composite_defns):
    metadata_sets = create_metadata_sets(atomics, composite_defns)

    atomics_keys = set(atomics.keys())
    composites_keys = set().union(*(set(d.keys()) for d in composite_defns))

    assert set(metadata_sets.keys()) == atomics_keys | composites_keys

    assert all(isinstance(metadata_sets[name], Atomic)
               for name in atomics_keys)

    assert all(isinstance(metadata_sets[name], Composite)
               for name in composites_keys)


    def get_defn(name):
        for definitions in composite_defns:
            for key, defn in definitions.items():
                if key == name:
                    return defn

    # print()
    # for name in composites_keys:
    #     print(name, get_defn(name))
    #     for i, component in enumerate(metadata_sets[name].components()):
    #         print('\t', i, component.prefix)
    #         print('\t', i, get_defn(name)[i])

    assert all(
        component.prefix == get_defn(name)[i].get('prefix', None)
        for name in composites_keys
        for i, component in enumerate(metadata_sets[name].components())
    )

    assert all(
        component.metadata_set == metadata_sets[get_defn(name)[i]['include']]
        for name in composites_keys
        for i, component in enumerate(metadata_sets[name].components())
    )
