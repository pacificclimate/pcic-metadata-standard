from pcic_metadata_standard import Visitor, Atomic, Composite, Prefixed


class PrintVisitor(Visitor):
    """Visitor for printing contents of a metadata set"""

    def __init__(self, prefix_separator='__', indentation_str='   '):
        self.prefix_separator = prefix_separator
        self.prefixes = []
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
        node_type = type(node)

        if node_type == Atomic:
            print("{i}{r}{d} [{n}]".format(
                r="{}: ".format(self.role) if self.role else '',
                i=self.indentation(), n=node.name, d=node.description)
            )
            self.indent()
            non_null_prefixes = filter(None, self.prefixes)
            prefix = self.prefix_separator.join(non_null_prefixes)
            prefix += self.prefix_separator if prefix else ''
            for attribute in node._attributes:
                print("{i}{p}{n}".format(
                    i=self.indentation(), p=prefix, n=attribute['name'])
                )
        elif node_type == Composite:
            print("{i}{r}{d} [{n}]".format(
                r="{}: ".format(self.role) if self.role else '',
                i=self.indentation(), n=node.name, d=node.description)
            )
            self.indent()
        elif node_type == Prefixed:
            self.prefixes.append(node.prefix)
            self.role = node.role

    def post(self, node):
        node_type = type(node)
        if node_type == Atomic:
            self.unindent()
        elif node_type == Composite:
            self.unindent()
        elif node_type == Prefixed:
            self.prefixes.pop()
            self.role = ''
