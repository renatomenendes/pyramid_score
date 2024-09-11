# pyramid_score/price_corridor.py

import pandas as pd

class PriceCorridor:
    """
    Classe para calcular o corredor de preços (preço mínimo e máximo) das transações de um cliente.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo os dados de transações.
    customer_id : str
        Nome da coluna que identifica os clientes.
    price : str
        Nome da coluna que contém os preços.

    Methods
    -------
    get_price_corridor(customer_id)
        Retorna o preço mínimo e máximo aceito por um cliente específico.
    """

    def __init__(self, df: pd.DataFrame, customer_id: str, price: str):
        self.df = df
        self.customer_id = customer_id
        self.price = price

    def get_price_corridor(self, customer_id: str) -> dict:
        """
        Calcula o preço mínimo e máximo que o cliente pagou.

        Parameters
        ----------
        customer_id : str
            O ID do cliente para o qual calcular o corredor de preços.

        Returns
        -------
        dict
            Dicionário contendo o preço mínimo e o preço máximo aceitos pelo cliente.
        """
        df_customer = self.df[self.df[self.customer_id] == customer_id]
        
        if df_customer.empty:
            raise ValueError("Nenhuma transação encontrada para o cliente fornecido.")
        
        min_price = df_customer[self.price].min()
        max_price = df_customer[self.price].max()

        return {"min_price": min_price, "max_price": max_price}
