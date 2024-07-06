import streamlit as st

from database import Database
from product import Category, Product


STATUS_KEY = "status_ok"
MSG_KEY = "msg"


def show(db: Database):
    """ Exibe formulário para inserir novo produto
    :param db: Instância do banco de dados
    """
    with st.form("product_form", clear_on_submit=True):
        category_descriptions = _get_category_descriptions(db)

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
        category = st.selectbox(
            "Categoria",
            category_descriptions,
            index=0,
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

        submit_button = st.form_submit_button("Novo produto")
        if submit_button:
            selected_category = st.session_state["categories"].get(category)
            p = Product(
                name, supplier_id, selected_category, quantity_per_unit,
                unit_price, stock, orders, reorder_days, discontinued
            )
            status = _submit(p, db)
            if status.get(STATUS_KEY):
                st.success(status.get(MSG_KEY), icon="✅")
            else:
                st.error(status.get(MSG_KEY), icon="🚨")


def _get_category_descriptions(db):
    """ Busca as descrições das categorias disponíveis
    :param db: Instância do banco de dados
    :return: Lista de descrições
    """
    if "categories" not in st.session_state:
        category_map = {}
        categories = db.list_categories()
        if len(categories) == 0:
            db.insert(Category("Geral"))
            categories = db.list_categories()

        for c in categories:
            category_map[f"{c.id}-{c.description}"] = c
        st.session_state["categories"] = category_map

    category_descriptions = list(st.session_state["categories"].keys())
    category_descriptions.sort()

    return category_descriptions


def _submit(p: Product, db: Database) -> dict:
    """ Grava produto no banco de dados
    :param p: Produto
    :param db: Banco de dados
    :return: Status e mensagem da operação
    """
    if len(p.name) == 0:
        return {
            STATUS_KEY: False,
            MSG_KEY: "É necessário informar um nome de produto"
        }
    
    if p.category is None:
        return {
            STATUS_KEY: False,
            MSG_KEY: "Categoria inválida"
        }
        
    if db.insert(p):
        del st.session_state["product_df"]
        return {
            STATUS_KEY: True,
            MSG_KEY: "Produto gravado com sucesso"
        }
    
    return {
        STATUS_KEY: False,
        MSG_KEY: "Erro ao inserir registro"
    }
