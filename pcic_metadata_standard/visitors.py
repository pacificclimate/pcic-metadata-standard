from pcic_metadata_standard import Visitor, Atomic, Composite, Prefixed


class PmsVisitor(Visitor):
    """
    Generic visitor for PMS definition trees.
    Manages the prefixes stack. Provides node type.
    """

    def __init__(self, prefix_separator='__'):
        self.prefix_separator = prefix_separator
        self.prefixes = []
        self.node_type = None

    def prefix(self):
        non_null_prefixes = filter(None, self.prefixes)
        result = self.prefix_separator.join(non_null_prefixes)
        result += self.prefix_separator if result else ''
        return result

    def pre(self, node):
        self.node_type = type(node)
        if self.node_type == Prefixed:
            self.prefixes.append(node.prefix)

    def post(self, node):
        self.node_type = type(node)
        if self.node_type == Prefixed:
            self.prefixes.pop()


class AttributeListVisitor(PmsVisitor):
    """
    Visitor for creating a list of attribute names.
    Useful for testing.
    """

    def __init__(self, prefix_separator='__'):
        super().__init__(prefix_separator)
        self.attributes = []

    def pre(self, node):
        super().pre(node)
        if self.node_type == Atomic:
            for attribute in node._attributes:
                self.attributes.append("{p}{n}".format(
                    p=self.prefix(), n=attribute['name'])
                )


class CsvVisitor(PmsVisitor):
    """
    Visitor for creating CSV files suitable for importing into our
    Confluence documentation. More or less why this code was developed --
    to eliminate the error-prone cut-and-paste for that documentation.
    """
    pass  # TODO


class PrintVisitor(PmsVisitor):
    """
    Visitor for printing contents of a metadata set.
    """

    def __init__(self, prefix_separator='__', indentation_str='   '):
        super().__init__(prefix_separator)
        self.indentation_str = indentation_str
        self.indentation_level = 0
        self.role = ''

    def indent(self):
        self.indentation_level += 1

    def unindent(self):
        self.indentation_level -= 1

    def indentation(self):
        return self.indentation_str * self.indentation_level

    def pre(self, node):
        super().pre(node)

        if self.node_type == Atomic:
            print("{i}{r}{d} [{n}]".format(
                r="{}: ".format(self.role) if self.role else '',
                i=self.indentation(), n=node.name, d=node.description)
            )
            self.indent()
            for attribute in node._attributes:
                print("{i}{p}{n}".format(
                    i=self.indentation(), p=self.prefix(), n=attribute['name'])
                )

        elif self.node_type == Composite:
            print("{i}{r}{d} [{n}]".format(
                r="{}: ".format(self.role) if self.role else '',
                i=self.indentation(), n=node.name, d=node.description)
            )
            self.indent()

        elif self.node_type == Prefixed:
            self.role = node.role

    def post(self, node):
        super().post(node)
        if self.node_type == Atomic:
            self.unindent()
        elif self.node_type == Composite:
            self.unindent()
        elif self.node_type == Prefixed:
            self.role = ''
