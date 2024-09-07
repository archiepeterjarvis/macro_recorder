import json
import os
import time
from enum import Enum

from kivy import Logger
from kivy.clock import Clock
from kivy.core.window import Window

MACROS_PATH = "./macros/"


class MacroActionType(Enum):
    MOUSE_DOWN = 1
    MOUSE_UP = 2


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
            cls._instance.recording = False
        return cls._instance

    def start(self):
        Logger.info("Recording started")
        self.recording = True

    def stop(self):
        Logger.info("Recording stopped")
        self.recording = False

    def record(self, action: MacroAction):
        if not self.recording:
            return

        Logger.info(f"Recording action: {action}")
        action.action_args['time'] = time.time()

        self.actions.append(action)

    def save_actions(self, filename):
        Logger.info(f"Saving actions to {filename}")

        # Alter the time argument so that it is relative to the start of the recording
        start_time = self.actions[0].action_args['time']
        for action in self.actions:
            action.action_args['time'] = action.action_args['time'] - start_time

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

        def _play(index):
            if index < len(self.actions):
                action = self.actions[index]
                if action.action_type == MacroActionType.MOUSE_DOWN:
                    self._simulate_mouse_down(action.action_args['pos'])
                elif action.action_type == MacroActionType.MOUSE_UP:
                    self._simulate_mouse_up(action.action_args['pos'])

                if index + 1 < len(self.actions):
                    Clock.schedule_once(lambda dt: _play(index + 1), self.actions[index + 1].action_args['time'])
        _play(0)

    @staticmethod
    def _simulate_mouse_down(pos):
        x, y = Window.size[0] - pos[0], Window.size[1] - pos[1]
        Logger.info(f"Simulating mouse down at {x}, {y}")

        Window.dispatch('on_mouse_down', x, y, 'left', {})

    @staticmethod
    def _simulate_mouse_up(pos):
        x, y = Window.size[0] - pos[0], Window.size[1] - pos[1]
        Logger.info(f"Simulating mouse up at {x}, {y}")

        Window.dispatch('on_mouse_up', x, y, 'left', {})
