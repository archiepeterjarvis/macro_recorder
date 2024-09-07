from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

from components.button import ButtonBase
from macro_recorder import MacroRecorder


class DemoScreen(Screen):
    def __init__(self, **kwargs):
        super(DemoScreen, self).__init__(**kwargs)
        self.macro_recorder = MacroRecorder()

        layout = BoxLayout(orientation='vertical')
        button1 = ButtonBase(text='Hello', size_hint=(1, 0.5))
        button2 = ButtonBase(text='World', size_hint=(1, 0.5))
        layout.add_widget(button1)
        layout.add_widget(button2)
        self.add_widget(layout)

        control_layout = BoxLayout(orientation='horizontal')
        control_layout.add_widget(Button(text='Start', on_press=self.on_start))
        control_layout.add_widget(Button(text='Stop', on_press=self.on_stop))
        control_layout.add_widget(Button(text='Replay', on_press=self.on_replay))
        layout.add_widget(control_layout)

    def on_start(self, *args):
        self.macro_recorder.start()

    def on_stop(self, *args):
        self.macro_recorder.stop()
        self.macro_recorder.save_actions("demo.json")

    def on_replay(self, *args):
        Clock.schedule_once(lambda dt: self.macro_recorder.play(), 1)


class DemoApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(DemoScreen(name='demo'))
        return self.sm


if __name__ == '__main__':
    DemoApp().run()
