"""
Config Example
==============

This file contains a simple example of how the use the Kivy settings classes in
a real app. It allows the user to change the caption and font_size of the label
and stores these changes.

When the user next runs the programs, their changes are restored.

"""

from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.lang import Builder

# We first define our GUI
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Configure app (or press F1)'
        on_release: app.open_settings()
    Label:
        id: label
        text: 'Hello'
'''



class MyApp(App):
    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = MySettingsWithTabbedPanel

        # We apply the saved configuration settings or the defaults
        root = Builder.load_string(kv)
        label = root.ids.label
        label.text = self.config.get('Frame1', 'name')
        label.font_size = float(self.config.get('Frame1', 'time_sec'))

        return root

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('time_up', {'time_hour': 0, 'time_min': 0})
        config.setdefaults('time_down', {'time_hour': 0, 'time_min': 0})
        for i in range(1, 118):
            config.setdefaults('Frame'+str(i), {'name': 'FRAME'+str(i), 'time_sec': 20, 'led': False})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        with open("sets.json", "r") as sets_json:
            settings.add_json_panel('Time settings', self.config, data=sets_json.read())

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "Frame1":
            if key == "name":
                self.root.ids.label.text = value
            elif key == 'time_sec':
                self.root.ids.label.font_size = float(value)

    def close_settings(self, settings):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MyApp, self).close_settings(settings)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).

    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """
    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))
    def add_kivy_panel(self):
        pass


MyApp().run()
