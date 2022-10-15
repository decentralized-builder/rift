from typing import TYPE_CHECKING

from rift.fift.fift_behavior import FiftBehavior

if TYPE_CHECKING:
    from rift.fift.types.builder import Builder
    from rift.fift.types.slice import Slice


class _FiftBaseType(FiftBehavior):
    type_: str
    value: str

    def __init__(self):
        pass

    def __load_data__(self, value: str, *args, **kwargs):
        self.value = value

    def __stack_entry__(self):
        return {
            "type": self.__type__(),
            "value": self.value,
        }

    @classmethod
    def __type__(cls) -> str:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"Fift{self.__type__().capitalize()}{{{self.value}}}"

    def __assign__(self, *args, **kwargs):
        pass

    @classmethod
    def __serialize__(
        cls, to: "Builder", value: "_FiftBaseType",
    ) -> "Builder":
        return to

    @classmethod
    def __deserialize__(
        cls,
        from_: "Slice",
        name: str = None,
        **kwargs,
    ):
        pass

    @classmethod
    def __predefine__(
        cls,
        **kwargs,
    ):
        pass
