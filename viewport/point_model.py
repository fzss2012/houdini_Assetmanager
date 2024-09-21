import omni.ui.scene as sc

from .ViewportModel import ViewportModeModel

from .Manipulator_Items import PositionItem
from .layerlable import MeasureSceneLabel
from pxr import Gf




from typing import Sequence, List

import omni.kit.raycast.query
from ..manager.state_machine import StateManager
from ..manager.Reference_Model import ReferenceModel

class PointModel(ViewportModeModel):
    def __init__(self,viewport_api):
        super().__init__(viewport_api) 

        self.points = []  
        self._start_point = PositionItem(changed_fn=self._on_point_changed)
        self._end_point = PositionItem(changed_fn=self._on_point_changed)
        self.active_point = None  
        self.curline = None
        self.visable = False
        self.mid_point = [0,0,0]
        # self.layervar = None  # Initialize layervar to None
        self.layervar = MeasureSceneLabel("",clicked_fn=self._on_point_changed,visible=self.visable)

        self.line_length = MeasureSceneLabel("",clicked_fn=self._on_point_changed,visible=self.visable)


        self.line_count = -1  # 初始化点击计数器
        self.current_state = None
        # self.line_length = None  # Initialize layervar to None
        self.distance = 0
        self.state_manager = StateManager()
        # 注册当前实例为观察者
        self.state_manager.register_observer(self)
        self.reference_model = ReferenceModel()
        self.object_list = []
        self.layer_label = []
        self.length_label = []
    def reset(self):
        super().reset()
        self._root.clear()


        
        self._start_point.value = [0, 0, 0]
        # self._end_point.value = [0, 0, 0]




    def update(self, state):
        self.on_state_change(state)

    def _on_moved(self, coords: Sequence[float]):
        self.cur_point =coords



    def on_state_change(self, new_state):
        self.current_state = new_state  
        if new_state == "idle" and self.state_manager.cleanup_drawing_tools():
            start_point = self.reference_model.points[0]
            end_point = self.reference_model.points[-1]
            
            # 重新计算中点
            strt_mid_point = [(start_point[i] + end_point[i]) / 2 for i in range(3)]
            # 重新计算距离
            start_distance = ((end_point[0] - start_point[0])**2 + 
                            (end_point[1] - start_point[1])**2 + 
                            (end_point[2] - start_point[2])**2)**0.5
            
            self.object_list[0].start = start_point
            self.object_list[0].end = end_point
            self.object_list[0].visible = True

            self.layer_label[0].visible(True)
            self.layer_label[0].text = "0"
            self.length_label[0].text = f"dist:{round(start_distance, 2)}"  # 保留两位小数

            self.length_label[0].visible(True)

            self.layer_label[0].set_position(strt_mid_point)
            self.length_label[0].set_position(Gf.Vec3d(strt_mid_point) + Gf.Vec3d(0, -5, 0))





    def _on_clicked(self, coords: Sequence[float], mouse_button: int=0):
        self.reference_model.points.append(self.cur_point)

        if self.current_state == 'drawing':
            if self.active_point:
                point1 = self.active_point
                point2 = self.cur_point



                
                self._end_point.value = self.cur_point
                self.active_point = None
                self.visable = True

                line = Gf.Range3d(self._start_point.value, self._end_point.value)
                mid_point = line.GetMidpoint()
                self.mid_point = mid_point
                size = line.GetSize()
                distance = round(Gf.Vec3d(size).GetLength(), 2)
                self.distance = distance

            else:
                self._start_point.value = self.cur_point
                self.active_point = self._start_point.value
                

                line = Gf.Range3d(self._start_point.value, self._end_point.value)
                mid_point = line.GetMidpoint()
                self.mid_point = mid_point
                size = line.GetSize()
                distance = round(Gf.Vec3d(size).GetLength(), 2)
                self.distance = distance
    def draw(self):

   

        self._color = [1,0,0,.5]

        with self._root:
            self._ui_line = sc.Line(
                self._start_point.value,
                self._end_point.value,
                color=self._color,
                thickness=3,
                visible=self.visable
            )
            self._ui_points = sc.Points(
                [self._start_point.value,self._end_point.value],
                sizes=[5,5],
                colors=[self._color]*2,
                visible=self.visable
            )

        with self._label_root:


            self.layervar = MeasureSceneLabel("",clicked_fn=self._on_point_changed,visible=self.visable)




            self.layervar.set_position(self.mid_point)

            self.line_length = MeasureSceneLabel("",clicked_fn=self._on_point_changed,visible=self.visable)

            self.line_length.set_position(self.mid_point+Gf.Vec3d(0,-5,0))


            self.layervar.text =str(self.line_count)
            self.line_length.text = "dist:"+str(self.distance)





        self.object_list.append(self._ui_line)
        self.layer_label.append(self.layervar)
        self.length_label.append(self.line_length)
    def _on_point_changed(self):

        # if self.layervar:
            

        self.line_count += 1  
        return
