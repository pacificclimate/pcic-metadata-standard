"""Classes for defining metadata sets."""

from abc import ABC, abstractmethod


# Abstract base classes for visitor pattern

class Visitable(ABC):
    """ABC for defining classes that accept a visitor.
    A visitor is an instance of the Visitor class."""
    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError()


class Visitor(ABC):
    """ABC for defining classes that implement a visitor"""
    @abstractmethod
    def pre(self, node):
        """Method called before child nodes of `node` are called."""
        raise NotImplementedError()

    @abstractmethod
    def post(self, node):
        """Method called after child nodes of `node` are called."""
        raise NotImplementedError()


# Classes for defining metadata

class Atomic(Visitable):
    """
    An Atomic metadata attribute set, whose specification (set of metadata
    attributes) is defined in a csv file."""

    def __init__(self, name, description, attributes):
        """

        """
        self.name = name
        self.description = description
        self._attributes = attributes

    def attributes(self):
        return self._attributes

    def components(self):
        return [self]

    def accept(self, visitor):
        visitor.pre(self)
        # This is a leaf node; no children to accept visitor
        visitor.post(self)


class Composite(Visitable):
    """
    A Composite metadata attribute set, whose specification is given by
    a list of prefixed attribute sets
    """

    def __init__(self, name, description, specs):
        assert isinstance(specs, (list, tuple))
        self.name = name
        self.description = description
        self._components = [Prefixed(**spec) for spec in specs]

    def components(self):
        return self._components

    def accept(self, visitor):
        visitor.pre(self)
        for component in self._components:
            component.accept(visitor)
        visitor.post(self)


class Prefixed(Visitable):
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

    def accept(self, visitor):
        visitor.pre(self)
        self.metadata_set.accept(visitor)
        visitor.post(self)
