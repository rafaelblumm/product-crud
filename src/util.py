import os
import pathlib
from sqlite3 import Connection
import streamlit as st
import getpass

from database import Database

def is_dev_mode() -> bool:
    """ Indica se está no modo desenvolvedor
    (deve ter a variável de ambiente 'DEV_MODE' definida)
    :return: Se está no modo dev
    """
    if "DEV_MODE" not in os.environ:
        return False
    
    return True


def get_username() -> str:
    """ Busca nome de usuário configurado na tela de login.
    Se não houver, busca usuário do sistema operacional.
    Em último caso, retorna nome padrão.
    :return: Nome de usuário
    """
    if "username" not in st.session_state:
        return get_default_username()
    
    return st.session_state["username"]


def get_default_username() -> str:
    """ Busca nome de usuário do sistema operacional ou usuário padrão
    :return: Nome de usuário
    """
    user = getpass.getuser()
    if len(user.strip()) == 0:
        user = "Usuári@"
    return user


def _get_db_path() -> str:
    """ Monta caminho da base de dados
    :return: /.../product_crud/data/stock.db
    """
    root_dir = pathlib.Path(__file__).parent.parent.resolve()
    return os.path.join(root_dir, "data", "stock.db")
