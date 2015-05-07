from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionGroup, ActionPrevious, ActionItem, ActionButton
from designer.uix.contextual import ContextSubMenu


class DesignerActionPrevious(ActionPrevious):
    pass


class DesignerActionSubMenu(ContextSubMenu, ActionItem):
    pass


class DesignerActionGroup(ActionGroup):
    pass


class DesignerActionButton(ActionButton):
    '''DesignerActionButton is a ActionButton to the ActionBar menu
    '''

    cont_menu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(DesignerActionButton, self).__init__(**kwargs)
        self.minimum_width = 150
        self.on_press= self.on_btn_press

    def on_btn_press(self, *args):
        '''
        Event to hide the ContextualMenu when a ActionButton is pressed
        '''
        self.cont_menu.dismiss()