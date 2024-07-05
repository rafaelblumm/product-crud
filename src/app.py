import os
import pathlib
import streamlit as st
import util
from product import Category, Product
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

    db = Database.get(util._get_db_path())
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
        _show_product_list()

    with tabs[1]:
        _show_category_list()

    with tabs[2]:
        _show_product_form(db)

    with tabs[3]:
        _show_about()


def _show_product_list():
    """ Exibe listagem de produtos
    """
    st.error("Not implemented")


def _show_category_list():
    """ Exibe listagem de categorias
    """
    st.error("Not implemented")


def _show_product_form(db: Database):
    """ Exibe formulário para inserir novo produto
    :param db: Instância do banco de dados
    """
    with st.form("product_form", clear_on_submit=True):
        if "categories" not in st.session_state:
            category_map = {}
            categories = db.list_categories()
            if len(categories) == 0:
                db.insert(Category("Geral"))
                categories = db.list_categories()

            for c in categories:
                category_map[c.description] = c
            st.session_state["categories"] = category_map

        st.write("Insira os dados do novo produto")

        name = st.text_input(
            "Nome",
            max_chars=100
        )
        supplier_id = st.number_input(
            label="ID de fornecedor",
            min_value=1,
            max_value=2147483647,
            step=1
        )
        category_descriptions = list(st.session_state["categories"].keys())
        category_descriptions.sort()
        category = st.selectbox(
            "Categoria",
            category_descriptions,
            index=None,
            placeholder="Selecione a categoria"
        )
        quantity_per_unit = st.number_input(
            label="Quantidade por unidade (Kg, Ml)",
            min_value=0.0,
            max_value=2147483647.0,
            step=1.0
        )
        unit_price = st.number_input(
            label="Preço unitário",
            min_value=0.01,
            max_value=2147483647.0,
            step=0.01
        )
        stock = st.number_input(
            label="Unidades em estoque",
            min_value=0,
            max_value=2147483647,
            step=1
        )
        orders = st.number_input(
            label="Unidades vendidas",
            min_value=0,
            max_value=2147483647,
            step=1
        )
        reorder_days = st.number_input(
            label="Dias de espera até reabastecimento do estoque",
            min_value=0,
            max_value=2147483647,
            step=1
        )
        discontinued = st.checkbox(
            "Produto descontinuado",
            value=False
        )

        submit_button = st.form_submit_button("Submit")
        if submit_button:
            p = Product(
                name,
                supplier_id,
                st.session_state["categories"].get(category),
                quantity_per_unit,
                unit_price,
                stock,
                orders,
                reorder_days,
                discontinued
            )
            if db.insert(p):
                st.success(
                    "Produto gravado com sucesso",
                    icon="✅"
                )


def _show_about():
    """ Exibe dados sobre o projeto
    """
    st.error("Not implemented")
