import json
import os
import time
from enum import Enum

from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse

MACROS_PATH = "./macros/"


class MacroActionType(Enum):
    CLICK = 1
    DRAG = 2
    INPUT = 3


class MacroAction:
    def __init__(self, action_type: MacroActionType, action_args: dict):
        self.action_type = action_type
        self.action_args = action_args

    def to_dict(self):
        return {
            'action_type': self.action_type.name,
            'action_args': self.action_args
        }

    @classmethod
    def from_dict(cls, data):
        action_type = MacroActionType[data['action_type']]
        action_args = data['action_args']
        return cls(action_type, action_args)


class MacroRecorder:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MacroRecorder, cls).__new__(cls)
            cls._instance.actions = []
            cls._instance.sm = App.get_running_app().sm
        return cls._instance

    def record(self, action: MacroAction):
        Logger.info(f"Recording action: {action}")
        self.actions.append(action)
        Logger.info(f"Actions: {self.actions}")

    def save_actions(self, filename):
        Logger.info(f"Saving actions to {filename}")
        actions_dict = [action.to_dict() for action in self.actions]
        with open(os.path.join(MACROS_PATH, filename), "w") as f:
            json.dump(actions_dict, f)

    def load_actions(self, filename):
        Logger.info(f"Loading actions from {filename}")
        with open(os.path.join(MACROS_PATH, filename), "r") as f:
            actions_dict = json.load(f)
        self.actions = [MacroAction.from_dict(action) for action in actions_dict]

    def play(self):
        Logger.info("Playing actions")
        for action in self.actions:
            if action.action_type == MacroActionType.CLICK:
                pos = action.action_args['pos']
                self._simulate_click(pos)
            elif action.action_type == MacroActionType.DRAG:
                start_pos = action.action_args['start_pos']
                end_pos = action.action_args['end_pos']
                self._simulate_drag(start_pos, end_pos)
            elif action.action_type == MacroActionType.INPUT:
                text = action.action_args['text']
                self._simulate_input(text)

    def _simulate_click(self, pos):
        x, y = pos
        Logger.info(f"Simulating click at {x}, {y}")
        Window.dispatch('on_mouse_down', x, y, 'left', {})
        Clock.schedule_once(lambda dt: Window.dispatch('on_mouse_up', x, y, 'left', {}), 0.1)

    def _simulate_drag(self, start_pos, end_pos):
        Logger.warning("Drag simulation not implemented yet")

    def _simulate_input(self, text):
        Logger.warning("Input simulation not implemented yet")