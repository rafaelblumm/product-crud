import streamlit as st
import pandas as pd


def show(db):
    """ Exibe listagem de produtos
    :param db: Instância do banco de dados 
    """
    _show_remove_button(db)
    should_reload = st.button("Recarregar", key="reload_products")
    if should_reload or "product_df" not in st.session_state:
        st.session_state["product_df"] = _build_dataframe(db.list_products())
    
    st.dataframe(
        st.session_state["product_df"],
        hide_index=True
    )


def _show_remove_button(db) -> None:
    """ Cria botão para remover produto
    :param db: Instância do banco de dados 
    """
    with st.popover("Remover produto"):
        id = st.number_input("ID do produto", min_value=0)
        if id:
            st.session_state["product"] = db.search_product(id)
        if "product" in st.session_state and st.session_state["product"] is None:
            st.error("Produto não encontrado")
        elif "product" in st.session_state:
            product = st.session_state["product"]
            if st.button("Deletar", type="primary"):
                if db.delete(product):
                    st.success("Produto removido com sucesso", icon="✅")
                    for key in ["product", "product_df"]:
                        del st.session_state[key]
                else:
                    st.error("Erro ao remover produto", icon="🚨")
            for line in product.__str__().split("\n"):
                st.write(line)


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
            "Categoria": [f"{p.category.id}-{p.category.description}" for p in products],
            "Qnt por unidade": [p.quantity_per_unit for p in products],
            "Preço unitário": [p.unit_price for p in products],
            "Em estoque": [p.stock for p in products],
            "Vendidos": [p.orders for p in products],
            "Dias até reposição": [p.reorder_days for p in products],
            "Descontinuado": [p.discontinued for p in products]
        }
    )
