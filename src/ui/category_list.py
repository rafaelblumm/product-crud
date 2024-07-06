import streamlit as st
import pandas as pd


def show(db):
    """ Exibe listagem de categorias
    :param db: Instância do banco de dados 
    """
    _show_create_button(db)
    _show_remove_button(db)
    if "category_df" not in st.session_state:
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
        st.error("Not implemented")


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