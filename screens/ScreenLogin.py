from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

from database.banco import BancoDados

from kivymd.app import MDApp

class ScreenLogin(Screen):
    """class of login screen"""
    mensagem = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.db = BancoDados("teste")
        self.mensagem = ""
        Window.bind(on_key_down=self.key_action)
    
    def key_action(self, *args):
        lista = list(args)
        if (lista[1] == 13 and lista[2] == 40) or (lista[1] == 271 and lista[2] == 88): #enter
            self.login(self.ids.usuario, self.ids.senha)
        elif lista[1] == 9 and lista[2] == 43: #tab
            self.ids.usuario.focus = False
            self.ids.senha.ids.text_field.focus = True
            

    def login(self, usuario, senha):
        # Implementa regras para acesso.
        booleano = True
        manager = self.db.hasManager(usuario.text)
        if manager == None:
            manager = self.db.setUser(usuario.text, senha.ids.text_field.text)
        
        booleano = self.db.isLogin(usuario.text, senha.ids.text_field.text, manager[2])
            
        if booleano:
            self.db.setPasswordManager(senha.ids.text_field.text)
            MDApp.get_running_app().setPASSWORD(senha.ids.text_field.text)
            senha.ids.text_field.text = ""
            usuario.text = ""
            self.parent.current = 'usuario'
            self.mensagem = ""
        else:
            usuario.text = ""
            senha.ids.text_field.text = ""
            self.mensagem = "Senha incorreta!"