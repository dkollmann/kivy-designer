import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.treeview import TreeViewLabel
from designer.uix.py_code_input import PyCodeInput, PyScrollView


class DesignerContent(FloatLayout):
    '''This class contains the body of the Kivy Designer. It contains,
       Project Tree and TabbedPanel.
    '''

    ui_creator = ObjectProperty(None)
    '''This property refers to the :class:`~designer.ui_creator.UICreator`
       instance. As there can only be one
       :data:`ui_creator` is a :class:`~kivy.properties.ObjectProperty`
    '''

    tree_toolbox_tab_panel = ObjectProperty(None)
    '''TabbedPanel containing Toolbox and Project Tree. Instance of
       :class:`~designer.designer_content.DesignerTabbedPanel`
    '''

    splitter_tree = ObjectProperty(None)
    '''Reference to the splitter parent of tree_toolbox_tab_panel.
       :data:`splitter_toolbox` is an
       :class:`~kivy.properties.ObjectProperty`
    '''

    toolbox = ObjectProperty(None)
    '''Reference to the :class:`~designer.toolbox.Toolbox` instance.
       :data:`toolbox` is an :class:`~kivy.properties.ObjectProperty`
    '''

    tree_view = ObjectProperty(None)
    '''This property refers to Project Tree. Project Tree displays project's
       py files under its parent directories. Clicking on any of the file will
       open it up for editing.
       :data:`tree_view` is a :class:`~kivy.properties.ObjectProperty`
    '''

    tab_pannel = ObjectProperty(None)
    '''This property refers to the instance of
       :class:`~designer.designer_content.DesignerTabbedPanel`.
       :data:`tab_pannel` is a :class:`~kivy.properties.ObjectProperty`
    '''

    def update_tree_view(self, proj_loader):
        '''This function is used to insert all the py files detected.
           as a node in the Project Tree.
        '''

        self.proj_loader = proj_loader

        # Fill nodes with file and directories
        self._root_node = self.tree_view.root
        for _file in proj_loader.file_list:
            self.add_file_to_tree_view(_file)

    def add_file_to_tree_view(self, _file):
        '''This function is used to insert py file given by it's path argument
           _file. It will also insert any directory node if not present.
        '''

        self.tree_view.root_options = dict(text='')
        dirname = os.path.dirname(_file)
        dirname = dirname.replace(self.proj_loader.proj_dir, '')
        # The way os.path.dirname works, there will never be '/' at the end
        # of a directory. So, there will always be '/' at the starting
        # of 'dirname' variable after removing proj_dir

        # This algorithm first breaks path into its components
        # and creates a list of these components.
        _dirname = dirname
        _basename = 'a'
        list_path_components = []
        while _basename != '':
            _split = os.path.split(_dirname)
            _dirname = _split[0]
            _basename = _split[1]
            list_path_components.insert(0, _split[1])

        if list_path_components[0] == '':
            del list_path_components[0]

        # Then it traverses from root_node to its children searching from
        # each component in the path. If it doesn't find any component
        # related with node then it creates it.
        node = self._root_node
        while list_path_components != []:
            found = False
            for _node in node.nodes:
                if _node.text == list_path_components[0]:
                    node = _node
                    found = True
                    break

            if not found:
                for component in list_path_components:
                    _node = TreeViewLabel(text=component)
                    self.tree_view.add_node(_node, node)
                    node = _node
                list_path_components = []
            else:
                del list_path_components[0]

        # Finally add file_node with node as parent.
        file_node = TreeViewLabel(text=os.path.basename(_file))
        file_node.bind(on_touch_down=self._file_node_clicked)
        self.tree_view.add_node(file_node, node)

        self.tree_view.root_options = dict(
            text=os.path.basename(self.proj_loader.proj_dir))

    def _file_node_clicked(self, instance, touch):
        '''This is emmited whenever any file node of Project Tree is
           clicked. This will open up a tab in DesignerTabbedPanel, for
           editing that py file.
        '''

        # Travel upwards and find the path of instance clicked
        path = instance.text
        parent = instance.parent_node
        while parent != self._root_node:
            _path = parent.text
            path = os.path.join(_path, path)
            parent = parent.parent_node

        full_path = os.path.join(self.proj_loader.proj_dir, path)
        if os.path.basename(full_path) == 'buildozer.spec':
            spec_editor = App.get_running_app().root.spec_editor

            spec_editor.load_settings(self.proj_loader.proj_dir)
            self._popup = Popup(title="Buildozer Spec", content=spec_editor,
                                size_hint=(0.9, 0.9), auto_dismiss=False)
            spec_editor.bind(on_close=self.cancel_spec_editor)
            self._popup.open()
        else:
            self.tab_pannel.open_file(full_path, path)

    def cancel_spec_editor(self, *args):
        '''Close the BuildozerSpecEditor
        '''
        spec_editor = App.get_running_app().root.spec_editor
        self._popup.dismiss()
        if spec_editor.parent:
            spec_editor.parent.remove_widget(spec_editor)
            spec_editor.parent = None


class DesignerTabbedPanel(TabbedPanel):
    '''DesignerTabbedPanel is used to display files opened up in tabs with
       :class:`~designer.ui_creator.UICreator`
       Tab as a special one containing all features to edit the UI.
    '''

    list_py_code_inputs = ListProperty([])
    '''This list contains reference to all the PyCodeInput's opened till now
       :data:`list_py_code_inputs` is a :class:`~kivy.properties.ListProperty`
    '''

    def open_file(self, path, rel_path, switch_to=True):
        '''This will open py file for editing in the DesignerTabbedPanel.
        '''

        for i, code_input in enumerate(self.list_py_code_inputs):
            if code_input.rel_file_path == rel_path:
                self.switch_to(self.tab_list[len(self.tab_list) - i - 2])
                return

        panel_item = DesignerTabbedPanelItem(text=os.path.basename(path))
        f = open(path, 'r')
        scroll = PyScrollView()
        _py_code_input = scroll.code_input
        _py_code_input.rel_file_path = rel_path
        _py_code_input.text = f.read()
        _py_code_input.bind(
            on_show_edit=App.get_running_app().root.on_show_edit)
        f.close()
        self.list_py_code_inputs.append(_py_code_input)
        panel_item.content = scroll
        self.add_widget(panel_item)
        if switch_to:
            self.switch_to(self.tab_list[0])


class DesignerTabbedPanelItem(TabbedPanelItem):
    pass
