from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.datatables import MDDataTable
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField

from utils.components import Password

from database.banco import BancoDados

class Content(BoxLayout):

    """class of dialog to add login"""
    def __init__(self, login = "", password = "", descricao = "", **kwargs):
        super().__init__(**kwargs)
        self.ids.login.text = login
        self.ids.password.text = password
        self.ids.descricao.text = descricao

class ContentSearch(BoxLayout):
    pass
        

class ScreenUser(Screen):

    dialog = None
    dialogChange = None
    dialogSearch = None
    lista_propriedades = ListProperty()  

    """função que configura o dataTable"""
    def on_pre_enter(self, *args):
        # self.lista_propriedades.append(["card-search", lambda x: self.peidar()])
        #self.lista_propriedades.append([MDTextField(text="Miguel"), lambda x: self.peidar()])
        

        self.ids.nav_drawer.set_state("close")
        layout = self.ids.anchor
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.9),
            use_pagination=True,
            column_data=[
                ("[color=#F8F8FF]Login[/color]", dp(50)),
                ("[color=#F8F8FF]Senha[/color]", dp(50)),
                ("[color=#F8F8FF]Descrição[/color]", dp(50)),
            ],
            row_data=[],

            background_color_header=get_color_from_hex("#65275d"),
            background_color_cell=get_color_from_hex("#7CFC00"),
            background_color_selected_cell=get_color_from_hex("#e4514f"),
        )
        self.data_tables.bind(on_row_press=self.row_selected)
        layout.add_widget(self.data_tables)
        self.popular()

    """função que popula o datatable"""
    def popular(self):
        PASSWORD = MDApp.get_running_app().getPASSWORD()
        self.db = BancoDados(PASSWORD)
        self.data_tables.row_data=[]
        self.lista_logins = self.db.getLogins()
        for dicionario in self.lista_logins:
            self.data_tables.add_row([dicionario['login'], dicionario['senha'], dicionario['descricao']])
    
    """when click on row"""
    def row_selected(self, table_view, cell_row):
        # get start index from selected row item range
        start_index, end_index = cell_row.table.recycle_data[cell_row.index]["range"]
        self.login = cell_row.table.recycle_data[start_index]["text"]
        self.senha = cell_row.table.recycle_data[end_index-1]["text"]
        self.descricao = cell_row.table.recycle_data[end_index]["text"]
        
        self.dialogChange = MDDialog(
                title="Inserção:",
                type="custom",
                content_cls=Content(self.login, self.senha, self.descricao),
                buttons=[
                    MDFlatButton(
                        text="Excluir",
                        theme_text_color="Custom",
                        on_release= self.excluir
                    ),
                    MDRaisedButton(
                        text="Alterar",
                        theme_text_color="Custom",
                        on_release= self.alterar
                    ),
                ],
            )
        self.dialogChange.open()
        
    """when plus button was clicked"""
    def more(self):
        
        if not self.dialog:
            self.dialog = MDDialog(
                title="Inserção:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="Fechar",
                        theme_text_color="Custom",
                        on_release= self.closeDialog
                    ),
                    MDRaisedButton(
                        text="Inserir",
                        theme_text_color="Custom",
                        on_release= self.inserir
                    ),
                ],
            )
        else:
            for obj in self.dialog.content_cls.children:
                if isinstance(obj, Password):
                    obj.ids.text_field.text = ""
                if isinstance(obj, MDTextField):
                    obj.text = ""
        self.dialog.open()
    
    """when inserir button was clicked"""
    def inserir(self, inst):
        lista = ["login", "senha", "descrição"]
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, Password):
                lista[1] = obj.ids.text_field.text
            if isinstance(obj, MDTextField):
                if obj.hint_text == "Login":
                    lista[0] = obj.text
                else:
                    lista[2] = obj.text
        if lista[0] == '' or lista[1] == '':
            print(lista)
            print('Nulo, não pode inserir')
        else:
            self.db.inserirLogin(lista[0], lista[1], lista[2])
            self.popular()
            self.dialog.dismiss()

    """when cancel button was clicked"""
    def closeDialog(self, inst):
        self.dialog.dismiss()
    
    """when eye button was clicked"""
    def changeEyes(self, inst):
        """altera a visibilidade da senha dentro do dialog"""
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                if obj.hint_text == "Password":
                    if obj.password:
                        self.dialog.buttons[0].icon = 'eye'
                    else:
                        self.dialog.buttons[0].icon = 'eye-off'

                    obj.password = not obj.password
                
    """when exit button was clicked"""
    def exit(self):
        self.db.fecharBanco()
        self.parent.current = 'telalogin'
    
    """função que retorna o id da linha"""
    def getLogin(self, login, senha, descricao):
        for dic in self.lista_logins:
            if dic['login'] == login and dic['senha'] == senha and dic['descricao'] == descricao:
                return dic['id']
        return -1

    """when alterar button was clicked"""
    def alterar(self, inst):
        iden = self.getLogin(self.login, self.senha, self.descricao)
        for obj in self.dialogChange.content_cls.children:
            if isinstance(obj, Password):
                senha = obj.ids.text_field.text
            if isinstance(obj, MDTextField):
                if obj.hint_text == "Login":
                    login = obj.text
                else:
                    descricao = obj.text

        self.db.updateLogin([login, senha, descricao, iden])
        self.dialogChange.dismiss()
        self.popular()
    
    """when excluir button was clicked"""
    def excluir(self, inst):
        iden = self.getLogin(self.login, self.senha, self.descricao)
        self.db.deleteLogin(iden)
        self.dialogChange.dismiss()
        self.popular()
    
    # função chamada quando o botão de pesquisar é clicado
    def pesquisar(self, x):
        print(x, 'pesquisar')
        if not self.dialogSearch:
            self.dialog = MDDialog(
                title="Pesquisa:",
                type="custom",
                content_cls=ContentSearch(),
                buttons=[
                    MDFlatButton(
                        text="Fechar",
                        theme_text_color="Custom",
                        on_release= self.closeDialog
                    ),
                    MDRaisedButton(
                        text="Pesquisar",
                        theme_text_color="Custom",
                        on_release= self.inserir
                    ),
                ],
            )
        else:
            for obj in self.dialog.content_cls.children:
                if isinstance(obj, Password):
                    obj.ids.text_field.text = ""
                if isinstance(obj, MDTextField):
                    obj.text = ""
        self.dialog.open()