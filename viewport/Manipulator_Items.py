from typing import Callable, List, Optional

from pxr import Gf

from omni.ui import scene as sc


class PositionItem(sc.AbstractManipulatorItem):
    def __init__(self, value: List[float] = [0.0, 0.0, 0.0], changed_fn: Optional[Callable[[], None]] = None):
        super().__init__()
        self._value: List[float] = value
        self._change_fn = changed_fn

    @property
    def vector(self) -> Gf.Vec3d:
        return Gf.Vec3d(self._value)

    @vector.setter
    def vector(self, value: Gf.Vec3d):
        self._value = [*value]

    @property
    def value(self) -> List[float]:
        return self._value

    @value.setter
    def value(self, value: List[float]) -> None:
        self._value = value
        self._on_value_changed()

    def _on_value_changed(self):
        if not self._change_fn:
            return
        self._change_fn()

    def add_value_changed_fn(self, function: Callable[[], None]):
        self._change_fn = function