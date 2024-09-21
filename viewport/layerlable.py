
from typing import Callable, List, Optional, Union

from omni.ui import scene as sc
from omni import ui
from pxr import Gf



class MeasureSceneLabel:
    def __init__(
        self,
        text: str,
        position: List[float] = [0,0,0],
        clicked_fn: Optional[Callable[[], None]] = None,
        visible: bool = False
    ):
        self._clicked_fn: Optional[Callable[[], None]] = clicked_fn

        self._root: sc.Transform = sc.Transform(
            look_at=sc.Transform.LookAt.CAMERA,
            transform=sc.Matrix44.get_translation_matrix(1,1,1)
        )

        self._click_gesture = sc.ClickGesture(
            name="click_scene_label",
            on_ended_fn=self._on_click,
        )

        self.__draw()
        self.set_position(position)
        self.visible(visible)

    def __draw(self):
        label_color = 0xFF000000
        text_size = 20

        with self._root:
            with sc.Transform(scale_to=sc.Space.SCREEN):
                self._label = sc.Label("", size=text_size, color=[0,0,0,1], alignment=ui.Alignment.CENTER)  # Aligns right


    @property
    def text(self) -> str:
        return self._label.text

    @text.setter
    def text(self, value: str) -> None:
        self._label.text = value


    def visible (self, value: bool) -> None:
        """
            Set widget visibility

            Args:
                value (bool): Visible
        """
        self._label.visible = value

    def set_position(self, position: Union[List[float], Gf.Vec3d]) -> None:
        """
            Set widget position

            Args:
                position (List[float], Gf.Vec3d): Position
        """
        self._root.transform = sc.Matrix44.get_translation_matrix(*position)

    def update(self, **kwargs):
        """
            Update properties of the widget

            Kwargs:
                text (str): Widget text
                position (List[float], Gf.Vec3d): Widget position
                visible (bool): Widget visibility
        """
        _text = kwargs.get("text", None)
        _position = kwargs.get("position", None)
        _visible = kwargs.get("visible", None)

        if _text and isinstance(_text, str):
            self.text = _text
        if _position and isinstance(_position, List):
            self.set_position(_position)
        if _visible and isinstance(_visible, bool):
            self.visible(_visible)

    def _on_click(self) -> None:
        if self._clicked_fn:
            self._clicked_fn()