from product import Category, Product
from enum import Enum
import sqlite3

# https://awari.com.br/python-sqlite3-aprenda-a-utilizar-o-banco-de-dados-sqlite3-com-python/

class InvalidDatabase(Exception):
    """ Erro de opção inválida de banco de dados
    """
    def __init__(self, message):
        super().__init__(message)


class AvailableDatabases(Enum):
    """ Soluções disponíveis de banco de dados
    """
    SQLITE = 1


class Database:
    """ Classe abstrata que representa um banco de dados genérico
    :param path: Caminho do banco de dados
    """
    def __init__(self,  path: str) -> None:
        self.path = path
        self.conn = None

    def get(path: str, database_option: int = AvailableDatabases.SQLITE):
        """ Cria uma instância do banco de dados de acordo com a solução escolhida
        :param path: Caminho do banco de dados
        :param database_option: Tipo do banco de dados (opções em ```AvailableDatabases```)
        :retur: Instância do banco de dados
        """
        match database_option:
            case AvailableDatabases.SQLITE:
                return SQLite(path)
            case _:
                raise InvalidDatabase("Banco de dados inválido")

    
    def connect(self) -> None:
        raise NotImplementedError


    def disconnect(self) -> None:
        raise NotImplementedError
    

    def initialize_tables(self) -> bool:
        raise NotImplementedError

    
    def insert(self, product: Product) -> bool:
        raise NotImplementedError
    

    def delete(self, id: int) -> bool:
        raise NotImplementedError
    

    def update(self, new_product: Product) -> bool:
        raise NotImplementedError
    

    def list(self, ) -> list:
        raise NotImplementedError


class SQLite(Database):
    """ Classe que representa uma instância do banco de dados SQLite
    """
    def __init__(self, path: str) -> None:
        super().__init__(path)
    

    def connect(self) -> None:
        """ Conecta com o banco de dados
        :return: Se conectou com sucesso
        """
        self.conn = sqlite3.connect(self.path)
    

    def disconnect(self) -> None:
        """ Encerra conexão com o banco de dados
        """
        self.conn.close()


    def insert(self, item: Product | Category) -> bool:
        """ Insere item no banco de dados
        :param item: Item a ser inserido
        :return: Sucesso da operação
        """
        if isinstance(item, Product):
            result_ok = self._insert_product(item)
        if isinstance(item, Category):
            result_ok = self._insert_category(item)
        
        if result_ok:
            self.conn.commit()
            
        return result_ok


    def _insert_product(self, p: Product) -> bool:
        """ Insere produto no banco de dados
        :param p: Novo produto
        :return: Se conseguiu inserir o produto
        """
        sql = f"""
            INSERT INTO products (product_name, supplier_id, category_id, 
                quantity_per_unit, unit_price, units_in_stock,
                units_on_order, reorder_level, discontinued)
            VALUES ("{p.name}", {p.supplier_id}, {p.category.id},
                {p.quantity_per_unit}, {p.unit_price}, {p.stock},
                {p.orders}, {p.reorder_days}, {self._bool_to_int(p.discontinued)});
        """
        return self.conn.execute(sql).rowcount != 0
    

    def _insert_category(self, c: Category) -> bool:
        """ Insere categoria no banco de dados
        :param c: Nova categoria
        :return: Se conseguiu inserir a categoria
        """
        sql = f"""
            INSERT INTO categories (description)
            VALUES ("{c.description}")
        """
        return self.conn.execute(sql).rowcount != 0


    def delete(self, item: Product | Category) -> bool:
        """ Deleta um item
        :param item: Item a deletar
        :return: Sucesso da operação
        """
        if isinstance(item, Product):
            result_ok = self._delete_product(item)
        if isinstance(item, Category):
            result_ok = self._delete_category(item)
        
        if result_ok:
            self.conn.commit()
            
        return result_ok


    def _delete_product(self, p: Product) -> bool:
        """ Deleta produto
        :param p: Produto a deletar
        :return: Se conseguiu deletar o produto
        """
        sql = f"""
            DELETE
            FROM products
            WHERE product_id = {p.id};
        """
        return self.conn.execute(sql).rowcount != 0
    

    def _delete_category(self, c: Category) -> bool:
        """ Deleta categoria
        :param c: Categoria a deletar
        :return: Se conseguiu deletar a categoria
        """
        sql = f"""
            DELETE
            FROM categories
            WHERE category_id = {c.id};
        """
        return self.conn.execute(sql).rowcount != 0
    

    def update(self, item: Product | Category) -> bool:
        """ Atualiza um item
        :param item: Item a atualizar
        :return: Sucesso da operação
        """
        if isinstance(item, Product):
            result_ok =  self._update_product(item)
        if isinstance(item, Category):
            result_ok =  self._update_category(item)
        
        if result_ok:
            self.conn.commit()

        return result_ok

    
    def _update_product(self, p: Product) -> bool:
        """ Atualiza dados de um produto
        :param p: Produto com os novos dados
        :return: Se conseguiu atualizar o produto
        """
        sql = f"""
            UPDATE products
            SET product_name = "{p.name}", supplier_id = {p.supplier_id},
                category_id = {p.category.id}, quantity_per_unit = {p.quantity_per_unit},
                unit_price = {p.unit_price}, units_in_stock = {p.stock},
                units_on_order = {p.orders}, reorder_level = {p.reorder_days},
                discontinued = {self._bool_to_int(p.discontinued)}
            WHERE product_id = {p.id};
        """
        return self.conn.execute(sql).rowcount != 0
    

    def _update_category(self, c: Category) -> bool:
        """ Atualiza dados de uma categoria
        :param c: Categoria com os novos dados
        :return: Se conseguiu atualizar a categoria
        """
        sql = f"""
            UPDATE categories
            SET description = "{c.description}"
            WHERE category_id = {c.id}
        """
        return self.conn.execute(sql).rowcount != 0
    

    def list_products(self) -> list:
        """ Lista todos os produtos no banco de dados
        :return: Todos os produtos
        """
        products = []
        for row in self._list("products"):
            products.append(Product.from_db(row))

        return products
    

    def list_categories(self) -> list:
        """ Lista todas as categorias no banco de dados
        :return: Todas as categorias
        """
        categories = []
        for row in self._list("categories"):
            categories.append(Category.from_db(row))

        return categories
    
    
    def _list(self, table: str) -> sqlite3.Cursor:
        """ Lista todos os itens de uma tabela
        :param table: Nome da tabela
        :return: Cursor do resultado
        """
        sql = f"""
            SELECT *
            FROM {table};
        """
        return self.conn.execute(sql)


    def initialize_tables(self) -> None:
        """ Inicializa tabelas se não estiverem criadas
        """
        self._create_categories_table()
        self._create_products_table()

    
    def _create_categories_table(self) -> None:
        """ Cria tabela de categorias
        """
        sql = """
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL
            );
        """
        self.conn.execute(sql)

    
    def _create_products_table(self) -> None:
        """ Cria tabela de produtos
        """
        sql = """
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                supplier_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                quantity_per_unit INTEGER NOT NULL,
                unit_price INTEGER NOT NULL,
                units_in_stock INTEGER NOT NULL,
                units_on_order INTEGER NOT NULL,
                reorder_level INTEGER NOT NULL,
                discontinued INTEGER NOT NULL,
                CONSTRAINT products_categories_FK
                FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
            );
        """
        self.conn.execute(sql)


    def _bool_to_int(self, val: bool) -> int:
        """ Converte valor booleano para inteiro
        :param val: Booleano a ser convertido
        :return: 1 para True e 0 para False
        """
        return 1 if val else 0