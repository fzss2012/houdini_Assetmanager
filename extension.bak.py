import omni.ext
import omni.ui as ui
from omni.ui import scene as sc
import omni.kit.raycast.query as raycast
from omni.kit.viewport.utility import get_active_viewport_window
import carb
import omni.appwindow
import asyncio
from typing import Sequence, Tuple
from .viewport.Manipulator_Items import PositionItem
from .viewport.point_model import PointToPointModel
class MyTestA1Extension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[my.test.a1] my test a1 启动")
        self.draw = False  # 初始化 _draw 属性
        self.ext_id = ext_id
        self._viewport_window = get_active_viewport_window()
        self._gesture_manager = sc.GestureManager()
        
        self._api=self._viewport_window.viewport_api

        self._current_point = PositionItem(changed_fn=self._on_point_changed)
        self.points = []

        self.pane = ui.Window("Example Window", width=300, height=300)
        

        with self.pane.frame:
            with ui.VStack():
                ui.Label("Hello World")
                ui.Button("click me", clicked_fn=self._on_start_point_clicked)



        self.gesture=sc.ClickGesture(
            name="point",
            mouse_button=0,
            on_ended_fn=lambda sender: self.__on_moved(sender,1),
            manager=self._gesture_manager  
            )



    def on_shutdown(self):
        print("[my.test.a1] my test a1 关闭")
        
    def __on_moved(self, sender, mouse_button):
        if not hasattr(self, '_api'):
            print("错误: _api 尚未初始化。")
            return  # 或者其他错误处理逻辑
        locals = self._generate_picking_ray(sender.gesture_payload.mouse)
        self._current_point.value = [locals[0][0], 0, locals[0][2]]


    def _generate_picking_ray(self, ndc_location: Sequence[float]) -> Tuple[Sequence[float], Sequence[float], float]:
        """
        A helper function to generate picking ray from ndc cursor location.
        """
        self._api=self._viewport_window.viewport_api
        ndc_near = (ndc_location[0], ndc_location[1], -1)
        ndc_far = (ndc_location[0], ndc_location[1], 1)
        view = self._api.view
        proj = self._api.projection
        view_proj_inv = (view * proj).GetInverse()

        origin = view_proj_inv.Transform(ndc_near)
        dir = view_proj_inv.Transform(ndc_far) - origin
        dist = dir.Normalize()

        return ((origin[0], origin[1], origin[2]), (dir[0], dir[1], dir[2]), dist)

    def _on_point_changed(self):
        # 获取当前点的值
        new_position = self._current_point.value
        
        self.pointz.positions = [new_position]  # 假设 set_positions 方法接受一个包含坐标的列表
        print("point changed", new_position)
    def _on_start_point_clicked(self):
        self.draw = not self.draw
        if self.draw:
            with self._viewport_window.get_frame(self.ext_id):
                with ui.ZStack():
                    self._scene_view = sc.SceneView()

                    with self._scene_view.scene:
                        self.pointz = PointToPointModel(self._viewport_window.viewport_api)
                        sc.Screen(
                            gesture=self.gesture
                        )
                    self._viewport_window.viewport_api.add_scene_view(self._scene_view)
        else:
            self._scene_view.scene.clear()
