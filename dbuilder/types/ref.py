from dbuilder.core import Entity
from dbuilder.types.types import Builder, Slice, Cell
from dbuilder.types.bases.entity_base import _EntityBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbuilder.types.payload import Payload


class RefType(_EntityBase):
    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        base = cls.__basex__
        if base == Cell:
            b = to.ref(value)
        elif hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            p: "Payload" = value
            c = p.as_cell()
            b = to.ref(c)
        return b

    @classmethod
    def __deserialize__(
        cls, from_: "Slice", name: str = None, inplace: bool = True,
    ):
        base = cls.__basex__
        if inplace:
            v = from_.ref_()
        else:
            v = from_.ref()
        if base == Cell:
            if name is not None:
                v.__assign__(name)
        if hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            v = v.parse()
            p: "Payload" = base(v, name=name)
            p.load()
            v = p
        return v

    @classmethod
    def __predefine__(cls, name: str = None):
        if name is None:
            return
        base = cls.__basex__
        if base == Cell:
            Cell.__predefine__(name)
        elif hasattr(base, "__magic__") and base.__magic__ == 0xA935E5:
            base.__predefine__(name)


class _RefTypeBuilder(type):
    def __new__(cls, base_cls=Cell):
        return super().__new__(
            cls,
            "Ref_%s" % (base_cls.__name__,),
            (RefType,),
            {
                "__basex__": base_cls,
            },
        )


def Ref(base: type = Cell):
    return _RefTypeBuilder.__new__(_RefTypeBuilder, base_cls=base)
