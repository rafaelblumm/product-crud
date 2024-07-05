class Category:
    """ Classe que representa a categoria de um produto
    """

    def __init__(self, description: str, id: int = 0) -> None:
        """ Cria nova categoria
        """
        self.description = description
        self.id = id


    def __str__(self) -> str:
        return f"""id={self.id}
description={self.description}"""
        

    def from_db(row: str):
        """ Construtor a partir de linha do banco de dados
        :param row: Linha do banco de dados
        """
        return Category(row[1], id = row[0])


class Product:
    """ Classe que representa um produto no banco de dados
    """

    def __init__(self,
                 name: str,
                 supplier_id: int,
                 category: Category,
                 quantity_per_unit: float,
                 unit_price: float,
                 stock: int,
                 orders: int,
                 reorder_days: int,
                 discontinued: bool,
                 id: int = 0) -> None:
        """ Cria novo produto
        """
        self.name = name
        self.supplier_id = supplier_id
        self.category = category
        self.quantity_per_unit = quantity_per_unit
        self.unit_price = unit_price
        self.stock = stock
        self.orders = orders
        self.reorder_days = reorder_days
        self.discontinued = discontinued
        self.id = id
    

    def from_db(row: str):
        """ Construtor a partir de linha do banco de dados
        :param row: Linha do banco de dados
        """
        return Product(
            row[1], row[2], row[3], row[4], row[5], row[6],
            row[7], row[8], row[9], id = row[0]
        )
    

    def __str__(self) -> str:
        return f"""id={self.id}
name={self.name}
supplier_id={self.supplier_id}
category={self.category}
quantity_per_unit={self.quantity_per_unit}
unit_price={self.unit_price}
stock={self.stock}
orders={self.orders}
reorder_days={self.reorder_days}
discontinued={self.discontinued}"""