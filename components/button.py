from kivy import Logger
from kivy.uix.button import Button

import macro_recorder


class ButtonBase(Button):
    def __init__(self, **kwargs):
        super(ButtonBase, self).__init__(**kwargs)
        self.macro_recorder = macro_recorder.MacroRecorder()

    def on_touch_down(self, touch):
        if super(ButtonBase, self).on_touch_down(touch):
            if not self.macro_recorder.recording:
                return True

            self.macro_recorder.record(macro_recorder.MacroAction(
                action_type=macro_recorder.MacroActionType.MOUSE_DOWN,
                action_args={
                    "pos": touch.pos
                }
            ))
            Logger.info(f"ButtonBase: Mouse down at {touch.pos}")

    def on_touch_up(self, touch):
        if super(ButtonBase, self).on_touch_up(touch):
            if not self.macro_recorder.recording:
                return True

            self.macro_recorder.record(macro_recorder.MacroAction(
                action_type=macro_recorder.MacroActionType.MOUSE_UP,
                action_args={
                    "pos": touch.pos
                }
            ))
            Logger.info(f"ButtonBase: Mouse up at {touch.pos}")
