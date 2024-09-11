# pyramid_score/price_elasticity.py

import pandas as pd
import numpy as np

class PriceElasticity:
    """
    Classe para calcular a elasticidade-preço da demanda com base nos dados do cliente.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo os dados históricos de transações.
    customer_id : str
        Nome da coluna que identifica os clientes.
    price : str
        Nome da coluna que contém os preços.
    quantity : str
        Nome da coluna que contém a quantidade demandada.

    Methods
    -------
    calculate_elasticity(customer_id)
        Calcula a elasticidade-preço de um cliente específico.
    """

    def __init__(self, df: pd.DataFrame, customer_id: str, price: str, quantity: str):
        self.df = df
        self.customer_id = customer_id
        self.price = price
        self.quantity = quantity

    def calculate_elasticity(self, customer_id: str) -> float:
        """
        Calcula a elasticidade-preço de um cliente específico.

        Parameters
        ----------
        customer_id : str
            O ID do cliente para calcular a elasticidade.

        Returns
        -------
        float
            O valor da elasticidade-preço.
        """
        df_customer = self.df[self.df[self.customer_id] == customer_id].sort_values(by=self.price)
        
        if len(df_customer) < 2:
            raise ValueError("O cliente precisa ter pelo menos duas transações com preços diferentes para calcular a elasticidade.")
        
        # Calculando as variações percentuais de preço e quantidade
        df_customer['price_change_pct'] = df_customer[self.price].pct_change()
        df_customer['quantity_change_pct'] = df_customer[self.quantity].pct_change()

        # Remover linhas com NaN nas variações percentuais
        df_customer = df_customer.dropna(subset=['price_change_pct', 'quantity_change_pct'])
        
        # Elasticidade = %ΔQ / %ΔP
        elasticity = df_customer['quantity_change_pct'].mean() / df_customer['price_change_pct'].mean()
        
        return elasticity
