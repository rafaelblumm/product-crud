import streamlit as st
import pandas as pd


def show(db):
    """ Exibe listagem de produtos
    :param db: Instância do banco de dados 
    """
    if "product_df" not in st.session_state:
        st.session_state["product_df"] = _build_dataframe(db.list_products())
    
    st.dataframe(
        st.session_state["product_df"],
        hide_index=True
    )


def _build_dataframe(products: list) -> pd.DataFrame:
    """ Cria DataFrame de produtos
    :param products: Lista de produtos
    :return: DataFrame
    """
    return pd.DataFrame(
        {
            "ID": [p.id for p in products],
            "Nome": [p.name for p in products],
            "ID de fornecedor": [p.supplier_id for p in products],
            "Categoria": [p.category.description for p in products],
            "Qnt por unidade": [p.quantity_per_unit for p in products],
            "Preço unitário": [p.unit_price for p in products],
            "Em estoque": [p.stock for p in products],
            "Vendidos": [p.orders for p in products],
            "Dias até reposição": [p.reorder_days for p in products],
            "Descontinuado": [p.discontinued for p in products]
        }
    )
    