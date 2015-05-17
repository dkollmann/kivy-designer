import os
import shutil

from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ObjectProperty, \
    ConfigParser, ConfigParserProperty

class Builder(EventDispatcher):
    '''Builder interface
    '''

    def __init__(self, profiler):
        self.profiler = profiler
        self.designer = self.profiler.designer
        self.designer_settings = self.designer.designer_settings
        self.proj_watcher = self.designer.project_watcher
        self.proj_settings = self.designer.proj_settings
        self.ui_creator = self.designer.ui_creator
        self.run_command = self.ui_creator.kivy_console.run_command


class Buildozer(Builder):
    '''Class to handle Buildozer builder
    '''

    def __init__(self, profiler):
        super(Buildozer, self).__init__(profiler)


class Hanga(Builder):
    '''Class to handle Hanga builder
    '''

    def __init__(self, profiler):
        super(Hanga, self).__init__(profiler)


class Desktop(Builder):
    '''Class to handle Desktop builder
    '''

    def __init__(self, profiler):
        super(Desktop, self).__init__(profiler)
        self.python_path = ''
        self.args = ''

    def _get_python(self):
        '''Initialize python variables
        '''
        self.python_path = self.designer_settings.config_parser.getdefault(
            'global',
            'python_shell_path',
            ''
        )

        if self.python_path == '':
            self.profiler.dispatch('on_error', 'Python Shell Path not '
                                   'specified.'
                                   '\n\nUpdate it on \'File\' -> \'Settings\'')
            return

        self.args = self.proj_settings.config_parser.getdefault(
            'arguments',
            'arg',
            ''
        )

        envs = self.proj_settings.config_parser.getdefault(
            'env variables',
            'env',
            ''
        )

        for env in envs.split(' '):
            self.ui_creator.kivy_console.environment[
                env[:env.find('=')]] = env[env.find('=') + 1:]

    def run(self):
        '''Run the project using Python
        '''
        self._get_python()

        py_main = os.path.join(self.profiler.project_path, 'main.py')

        if not os.path.isfile(py_main):
            self.profiler.dispatch('on_error', 'Cannot find main.py')
            return

        self.run_command(
                    '%s %s %s' % (self.python_path, py_main, self.args))
        self.ui_creator.tab_pannel.switch_to(
            self.ui_creator.tab_pannel.tab_list[2])

        self.profiler.dispatch('on_message', 'Running main.py...')
        self.profiler.dispatch('on_run')
        self.ui_creator.kivy_console.bind(on_subprocess_done=self.on_stop)

    def stop(self, *args):
        '''If there is a process running, it'll be stopped
        '''
        self.ui_creator.kivy_console.kill_process()
        self.profiler.dispatch('on_stop')

    def clean(self, *args):
        '''Remove .pyc files and __pycache__ folder
        '''
        self.proj_watcher.stop()
        for _file in os.listdir(self.profiler.project_path):
            ext = _file.split('.')[-1]
            if ext == 'pyc':
                os.remove(os.path.join(self.profiler.project_path, _file))
        __pycache__ = os.path.join(self.profiler.project_path, '__pycache__')
        if os.path.exists(__pycache__):
            shutil.rmtree(__pycache__)

        self.proj_watcher.start_watching(self.profiler.project_path)
        self.profiler.dispatch('on_message', 'Project cleaned')

    def build(self, *args):
        '''Compile all .py to .pyc
        '''
        self._get_python()

        proj_path = self.profiler.project_path

        self.run_command(
                    '%s -m compileall %s' % (self.python_path, proj_path))

        self.ui_creator.tab_pannel.switch_to(
            self.ui_creator.tab_pannel.tab_list[2])

        self.profiler.dispatch('on_message', 'Building project...')
        self.profiler.dispatch('on_build')
        self.ui_creator.kivy_console.bind(on_subprocess_done=self.on_build)
        self.profiler.dispatch('on_build')

    def on_build(self, *args):
        '''on_build event handler
        '''
        self.profiler.dispatch('on_message', 'Build complete')
        self.profiler.dispatch('on_build')

    def on_stop(self, *args):
        '''on_stop event handler
        '''
        self.profiler.dispatch('on_stop')


class Profiler(EventDispatcher):
    profile_path = StringProperty('')
    ''' Profile settings path
    :class:`~kivy.properties.StringProperty` and defaults to ''.
    '''

    project_path = StringProperty('')
    ''' Project path
    :class:`~kivy.properties.StringProperty` and defaults to ''.
    '''

    designer = ObjectProperty(None)
    '''Reference of :class:`~designer.app.Designer`.
       :data:`designer` is a :class:`~kivy.properties.ObjectProperty`
    '''

    profile_config = ObjectProperty(None)
    '''Reference to a ConfigParser with the profile settings
    :class:`~kivy.properties.ObjectProperty` and defaults to None.
    '''

    pro_name = ConfigParserProperty('', 'profile', 'name', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile name
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    pro_builder = ConfigParserProperty('', 'profile', 'builder', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile builder
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    pro_target = ConfigParserProperty('', 'profile', 'target', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile target
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    pro_mode = ConfigParserProperty('', 'profile', 'mode', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile builder
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    pro_install = ConfigParserProperty('', 'profile', 'install', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile install_on_device
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    pro_debug = ConfigParserProperty('', 'profile', 'debug', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile debug mode
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    pro_verbose = ConfigParserProperty('', 'profile', 'verbose', 'profiler')
    '''Reference to a ConfigParser with the profile settings
    Get the profile verbose mode
    :class:`~kivy.properties.ConfigParserProperty`
    '''

    builder = ObjectProperty(None)
    '''Reference to the builder class. Can be Hanga, Buildozer or Desktop
    :class:`~kivy.properties.ObjectProperty`
    '''

    __events__ = ('on_run', 'on_stop', 'on_error', 'on_message', 'on_build')

    def __init__(self, **kwargs):
        super(Profiler, self).__init__(**kwargs)
        self.profile_config = ConfigParser(name='profiler')

    def _update_profile(self):
        '''Reload the profile configuration
        '''
        pass

    def run(self):
        '''Run project
        '''
        self.builder.run()

    def stop(self):
        '''Stop project
        '''
        self.builder.stop()

    def clean(self):
        '''Clean project
        '''
        self.builder.clean()

    def build(self):
        '''Build project
        '''
        self.builder.build()

    def load_profile(self, prof_path, proj_path):
        '''Read the settings
        '''
        self.profile_path = prof_path
        self.project_path = proj_path

        self.profile_config.read(self.profile_path)

        if self.pro_builder == 'Buildozer':
            self.builder = Buildozer(self)
        elif self.pro_builder == 'Hanga':
            self.builder = Hanga(self)
        else:
            self.builder = Desktop(self)

    def on_error(self, *args):
        '''on_error event handler
        '''
        pass

    def on_message(self, *args):
        '''on_message event handler
        '''
        pass

    def on_run(self, *args):
        '''on_run event handler
        '''
        pass

    def on_stop(self, *args):
        '''on_stop event handler
        '''
        pass

    def on_build(self, *args):
        '''on_build event handler
        '''
        pass