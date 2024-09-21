from omni.ui_scene import scene as sc


class PreventOthers(sc.GestureManager):
    """
        Hide other gestures
    """
    def __init__(self):
        self._manipulator = None
        self._white_list = ['PanGesture', 'TumbleGesture', 'LookGesture', 'ZoomGesture', 'MeasureClick', 'MeasureHover', 'MeasureDelete']
        super().__init__()

    def __del__(self):
        self._manipulator = None

    def can_be_prevented(self, gesture) -> bool:
        """
            Called per gesture. Determines if the gesture can be prevented.
        """
        return

    def should_prevent(self, gesture, preventer) -> bool:

        return 
