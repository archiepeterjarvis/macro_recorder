from kivy import Logger
from kivy.uix.button import Button

import macro_recorder


class ButtonBase(Button):
    """
    Base class for all buttons in the application.
    """

    def __init__(self, **kwargs):
        super(ButtonBase, self).__init__(**kwargs)
        self.macro_recorder = macro_recorder.MacroRecorder()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.macro_recorder.record(macro_recorder.MacroAction(
                action_type=macro_recorder.MacroActionType.CLICK,
                action_args={
                    "pos": touch.pos
                }
            ))
            Logger.info(f"ButtonBase: Clicked at {touch.pos}")
        return super(ButtonBase, self).on_touch_down(touch)
