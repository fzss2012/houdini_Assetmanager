from omni.ui import scene as sc
from typing import List, Tuple


class MultiPoints:
    def __init__(self):
        self.points_data = []
        self.visible = True
        self.size = 1.0
        self.color = (1.0, 1.0, 1.0)  # 默认白色
        
    def add_point(self, position):
        self.points_data.append(position)
        
    def remove_point(self, index):
        if 0 <= index < len(self.points_data):
            del self.points_data[index]
            
    def clear_points(self):
        self.points_data.clear()
        
    def set_visibility(self, visible):
        self.visible = visible
        
    def set_size(self, size):
        self.size = size
        
    def set_color(self, color):
        self.color = color
        
    def get_points(self):
        return self.points_data
    


class ScPointsModel:
    def __init__(self):
        self.multi_points = MultiPoints()
        self.sc_points: sc.Points = None

    def create_sc_points(self, color: Tuple[float, float, float, float] = (1, 1, 1, 1), size: float = 1):
        """创建 sc.Points 对象"""
        self.sc_points = sc.Points(
            points=self.multi_points.get_points(),
            colors=[color] * len(self.multi_points.get_points()),
            sizes=[size] * len(self.multi_points.get_points())
        )

    def update_sc_points(self):
        """更新 sc.Points 对象的数据"""
        if self.sc_points:
            self.sc_points.points = self.multi_points.get_points()

    def add_point(self, point: List[float]):
        """添加一个新的点"""
        self.multi_points.add_point(point)
        self.update_sc_points()

    def remove_point(self, index: int):
        """移除一个点"""
        self.multi_points.remove_point(index)
        self.update_sc_points()

    def clear_points(self):
        """清除所有点"""
        self.multi_points.clear_points()
        self.update_sc_points()

    def set_visibility(self, visible: bool):
        """设置可见性"""
        self.multi_points.set_visibility(visible)
        if self.sc_points:
            self.sc_points.visible = visible

    def set_color(self, color: Tuple[float, float, float, float]):
        """设置颜色"""
        self.multi_points.set_color(color)
        if self.sc_points:
            self.sc_points.colors = [color] * len(self.multi_points.get_points())

    def set_size(self, size: float):
        """设置大小"""
        self.multi_points.set_size(size)
        if self.sc_points:
            self.sc_points.sizes = [size] * len(self.multi_points.get_points())



            