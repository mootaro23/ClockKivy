from time import strftime
import re

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class ClockLayout(BoxLayout):
    """
    root widget を象徴するクラス
    """
    time_prop = ObjectProperty(None)  # 時刻を表示する Label widget
    watch_prop = ObjectProperty(None)  # ストップウォッチを表示する Label widget
    btn_box = ObjectProperty(None)
    start_btn = ObjectProperty(None)
    reset_btn = ObjectProperty(None)


class ClockApp(App):
    stop_watch = False
    total_past = 0.0

    on_size_call = False
    font_ratio = 0  # 初期状態での texture_size.y に対する font_size の比率
    texture_ratio = 0  # 初期状態での texture_size.y に対する texture_size.x の比率
    stop_watch_pat = re.compile(r'(?:\[size=\d+\])?(?P<size>\d+)(?:\[/size\])?')

    def on_start(self):
        Clock.schedule_interval(self.update, 0)
        self.root.btn_box.background_color = get_color_from_hex('#e6e6e6')

        # kivyファイル内ではなくこのアプリケーションクラス内でイベントハンドラの関連付けを行う方法
        # この場合のイベントハンドラの第２引数にはイベントが発生した instance が渡されてくる
        # self.root.start_btn.bind(on_press=self.cb_start)
        # self.root.reset_btn.bind(on_press=self.cb_reset)

    def update(self, nap):
        # self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')  # id を利用した widget の参照
        self.root.time_prop.text = strftime('[b]%H[/b]:%M:%S')  # property を利用した widget の参照
        if self.stop_watch:
            self.total_past += nap
            minutes, seconds = divmod(self.total_past, 60)
            micro_size = int(self.root.watch_prop.font_size * 0.7)
            self.root.watch_prop.text = f"{int(minutes):02}:{int(seconds):02}.[size={micro_size}]{int(seconds * 100 % 100):02}[/size]"

    def cb_start(self):
        self.root.start_btn.text = 'Start' if self.stop_watch else 'Stop'
        self.stop_watch = not self.stop_watch

    def cb_reset(self):
        self.stop_watch = False
        self.total_past = 0.0
        self.root.start_btn.text = 'Start'
        micro_size = int(self.root.watch_prop.font_size * 0.7)
        self.root.watch_prop.text = f"00:00.[size={micro_size}]00[/size]"

    def on_size(self):
        if self.on_size_call:
            label_x, label_y = self.root.time_prop.size

            # texture_size の 8 割に対してのサイズを基にする
            if (label_x / label_y) < self.texture_ratio:  # x 方向に対しての比率でフォントサイズを計算
                new_ratio = (label_x * 0.8) / self.texture_ratio
            else:  # y 方向に対しての比率でフォントサイズを計算
                new_ratio = label_y * 0.8
            self.root.time_prop.font_size = self.font_ratio * new_ratio
            self.root.watch_prop.font_size = self.font_ratio * new_ratio

            stop_txt_lst = self.root.watch_prop.text.split('.')
            micro_size = int(self.root.watch_prop.font_size * 0.6)
            m = self.stop_watch_pat.search(stop_txt_lst[1])
            self.root.watch_prop.text = f"{stop_txt_lst[0]}.[size={micro_size}]{m.group('size')}[/size]"
            box_height = int(self.root.time_prop.size[1] * 0.4)
            self.root.btn_box.height = box_height
            self.root.btn_box.padding = int(box_height * 0.15)
            self.root.btn_box.spacing = int(box_height * 0.15)

        else:
            self.font_ratio = self.root.time_prop.font_size / self.root.time_prop.texture_size[1]
            self.texture_ratio = self.root.time_prop.texture_size[0] / self.root.time_prop.texture_size[1]

        self.on_size_call = True


if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#ff6666')
    # resource_add_path(r"C:\Windows\Fonts")
    LabelBase.register(
        name='Roboto',
        fn_regular='Roboto-Thin.ttf',
        fn_bold='Roboto-Medium.ttf'
    )
    ClockApp().run()

