import streamlit as st
import util

def run_app():
    """ Executa a página principal
    """
    _configure_page()
    _configure_sidebar()
    st.header(f"Bem-vindo(a), {util.get_username()}!")


def _configure_page():
    """ Configura a página
    """
    st.set_page_config(
        page_title="Cadastro de produtos",
        page_icon=":package:",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def _configure_sidebar():
    """ Configura a barra lateral da página
    """
    with st.sidebar:
        st.title("Cadastro de produtos")
        st.divider()

        st.caption("Engenharia de software: Análise (2024/01)")
        st.divider()
        st.caption("Felipe Braun Hinkel")
        st.caption("Luidi Bahia Kleemann")
        st.caption("Murilo Denech Longue")
        st.caption("Rafael Flores Blumm")
