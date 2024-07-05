import streamlit as st
import util

def login_page():
    """ Exibe página de login.
    Se estiver em modo dev, assume nome padrão para o usuário
    """
    if util.is_dev_mode():
        st.session_state["username"] = util.get_username()
        return

    _configure_page()
    st.title("Bem-vindo ao :green[cadastro de produtos]!")
    st.subheader("Informe seu nome para prosseguir")
    name_input = st.text_input("Nome de usuário",
                               max_chars=50,
                               placeholder=util.get_default_username())
    submit_button = st.button("Acessar", type="primary")

    if (submit_button or name_input) and _is_valid_name(name_input):
        st.session_state["username"] = name_input


def _configure_page():
    """ Configura a página
    """
    st.set_page_config(
        page_title="Cadastro de produtos",
        page_icon=":package:",
    )


def _is_valid_name(name: str) -> bool:
    """ Valida nome de usuário
        :param name: Nome do usuário
        :return: Indica se nome de usuário é válido
    """
    return len(name) > 0
