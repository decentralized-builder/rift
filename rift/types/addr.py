from rift.core import Entity
from rift.types.bases import Builder, Cell, Int, Slice
from rift.types.int_aliases import int8, integer, uint2, uint256
from rift.types.maybe import Maybe
from rift.types.payload import Payload


class MsgAddress(Slice):
    class Std(Payload):
        __tag__ = "$10"
        anycast: Maybe[Cell]
        workchain: int8
        address: uint256

    @classmethod
    def __serialize__(cls, to: "Builder", value: "Entity") -> "Builder":
        if isinstance(value, Int) or isinstance(value, integer):
            b = type(value).__serialize__(to, value)
        else:
            b = to.slice(value)
        return b

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        inplace: bool = True,
        lazy: bool = True,
        **kwargs,
    ):
        # TODO: HANDLE INPLACE STUFF
        v = from_.addr_()
        if name is not None:
            v.__assign__(name)
        return v

    @classmethod
    def std(cls, workchain: int, addr: uint256) -> Slice:
        return (
            cls.Std(
                anycast=None,
                workchain=workchain,
                address=addr,
            )
            .as_cell()
            .parse()
        )

    @classmethod
    def empty(cls):
        return uint2(0b00)
