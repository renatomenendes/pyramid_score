# rfm_pyramid_score/group_price_corridor.py

import pandas as pd
import numpy as np

class GroupPriceCorridor:
    """
    Classe para calcular o corredor de preços (preço mínimo e máximo) de um grupo de clientes comparáveis,
    removendo outliers superiores e inferiores com base no IQR.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo os dados de transações.
    segment : str
        Nome da coluna que identifica os segmentos dos clientes.
    price : str
        Nome da coluna que contém os preços.

    Methods
    -------
    get_price_corridor(segment)
        Retorna o preço mínimo e máximo aceito por clientes comparáveis dentro do mesmo segmento, removendo outliers.
    """

    def __init__(self, df: pd.DataFrame, segment: str, price: str):
        self.df = df
        self.segment = segment
        self.price = price

    def _remove_outliers(self, df: pd.DataFrame, price_col: str) -> pd.DataFrame:
        """
        Remove os outliers usando o método do Interquartile Range (IQR).

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame do grupo com os preços.
        price_col : str
            Nome da coluna de preços.

        Returns
        -------
        pd.DataFrame
            DataFrame sem outliers.
        """
        Q1 = df[price_col].quantile(0.25)
        Q3 = df[price_col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filtra o DataFrame removendo outliers
        df_filtered = df[(df[price_col] >= lower_bound) & (df[price_col] <= upper_bound)]

        return df_filtered

    def get_price_corridor(self, segment: str) -> dict:
        """
        Calcula o preço mínimo e máximo aceito pelos clientes de um segmento específico,
        removendo outliers.

        Parameters
        ----------
        segment : str
            O segmento para o qual calcular o corredor de preços.

        Returns
        -------
        dict
            Dicionário contendo o preço mínimo e o preço máximo aceitos pelos clientes do segmento.
        """
        df_segment = self.df[self.df[self.segment] == segment]
        
        if df_segment.empty:
            raise ValueError(f"Nenhum cliente encontrado no segmento '{segment}'.")

        # Remove outliers de preços
        df_filtered = self._remove_outliers(df_segment, self.price)

        # Calcula o preço mínimo e máximo
        min_price = df_filtered[self.price].min()
        max_price = df_filtered[self.price].max()

        return {"min_price": min_price, "max_price": max_price}
