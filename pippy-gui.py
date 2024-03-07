import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView


class LogViewPopup(Popup):
    def __init__(self, log, **kwargs):
        super(LogViewPopup, self).__init__(**kwargs)
        self.title = "Лог"
        self.content = Label(text=log)


class PippyUI(BoxLayout):
    def __init__(self, **kwargs):
        super(PippyUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20

        logo_label = Label(text="  ____ ___ ____  ______   __\n|  _ \_ _|  _ \|  _ \ \ / /\n| |_) | || |_) | |_) \ V / \n|  __/| ||  __/|  __/ | |\n|_|  |___|_|   |_|    |_|")
        self.add_widget(logo_label)

        self.install_button = Button(text="Установить пакет")
        self.install_button.bind(on_release=self.install_popup)
        self.add_widget(self.install_button)

        self.uninstall_button = Button(text="Удалить пакет")
        self.uninstall_button.bind(on_release=self.uninstall_popup)
        self.add_widget(self.uninstall_button)

        self.upgrade_button = Button(text="Обновить pip")
        self.upgrade_button.bind(on_release=self.upgrade_popup)
        self.add_widget(self.upgrade_button)

        self.log_button = Button(text="Просмотреть лог")
        self.log_button.bind(on_release=self.view_log)
        self.add_widget(self.log_button)

        self.quit_button = Button(text="Выйти")
        self.quit_button.bind(on_release=self.quit)
        self.add_widget(self.quit_button)

    def install_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text="Что вы хотите установить?"))
        package_input = TextInput()
        content.add_widget(package_input)
        button = Button(text="Установить")
        button.bind(on_release=lambda x: self.install(package_input.text))
        content.add_widget(button)
        popup = Popup(title="Установить пакет", content=content, size_hint=(None, None), size=(900, 600))
        popup.open()

    def install(self, package):
        self.show_loading_popup()
        os.system("pip install " + package)
        self.loading_popup.dismiss()
        self.show_success_popup()

    def uninstall_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text="Что вы хотите удалить?"))
        package_input = TextInput()
        content.add_widget(package_input)
        button = Button(text="Удалить")
        button.bind(on_release=lambda x: self.uninstall(package_input.text))
        content.add_widget(button)
        popup = Popup(title="Удалить пакет", content=content, size_hint=(None, None), size=(900, 600))
        popup.open()

    def uninstall(self, package):
        self.show_loading_popup()
        os.system("pip uninstall " + package)
        self.loading_popup.dismiss()
        self.show_success_popup()

    def upgrade_popup(self, instance):
        box = BoxLayout(orientation='vertical', padding=20)
        box.add_widget(Label(text="Обновление pip..."))
        popup = Popup(title="Обновить pip", content=box, size_hint=(None, None), size=(900, 600))
        popup.open()
        os.system("pip install --upgrade pip")
        popup.dismiss()
        self.show_success_popup()

    def show_loading_popup(self):
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text="Загрузка...", font_size='20sp'))
        popup = Popup(title="Подождите", content=content, size_hint=(None, None), size=(900, 600))
        self.loading_popup = popup
        popup.open()

    def show_success_popup(self):
        content = BoxLayout(orientation='vertical', padding=20)
        content.add_widget(Label(text="Операция успешно выполнена.", font_size='20sp'))
        button = Button(text="OK")
        content.add_widget(button)
        popup = Popup(title="Успешно", content=content, size_hint=(None, None), size=(900, 600))
        button.bind(on_release=popup.dismiss)
        popup.open()

    def view_log(self, instance):
        with open("pip.log", "r") as f:
            log = f.read()
        popup = LogViewPopup(log)
        popup.open()

    def quit(self, instance):
        quit()


class PippyApp(App):
    def build(self):
        return PippyUI()


if __name__ == '__main__':
    PippyApp().run()