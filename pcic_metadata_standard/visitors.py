from pcic_metadata_standard import Visitor, Atomic, Composite, Prefixed


class PrintVisitor(Visitor):
    """Visitor for printing contents of a metadata set"""

    def __init__(self, prefix_separator='__'):
        self.prefix_separator = prefix_separator
        self.prefixes = []

    def pre(self, node):
        node_type = type(node)

        if node_type == Atomic:
            print("{}: {}".format(node.name, node.description))
            non_null_prefixes = filter(None, self.prefixes)
            prefix = self.prefix_separator.join(non_null_prefixes)
            prefix += self.prefix_separator if prefix else ''
            for attribute in node._attributes:
                print("\t{}{}".format(prefix, attribute['name']))
        elif node_type == Composite:
            print("{}: {}".format(node.name, node.description))
        elif node_type == Prefixed:
            self.prefixes.append(node.prefix)

    def post(self, node):
        node_type = type(node)
        if node_type == Prefixed:
            self.prefixes.pop()
