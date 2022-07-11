from dbuilder.ast.method import Method
from dbuilder.ast.node import Node
from dbuilder.ast.printer import Printer


class Contract(Node):
    methods: list[Method] = []
    vars = []
    current_method: Method = None

    def __init__(self, name):
        super().__init__()
        self.name = name

    def add_method(self, method):
        self.current_method = method
        self.methods.append(method)

    def add_statement(self, statement):
        self.current_method.add_statement(statement)

    def end_method(self, method):
        self.current_method = None

    def add_variable(self):
        pass

    def print_func(self, printer: Printer):
        # printer.incr_indent()
        for m in self.methods:
            m.print_func(printer)
        # printer.decr_indent()
