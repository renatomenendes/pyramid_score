import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

class RFMAnalysis:
    """
    Classe para realizar análise RFM (Recência, Frequência e Valor Monetário) e segmentação de clientes.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo os dados de transações.
    customer_id : str
        Nome da coluna que identifica os clientes.
    transaction_date : str
        Nome da coluna que contém as datas de transações.
    amount : str
        Nome da coluna que contém o valor das transações.
    automated : bool, optional
        Se True (padrão), realiza todas as operações automaticamente. Se False, permite executar cada operação manualmente.

    Attributes
    ----------
    rfm_table : pd.DataFrame
        DataFrame contendo os scores RFM e os segmentos para cada cliente.
    segment_table : pd.DataFrame
        DataFrame contendo a distribuição dos clientes por segmento.
    """
    
    def __init__(self, df: pd.DataFrame, customer_id: str, transaction_date: str, amount: str, automated=True):
        self.df = df
        self.customer_id = customer_id
        self.transaction_date = transaction_date
        self.amount = amount
        
        # Execução automática das operações
        if automated:
            df_grp = self.produce_rfm_dataset(self.df)
            df_grp = self.calculate_rfm_score_pyramid(df_grp)
            self.rfm_table = self.find_segments(df_grp)
            self.segment_table = self.find_segment_df(self.rfm_table)
    
    def produce_rfm_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara o dataset RFM a partir dos dados brutos de transações.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame contendo as transações dos clientes.

        Returns
        -------
        pd.DataFrame
            DataFrame com os valores de recência, frequência e valor monetário por cliente.
        """
        df = df.dropna(subset=[self.customer_id, self.amount])
        df[self.amount] = df[self.amount].astype(float)
        df[self.transaction_date] = pd.to_datetime(df[self.transaction_date])

        # Agrupamento por cliente e cálculo de recência, frequência e valor monetário
        df_grp = df.groupby(self.customer_id).agg({
            self.transaction_date: lambda x: (df[self.transaction_date].max() - x.max()).days,
            self.amount: ['count', 'sum']
        }).reset_index()

        df_grp.columns = [self.customer_id, 'recency', 'frequency', 'monetary_value']
        return df_grp

    def calculate_rfm_score_pyramid(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula os scores RFM e distribui os clientes em uma pirâmide de valor baseada em percentuais.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame com os valores de recência, frequência e valor monetário.

        Returns
        -------
        pd.DataFrame
            DataFrame com os scores RFM calculados e a classificação em faixas.
        """
        # Calcular o score total como uma soma ponderada das métricas RFM (ajustável)
        df['rfm_score'] = df['recency'] * 0.15 + df['frequency'] * 0.28 + df['monetary_value'] * 0.57

        # Ordenar os clientes pelo rfm_score (quanto maior o score, mais valioso o cliente)
        df = df.sort_values(by='rfm_score', ascending=False).reset_index(drop=True)

        # Definir os percentuais acumulados
        total_customers = len(df)
        percentiles = [0.005, 0.015, 0.03, 0.05, 0.10, 0.15, 0.20, 0.15, 0.10, 0.20]
        cumulative_percentiles = np.cumsum([int(p * total_customers) for p in percentiles])

        # Classificar os clientes nas faixas de valor
        conditions = [
            (df.index < cumulative_percentiles[0]),
            (df.index >= cumulative_percentiles[0]) & (df.index < cumulative_percentiles[1]),
            (df.index >= cumulative_percentiles[1]) & (df.index < cumulative_percentiles[2]),
            (df.index >= cumulative_percentiles[2]) & (df.index < cumulative_percentiles[3]),
            (df.index >= cumulative_percentiles[3]) & (df.index < cumulative_percentiles[4]),
            (df.index >= cumulative_percentiles[4]) & (df.index < cumulative_percentiles[5]),
            (df.index >= cumulative_percentiles[5]) & (df.index < cumulative_percentiles[6]),
            (df.index >= cumulative_percentiles[6]) & (df.index < cumulative_percentiles[7]),
            (df.index >= cumulative_percentiles[7]) & (df.index < cumulative_percentiles[8]),
            (df.index >= cumulative_percentiles[8])
        ]

        labels = [
            'Top 0.5%', 'Next 1.5%', 'Next 3%', 'Next 5%', 'Next 10%', 
            'Next 15%', 'Next 20%', 'Next 15%', 'Next 10%', 'Bottom 20%'
        ]

        df['segment'] = np.select(conditions, labels, default='Other')

        return df

    def find_segments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Segmenta os clientes de acordo com os scores RFM e pirâmide de valor.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame com os scores RFM e as faixas de valor.

        Returns
        -------
        pd.DataFrame
            DataFrame contendo os clientes e seus segmentos correspondentes.
        """
        return df  # Agora o DataFrame já tem a segmentação com base na pirâmide

    def find_segment_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Retorna a distribuição dos clientes por segmento.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame com os clientes e seus segmentos.

        Returns
        -------
        pd.DataFrame
            DataFrame com a contagem de clientes por segmento.
        """
        return df.groupby('segment').size().reset_index(name='no_of_customers')

    def find_customers(self, segment: str) -> pd.DataFrame:
        """
        Retorna os clientes pertencentes a um determinado segmento.

        Parameters
        ----------
        segment : str
            O nome do segmento a ser filtrado.

        Returns
        -------
        pd.DataFrame
            DataFrame com os clientes do segmento especificado.
        """
        return self.rfm_table[self.rfm_table['segment'] == segment].reset_index(drop=True)
