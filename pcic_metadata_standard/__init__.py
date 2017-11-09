"""Classes for defining metadata sets."""

import os
import os.path
import collections
import csv

import yaml


class Atomic:
    """
    An Atomic metadata attribute set, whose specification (set of metadata
    attributes) is defined in a csv file."""

    def __init__(self, name, filepath):
        """

        :param filepath: (str) path to csv file containing metadata attribute
            definitions
        """
        self.name = name
        with open(filepath) as file:
            self.description = file.readline()
            reader = csv.DictReader(
                file,
                fieldnames=('name', 'source', 'required', 'comments')
            )
            self._attributes = list(reader)

    def attributes(self):
        return self._attributes

    def components(self):
        return [self]


class Prefixed:
    """
    A Prefixed metadata attribute set. This is an Atomic or Composite
    metadata set with a prefix attached.
    """

    def __init__(self, prefix=None, metadata_set=None, role=None):
        assert prefix is None or isinstance(prefix, str)
        assert isinstance(metadata_set, (Atomic, Composite))
        self.prefix = prefix
        self.metadata_set = metadata_set
        self.role = role

    def attributes(self, prefix_separator='__'):
        prefix = self.prefix + prefix_separator if self.prefix else ''
        return [
            # make a copy and update 'name'
            dict(attr, name=prefix + attr['name'])
            for component in self.metadata_set.components()
            for attr in component.attributes()
        ]


class Composite:
    """
    A Composite metadata attribute set, whose specification is given by
    a list of prefixes and attribute sets
    """

    def __init__(self, name, specs):
        assert isinstance(specs, (list, tuple))
        self.name = name
        self._components = [Prefixed(**spec) for spec in specs]

    def components(self):
        return self._components


def load_atomics(data_dir):
    """Load a set of atomic metadata sets from a directory containing csv files.
    Each file contains the definition of one atomic metadata set.

    :param data_dir: (str) filepath of directory containing csv files be loaded.
    :return: dict of
    """

    atomics = collections.OrderedDict()
    for filename in os.listdir(data_dir):
        basename, _ = os.path.splitext(os.path.basename(filename))
        filepath = os.path.join(data_dir, filename)
        atomics[basename] = Atomic(basename, filepath)
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
            metadata_sets[name] = Composite(name, specs)
    return metadata_sets


def all_metadata_sets(atomic_data_dir, composite_defn_yaml):
    atomics = load_atomics(atomic_data_dir)
    with open(composite_defn_yaml) as f:
        composite_defns = yaml.safe_load(f)
    return create_metadata_sets(atomics, composite_defns)