import os
import os.path
import shutil

from kivy.config import ConfigParser
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.popup import Popup
from kivy.uix.settings import Settings, InterfaceWithSidebar, \
    MenuSidebar, ContentPanel

import designer
from designer.confirmation_dialog import ConfirmationDialog
from designer.helper_functions import get_kivy_designer_dir


class ProfileContentPanel(ContentPanel):
    ''' ContentPanel with a custom design and custom events
    '''

    __events__ = ('on_current_panel', )

    def __int__(self, **kwargs):
        super(ProfileContentPanel, self).__init__(**kwargs)

    def on_current_uid(self, *args):
        ''' Override the on_current_uid to to bind panel_change event
        '''
        super(ProfileContentPanel, self).on_current_uid(args)
        self.dispatch('on_current_panel')

    def on_current_panel(self, *args):
        ''' Event handler for panel_change
        '''
        pass


class ProfileMenuSidebar(MenuSidebar):
    pass


class ProfileSettingsInterface(InterfaceWithSidebar):
    ''' InterfaceWithSidebar with a custom style and custom events
    '''

    button_bar = ObjectProperty(None)
    ''' Reference to the widget's GridLayout with buttons
    :class:`~kivy.properties.ObjectProperty` and defaults to None.
    '''

    new_button = ObjectProperty(None)
    ''' Reference to the widget's New button.
    :class:`~kivy.properties.ObjectProperty` and defaults to None.
    '''

    __events__ = ('on_delete', 'on_new', )

    def __init__(self, **kwargs):
        super(ProfileSettingsInterface, self).__init__(**kwargs)
        self.button_bar.btn_delete_prof.bind(
            on_press=lambda j: self.dispatch('on_delete'))
        self.menu.new_button.bind(on_press=lambda j: self.dispatch('on_new'))
        self.content.bind(on_current_panel=self.on_current_panel)

    def on_delete(self, *args):
        '''Event handler for button "Delete" press
        '''
        pass

    def on_new(self, *args):
        '''Event handler for button "New" press
        '''
        pass

    def on_current_panel(self, *args):
        ''' Event handler to panel change
        The default profile cannot be deleted, so we watch this event to
        prevent the user to delete desktop.ini
        '''
        _file = self.content.current_panel.config.filename
        filename = os.path.basename(_file)
        self.button_bar.btn_delete_prof.disabled = filename == 'desktop.ini'


class ProfileSettings(Settings):
    '''Subclass of :class:`kivy.uix.settings.Settings` responsible for
       showing build profile settings of Kivy Designer.
    '''

    config_parsers = DictProperty({})
    '''List of config parsers
    :class:`~kivy.properties.DictProperty` and defaults to {}.
    '''

    def __init__(self, **kwargs):
        super(ProfileSettings, self).__init__(**kwargs)
        # list of ConfigParsers. Each file has one to handle the settings
        self.PROFILES_PATH = ''
        self.DEFAULT_PROFILES = ''
        self.interface.bind(on_new=self.on_new)
        self.interface.bind(on_delete=self.on_delete)

    def load_profiles(self):
        '''This function loads project settings
        '''
        self.config_parser = ConfigParser()
        self.PROFILES_PATH = os.path.join(get_kivy_designer_dir(),
            'profiles')

        _dir = os.path.dirname(designer.__file__)
        _dir = os.path.split(_dir)[0]
        self.DEFAULT_PROFILES = os.path.join(_dir, 'profiles')

        if not os.path.exists(self.PROFILES_PATH):
            shutil.copytree(self.DEFAULT_PROFILES, self.PROFILES_PATH)

        self.update_panel()

    def update_panel(self):
        '''Update the MenuSidebar
        '''
        _dir = os.path.dirname(designer.__file__)
        _dir = os.path.split(_dir)[0]

        self.config_parsers = {}
        self.interface.menu.buttons_layout.clear_widgets()

        for _file in os.listdir(self.PROFILES_PATH):
            _file_path = os.path.join(self.PROFILES_PATH, _file)
            config_parser = ConfigParser()
            config_parser.read(_file_path)
            prof_name = config_parser.getdefault('profile', 'name', 'PROFILE')
            if not prof_name.strip():
                prof_name = 'PROFILE'
            self.config_parsers[prof_name + '_' + _file_path] = config_parser

        for _file in sorted(self.config_parsers):
            prof_name = self.config_parsers[_file].getdefault('profile',
                                                              'name',
                                                              'PROFILE')
            if not prof_name.strip():
                prof_name = 'PROFILE'
            self.add_json_panel(prof_name,
                                self.config_parsers[_file],
                                os.path.join(
                                    _dir,
                                    'designer',
                                    'settings',
                                    'build_profile.json')
                                )

        # force to show the first profile
        first_panel = self.interface.menu.buttons_layout.children[-1].uid
        self.interface.content.current_uid = first_panel

    def on_config_change(self, *args):
        '''This function is default handler of on_config_change event.
        '''
        args[0].write()
        super(ProfileSettings, self).on_config_change(*args)

    def on_new(self, *args):
        '''Handler for "New Profile" button
        '''
        new_name = 'new_profile'
        i = 1
        while os.path.exists(os.path.join(
                self.PROFILES_PATH, new_name + str(i) + '.ini')):
            i += 1
        new_name += str(i)
        new_prof_path = os.path.join(
            self.PROFILES_PATH, new_name + '.ini')

        shutil.copy2(os.path.join(self.DEFAULT_PROFILES, 'desktop.ini'),
                     new_prof_path)
        config_parser = ConfigParser()
        config_parser.read(new_prof_path)
        config_parser.set('profile', 'name', new_name.upper())
        config_parser.write()

        self.update_panel()

    def on_delete(self, *args):
        '''Handler to "Delete profile" button
        '''
        self._confirm_dlg = ConfirmationDialog(
            message="Do you want to delete this profile?")
        self._popup = Popup(title='Delete Profile',
                            content=self._confirm_dlg,
                            size_hint=(None, None),
                            size=('200pt', '150pt'),
                            auto_dismiss=False)
        self._confirm_dlg.bind(on_ok=self._perform_delete_prof,
                               on_cancel=self._popup.dismiss)
        self._popup.open()

    def _perform_delete_prof(self, *args):
        '''Delete the selected profile
        '''
        selected_config = self.interface.content.current_panel.config.filename
        os.remove(selected_config)
        self.update_panel()
        self._popup.dismiss()
