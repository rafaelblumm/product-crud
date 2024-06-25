import os
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
        user = getpass.getuser()
        if len(user.strip()) == 0:
            user = "Usuári@"
        return user
    
    return st.session_state["username"]
