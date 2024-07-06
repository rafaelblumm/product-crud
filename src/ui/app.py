import os
import pathlib
import streamlit as st
import util
import ui.product_form as product_form
import ui.product_list as product_list
from database import Database


def run_app():
    """ Executa a página principal
    """
    _setup_db()
    _configure_page()
    _configure_sidebar()
    _configure_main_container()


def _setup_db():
    """ Configura acesso a banco de dados
    """
    if "database" in st.session_state:
        return
    
    db_path = util._get_db_path()
    data_dir = pathlib.Path(db_path).parent.resolve()
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    db = Database.get(db_path)
    db.connect()
    db.initialize_tables()
    st.session_state["database"] = db


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

    db = st.session_state["database"]
    with tabs[0]:
        product_list.show(db)

    with tabs[1]:
        _show_category_list()

    with tabs[2]:
        product_form.show(db)

    with tabs[3]:
        _show_about()


def _show_category_list():
    st.error("Not implemented")


def _show_about():
    """ Exibe dados sobre o projeto
    """
    st.error("Not implemented")
