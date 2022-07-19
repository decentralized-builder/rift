from dbuilder.ast import Node, Expr, Statement
from dbuilder.func import CallStacks


def mark(*args):
    for o in args:
        if isinstance(o, Entity):
            if isinstance(o.data, Expr):
                o.data.__hide__ = True


class Invokable:
    def __init__(self, name, entity):
        self.name = name
        self.entity = entity
        self.method_annotations = None

    def __call__(self, *args, **kwargs):
        e = Entity(
            Expr.call_expr(
                self.entity,
                self.name,
                *args,
                annotations=self.method_annotations,
            ),
        )
        setattr(e, "__unpackable", True)
        setattr(e, "__expr", CallStacks.add_statement(Statement.EXPR, e.data))
        e.has_expr = True
        return e


class Entity(Node):
    N_ID = 0

    def __init__(self, data=None, name=None) -> None:
        super().__init__()
        if data is None:
            data = {}
        self.data = data
        self.NAMED = False
        if name is not None:
            self.NAMED = True
            self.name = name
        Entity.N_ID += 1
        self.id = Entity.N_ID
        self.assigned = False
        self.has_expr = False
        self.__used__ = False

    def __eq__(self, other):
        mark(self, other)
        return Entity(Expr.binary_op("==", self, other))

    def __le__(self, other):
        mark(self, other)
        return Entity(Expr.binary_op("<=", self, other))

    def __add__(self, other):
        mark(self, other)
        return Entity(Expr.binary_op("+", self, other))

    def __radd__(self, other):
        mark(self, other)
        return Entity(Expr.binary_op("+", other, self))

    def __or__(self, other):
        mark(self, other)
        return Entity(Expr.binary_op("|", self, other))

    def __ror__(self, other):
        mark(self, other)
        return Entity(Expr.binary_op("|", other, self))

    def __invert__(self):
        mark(self)
        return Entity(Expr.unary_op("~", self))

    def __getattr__(self, item):
        mark(self)
        return Invokable(item, self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.NAMED:
            return self.name
        return repr(self.data)

    def __assign__(self, v):
        if self.NAMED:
            CallStacks.add_statement(
                Statement.ASSIGN, v, Expr.variable(self.name),
            )
            return Entity(
                name=v,
            )
        if self.has_expr:
            _x = getattr(self, "__expr")
            s: Statement = Node.find(_x)
            s.args = (v, s.args[0])
            s.type = Statement.ASSIGN
        else:
            # TODO: Most likely this never occurs (cleanup)
            CallStacks.add_statement(Statement.ASSIGN, v, self.data)
        self.NAMED = True
        self.name = v

    def __massign__(self, vs, xs):
        if self.has_expr:
            _x = getattr(self, "__expr")
            s: Statement = Node.find(_x)
            if s.type == s.EXPR:
                s.args = (vs, s.args[0])
                s.type = Statement.M_ASSIGN
            else:
                CallStacks.add_statement(Statement.M_ASSIGN, vs, self.data)
        for x, v in zip(xs, vs):
            x.NAMED = True
            x.name = v

    def __prep_unpack__(self, l_):
        self._unpack_len = l_

    def __iter__(self):
        if hasattr(self, "__unpackable") and self.__unpackable:
            for _ in range(self._unpack_len):
                yield Entity()

    @classmethod
    def type_name(cls) -> str:
        return ""

    @classmethod
    def abstract_init(cls, *args, **kwargs) -> "Entity":
        return cls(*args, **kwargs)
