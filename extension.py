import omni.ext
import omni.ui as ui
from omni.ui import scene as sc
import carb
import omni.appwindow
import omni.kit.app

import asyncio
from typing import Sequence, Tuple
from omni.kit.viewport.utility import get_active_viewport_window
from .manager.state_machine import StateManager
from .viewport.point_model import PointModel
from .panel.startDraw import startPanel
from .manager.state_machine import StateManager
from .prims.L1model import L1Model

class MyTestA1Extension(omni.ext.IExt):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance



    def on_startup(self, ext_id):
        print("[my.test.a1] my test a1 启动")
        # StateManager.get_instance()  # 初始化状态管理器

        self._viewport_window = get_active_viewport_window()
        startpanel = startPanel()
        startpanel.initialize_state()
        self.__build_scene(ext_id)
        app = omni.kit.app.get_app()

        self.l1model = L1Model()

    def on_shutdown(self):
        print("[my.test.a1] my test a1 关闭")
        # 清理资源
        if hasattr(self, 'point_model'):
            del self.point_model  # 显式删除 point_model
        if self._scene_view:
            self._viewport_window.viewport_api.remove_scene_view(self._scene_view)
            self._scene_view = None  # 清除对 SceneView 的引用

    def __build_scene(self, ext_id):
        """
            Called to build the SceneView wehere the MeasureManipulator lives
        """
        with self._viewport_window.get_frame(ext_id):
            with ui.ZStack():
                self._scene_view = sc.SceneView()
                with self._scene_view.scene:
                    self.point_model = PointModel(self._viewport_window.viewport_api)

            self._viewport_window.viewport_api.add_scene_view(self._scene_view)