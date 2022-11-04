from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager


"""Import Screens"""
from screens.ScreenLogin import ScreenLogin
from screens.ScreenIcon import ScreenHelp
from screens.ScreenPass import ScreenUser
from utils.Menu import DrawerList, ContentNavigationDrawer
from utils.components import Password

"""Import KV files"""
Builder.load_file("utils/menu.kv")
Builder.load_file("utils/components.kv")
Builder.load_file("screens/screenicon.kv")
Builder.load_file("screens/screenlogin.kv")
Builder.load_file("screens/screenpass.kv")

class Manager(ScreenManager):
    pass

class MainApp(MDApp):
        
    def getPASSWORD(self):
        return self.PASSWORD
    
    def setPASSWORD(self, passwr):
        self.PASSWORD = passwr
    
    def change_screen(self, what):
            
        if what == "Senhas":
            MDApp.get_running_app().sm.current = 'usuario'
        
        elif what == 'Help':
            MDApp.get_running_app().sm.current = 'help'

        elif what == "Sair":
            MDApp.get_running_app().sm.current = 'telalogin'
    

    def build(self):
        self.sm = Manager()
        return self.sm

if __name__ == '__main__':
    MainApp().run()