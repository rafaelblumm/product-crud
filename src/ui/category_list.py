import streamlit as st
import pandas as pd

from product import Category


def show(db):
    """ Exibe listagem de categorias
    :param db: Instância do banco de dados 
    """
    _show_create_button(db)
    _show_remove_button(db)
    should_reload_categories = st.button("Recarregar", key="reload_categories")
    if should_reload_categories or "category_df" not in st.session_state:
        st.session_state["category_df"] = _build_dataframe(db.list_categories())
    
    st.dataframe(
        st.session_state["category_df"],
        hide_index=True
    )


def _show_create_button(db):
    """ Exibe botão para criar categoria
    :param db: Instância do banco de dados 
    """
    with st.popover("Nova categoria"):
        description = st.text_input("Descrição da categoria", max_chars=30)
        if description:
            if len(description) == 0:
                st.error("É necessário informar uma descrição")
            else:
                if db.insert(Category(description)):
                    del st.session_state["categories"]
                    st.success("Categoria adicionada com sucesso", icon="✅")
                else:
                    st.error("Erro ao adicionar categoria", icon="🚨")


def _show_remove_button(db):
    """ Exibe botão para remover categoria
    :param db: Instância do banco de dados 
    """
    with st.popover("Remover categoria"):
        st.error("Not implemented")


def _build_dataframe(categories: list) -> pd.DataFrame:
    """ Cria DataFrame de categorias
    :param categories: Lista de categorias
    :return: DataFrame
    """
    return pd.DataFrame(
        {
            "ID": [c.id for c in categories],
            "Descrição": [c.description for c in categories]
        }
    )