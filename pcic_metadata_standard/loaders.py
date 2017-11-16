import collections
import csv
import os
import os.path

import yaml

from pcic_metadata_standard import Atomic, Composite


def load_atomic_from_csv(filepath):
    with open(filepath) as file:
        basename, _ = os.path.splitext(os.path.basename(filepath))
        description = file.readline().rstrip()
        # print('load_atomic_from_csv', filepath, basename, description)
        reader = csv.DictReader(
            file,
            fieldnames=('name', 'source', 'required', 'comments')
        )
        attributes = list(reader)
        return Atomic(basename, description, attributes)


def load_atomics_from_csvs(data_dir):
    """Load a set of atomic metadata sets from a directory containing csv files.
    Each file contains the definition of one atomic metadata set.

    :param data_dir: (str) filepath of directory containicng csv files be loaded.
    :return: dict of
    """

    atomics = collections.OrderedDict()
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        atomic = load_atomic_from_csv(filepath)
        atomics[atomic.name] = atomic
    return atomics


def create_metadata_sets(atomics, composite_defns):
    """Create a complete collection of metadata sets from a

    :param atomics: dict of atomic metadata sets that is the basis for
        composites
    :param composite_defns: list of composite metadata set definitions
        (see below)
    :return: dict of all metadata sets, atomic and composite

    A composite metadata set definition (list element) is a dict with
    the following content::

        {
            <composite metadata set name>:
                'description': <description>
                'specification': [
                    {
                        'prefix': <prefix>,
                        'include': <metadata set name>,
                    },
                    ...
                ]
        }

    where

        - ``<prefix>`` is absent (not present in the dict), `None`, or the
          empty string for no prefix, or a non-empty string specifying the
          prefix.

        - ``<metadata set name>`` is a string naming a defined metadata set
          (atomic or composite). Composite metadata sets defined earlier (at
          lower indices) in the list of definitions can be named in later
          definitions.

    The metadata set definition is defined in this way to support its simple
    expression in a YAML file, as follows::

        - <composite metadata set name>:
            - prefix: <prefix>
              include: : <metadata set name>
            - prefix: <prefix>
              include: : <metadata set name>
            ...

        - <composite metadata set name>:
            ...

        ...
    """
    metadata_sets = collections.OrderedDict()
    metadata_sets.update(atomics)
    for definitions in composite_defns:
        # Technically, there can be many composite metadata sets defined in
        # a single list item, though we don't recommend it (order of maps is
        # arbitrary).
        for name, definition in definitions.items():
            specs = [
                {
                    'prefix': component.get('prefix', None),
                    'metadata_set': metadata_sets[component['include']],
                    'role': component.get('role', None),
                }
                for component in definition['specification']
            ]
            metadata_sets[name] = Composite(name, definition['description'], specs)
    return metadata_sets


def load_all_metadata_sets(atomic_data_dir, composite_defn_filepath):
    atomics = load_atomics_from_csvs(atomic_data_dir)
    with open(composite_defn_filepath) as f:
        composite_defns = yaml.safe_load(f)
    return create_metadata_sets(atomics, composite_defns)
