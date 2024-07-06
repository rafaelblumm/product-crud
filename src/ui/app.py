import os
import pathlib
import streamlit as st
import util
import ui.product_form as product_form
import ui.product_list as product_list
import ui.category_list as category_list
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

        if st.button("Encerrar sessão"):
            st.session_state["database"].disconnect()
            st.stop()


def _configure_main_container():
    """ Configura container principal da tela
    """
    st.header(f"Bem-vindo(a), {util.get_username()}!")

    tabs = st.tabs([
        "Listagem de produtos",
        "Listagem de categorias",
        "Inserir produto"
    ])

    db = st.session_state["database"]
    with tabs[0]:
        product_list.show(db)

    with tabs[1]:
        category_list.show(db)

    with tabs[2]:
        product_form.show(db)
