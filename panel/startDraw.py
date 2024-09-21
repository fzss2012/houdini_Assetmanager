
from typing import Optional

from carb import log_warn
from pxr import UsdGeom

import asyncio
from omni import ui
from omni.kit.ui import get_editor_menu
import omni.usd as ou
import omni.kit.app
from omni.kit.viewport.utility import get_active_viewport_window
from ..manager.state_machine import StateManager
from ..manager.Reference_Model import ReferenceModel
class startPanel(ui.Window):
    def __init__(self):
        super().__init__(title="Panel",
                         width=400,
                         height=400,
                         visible=True,
                         dockPreference=ui.DockPreference.DISABLED,
                         flags=ui.WINDOW_FLAGS_NO_SCROLLBAR,
                         )
        self.deferred_dock_in("Stage", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)
        self.state_manager = StateManager()
        self.initialize_state()
        self.reference_model = ReferenceModel()
        with self.frame:
            with ui.ScrollingFrame(style={"ScrollingFrame": {"background_color": 0}}):

                with ui.VStack():

                    def size_me(window):
                        window.width = 300
                        window.height = 300

                    ui.Button("aaaaa", clicked_fn=self.toggle_drawing_state)
    def toggle_drawing_state(self):
        current_state = self.state_manager.get_state()
        if current_state == "idle":
            self.reference_model.points = []
            action = "start_drawing"
        elif current_state == "drawing":
            action = "stop_drawing"
        else:
            return 
        if self.state_manager.transition(action):
            new_state = self.state_manager.get_state()
            self.update_status_label(new_state)
        else:
            log_warn("状态转换失败或未定义的动作")
    def update_status_label(self,state):
        return True
    def initialize_state(self):
        initial_state = "idle"  # 假设的初始状态
