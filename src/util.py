import os
import pathlib
import streamlit as st
import getpass


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


def bool_to_int(val: bool) -> int:
    """ Converte valor booleano para inteiro
    :param val: Booleano a ser convertido
    :return: 1 para True e 0 para False
    """
    return 1 if val else 0


def int_to_bool(val: int) -> int:
    """ Converte valor inteiro para booleano
    :param val: Inteiro a ser convertido
    :return: True para 1 e False para 0
    """
    return val == 1
