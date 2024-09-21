import omni.ui.scene as sc
from abc import abstractmethod
from typing import Sequence, Tuple
import omni.kit.raycast.query


class GesturePreventionManager(sc.GestureManager):
    def __init__(self):
        super().__init__()

    def can_be_prevented(self, gesture: sc.AbstractGesture) -> bool:
        return False  # 允许所有手势

    def should_prevent(self, gesture: sc.AbstractGesture, preventer: sc.AbstractGesture) -> bool:
        return False  # 不阻止任何手势
    
class ViewportModeModel(sc.AbstractManipulatorModel):
    def __init__(self, viewport_api):
        super().__init__() 

        self._api = viewport_api
        self._raycast_query = omni.kit.raycast.query.acquire_raycast_query_interface()

        self.items = []  
        self.active_item = None 
        self.__base: sc.Transform = sc.Transform()

        with self.__base:
            self._screen: sc.Screen = self.__build_screen()
            self._root: sc.Transform = sc.Transform()
            self._label_root: sc.Transform = sc.Transform()
        # self.reset()
    def __build_screen(self) -> sc.Screen:
        gesture_manager: GesturePreventionManager = GesturePreventionManager()
        move_gesture = sc.HoverGesture(
            name=f"move",
            on_changed_fn=lambda sender: self.__on_moved(sender),
            manager=gesture_manager
        )
        click_gesture = sc.ClickGesture(
            name=f"right_click",
            mouse_button=0,
            on_ended_fn=lambda sender: self.__on_clicked(sender, 0),
            manager=gesture_manager
        )
        return sc.Screen(gestures=[
            move_gesture,
            click_gesture,
        ])
    
    def __on_clicked(self, sender: sc.ClickGesture, button: int):
        self._on_clicked(sender, button)
        self.draw()

    def __on_moved(self, sender):
        coords = self._api.map_ndc_to_texture(sender.gesture_payload.mouse)[-1]

        plane_point = [0, 0, 0]
        plane_normal = [0, 1, 0]
        
        def ray_plane_intersection_callback(ray, result):
            # 计算射线与平面的交点
            t = (plane_point[1] - ray.origin[1]) / ray.forward[1]
            intersection_point = [
                ray.origin[0] + t * ray.forward[0],
                0,  # y坐标始终为0  
                ray.origin[2] + t * ray.forward[2]
            ]
            
            self._on_moved(intersection_point)  # 假设您有这样一个方法来处理移动

        if coords:
            origin, dir, dist = self._generate_picking_ray(sender.gesture_payload.mouse)
            ray = omni.kit.raycast.query.Ray(origin, dir)

            self._raycast_query.submit_raycast_query(ray, ray_plane_intersection_callback)

    @abstractmethod
    def draw(self):
        """
            Draw based on the state and mode
        """
        return
    @abstractmethod
    def reset(self):
        """
            Reset the data tied to the model
        """

    @abstractmethod
    def _on_moved(self, coords: Sequence[float]):
        return
    @abstractmethod
    def _on_clicked(self, coords: Sequence[float]):
        return
    def _generate_picking_ray(self, ndc_location: Sequence[float]) -> Tuple[Sequence[float], Sequence[float], float]:
        """
        A helper function to generate picking ray from ndc cursor location.
        """
        ndc_near = (ndc_location[0], ndc_location[1], -1)
        ndc_far = (ndc_location[0], ndc_location[1], 1)
        view = self._api.view
        proj = self._api.projection
        view_proj_inv = (view * proj).GetInverse()

        origin = view_proj_inv.Transform(ndc_near)
        dir = view_proj_inv.Transform(ndc_far) - origin
        dist = dir.Normalize()

        # Don't use (*origin) to unpack Gf Types. Very Slow
        return ((origin[0], origin[1], origin[2]), (dir[0], dir[1], dir[2]), dist)