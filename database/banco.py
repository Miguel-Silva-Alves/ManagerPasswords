import sqlite3
import cryptocode
import os

from settings import SECRET_KEY


class BancoDados():
    def __init__(self, passwordManager) -> None:
        caminho = os.path.join(os.path.dirname(__file__), 'database_saved.db')
        self.conexao = sqlite3.connect(caminho)
        self.criar_tabela_logins()
        self.criar_tabela_users()
        self.passwordManager = passwordManager
    
    def setPasswordManager(self, passwordManager):
        self.passwordManager = passwordManager
    
    def criar_tabela_users(self):
        self.conexao.execute("""
        create table if not exists user (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
    
    def criar_tabela_logins(self):
        """ cria a tabela 'login' caso ela não exista """
        self.conexao.execute("""
        create table if not exists login (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            senha TEXT NOT NULL,
            descricao TEXT
        )
        """)

    """ SET USER """
    def setUser(self, user, password):
        senha = cryptocode.encrypt(password, SECRET_KEY+password)
        cursor = self.conexao.cursor()
        cursor.execute("""
        INSERT INTO user (name, password)
        VALUES (?,?)
        """, (user, senha))
        self.conexao.commit()
        return self.hasManager(user)
        



    """ insere um login a tabela 'login' """
    def inserirLogin(self, login, senha, descricao, plus=None):

        senha = cryptocode.encrypt(senha, self.passwordManager)

        cursor = self.conexao.cursor()
        cursor.execute("""
        INSERT INTO login (login, senha, descricao)
        VALUES (?,?,?)
        """, (login, senha, descricao))
        self.conexao.commit()
    
    
    """ retorna um dicionario com todos os registros da tabela login"""
    def getLogins(self):
        cursor = self.conexao.cursor()
        # lendo os dados
        cursor.execute("""
        SELECT * FROM login;
        """)
        retorno = []
        for linha in cursor.fetchall():
            if linha[1] != '_loginManager3':
                senha = cryptocode.decrypt(linha[2],self.passwordManager)
                dic = {}
                dic['login'] = linha[1]
                dic['senha'] = senha
                dic['descricao'] = linha[3]
                dic['id'] = linha[0]
                retorno.append(dic)
        return retorno
    
    
    """ retorna uma lista com um único elemento referente ao login com determinado login"""
    def getLoginId(self, id):
        cursor = self.conexao.cursor()
        # lendo os dados
        cursor.execute("SELECT * FROM login WHERE id=?;", (id,))
        return cursor.fetchone()
    
    def hasManager(self, user):
        cursor = self.conexao.cursor()
        # lendo os dados
        cursor.execute("""
        SELECT * FROM user WHERE name=?;
        """, (user,))
        return cursor.fetchone()
    
    def isLogin(self, user, senha, autentificao):

        if cryptocode.decrypt(autentificao, SECRET_KEY+senha) == senha:
            return True
        return False

    def updateLogin(self, lista):
        senha = cryptocode.encrypt(lista[1],self.passwordManager)
        cursor = self.conexao.cursor()
        cursor.execute("UPDATE login SET login = ?, senha = ?, descricao = ? WHERE id = ?", (lista[0], senha, lista[2], lista[3]))
        self.conexao.commit()
    
    def deleteLogin(self, id):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM login WHERE id = ?", (id,))
        self.conexao.commit()
    
    def deleteMensagem(self, id):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM mensagens WHERE id = ?", (id,))
        self.conexao.commit()
    
    
    def fecharBanco(self):
        self.conexao.close()
