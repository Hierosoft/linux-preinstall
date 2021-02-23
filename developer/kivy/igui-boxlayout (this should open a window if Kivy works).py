from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.factory import Factory

class MainForm(BoxLayout):
    pass

class MyApp(App):

    def build(self):
        form = MainForm()
        form.cols = 1
        form.orientation = "vertical"
        form.okButton = Factory.Button(text="OK", id="okButton")
        form.add_widget(form.okButton)
        return form

if __name__ == '__main__':
    MyApp().run()
