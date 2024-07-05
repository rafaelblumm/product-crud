import streamlit as st
import util


def run_app():
    """ Executa a página principal
    """
    _configure_page()
    _configure_sidebar()
    _configure_main_container()


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


def _configure_main_container():
    """ Configura container principal da tela
    """
    st.header(f"Bem-vindo(a), {util.get_username()}!")

    tabs = st.tabs([
        "Listagem de produtos",
        "Listagem de categorias",
        "Inserir produto",
        "Sobre"
    ])

    with tabs[0]:
        _show_product_list()

    with tabs[1]:
        _category_list()

    with tabs[2]:
        _show_product_form()

    with tabs[3]:
        _show_about()


def _show_product_list():
    """ Exibe listagem de produtos
    """
    st.error("Not implemented")


def _category_list():
    """ Exibe listagem de categorias
    """
    st.error("Not implemented")


def _show_product_form():
    """ Exibe formulário para inserir novo produto
    """
    st.error("Not implemented")


def _show_about():
    """ Exibe dados sobre o projeto
    """
    st.error("Not implemented")
