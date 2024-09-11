import pandas as pd

class PyramidScoreAnalysis:
    """
    Classe para realizar análise de Pyramid Score (Recência, Frequência e Valor Monetário) e segmentação de clientes.

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
        Se True (padrão), realiza todas as operações automaticamente.
        Se False, permite executar cada operação manualmente.

    Attributes
    ----------
    pyramid_score_table : pd.DataFrame
        DataFrame contendo os scores e segmentos de Pyramid Score para cada cliente.
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
            df_grp = self._produce_pyramid_score_dataset(self.df)
            df_grp = self._calculate_pyramid_score(df_grp)
            self.pyramid_score_table = self._assign_segments(df_grp)
            self.segment_table = self._get_segment_distribution(self.pyramid_score_table)
    
    def _produce_pyramid_score_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepara o dataset de Pyramid Score a partir dos dados brutos de transações.

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

    def _calculate_pyramid_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula os scores de Pyramid Score e distribui os clientes em uma pirâmide de valor baseada em percentuais.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame com os valores de recência, frequência e valor monetário.

        Returns
        -------
        pd.DataFrame
            DataFrame com os scores calculados e a classificação em faixas.
        """
        # Calcular o score total como uma soma ponderada das métricas (ajustável)
        df['pyramid_score'] = df['recency'] * 0.15 + df['frequency'] * 0.28 + df['monetary_value'] * 0.57

        # Ordenar os clientes pelo pyramid_score (quanto maior o score, mais valioso o cliente)
        df = df.sort_values(by='pyramid_score', ascending=False).reset_index(drop=True)

        # Definir os percentuais acumulados
        total_customers = len(df)
        percentiles = [0.005, 0.015, 0.03, 0.05, 0.10, 0.15, 0.20, 0.15, 0.10, 0.20]
        cumulative_percentiles = np.cumsum([int(p * total_customers) for p in percentiles])

        # Classificar os clientes nas faixas de valor com os rótulos definidos
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
            'Platinum Tier', 'Gold Tier', 'Silver Tier', 'Bronze Tier', 'Prime Clients', 
            'Core Clients', 'Entry-Level Clients', 'Low Contribution', 'Minimal Value', 'Residual Tier'
        ]

        df['segment'] = np.select(conditions, labels, default='Other')

        return df

    def _assign_segments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Segmenta os clientes de acordo com os scores Pyramid Score e pirâmide de valor.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame com os scores e as faixas de valor.

        Returns
        -------
        pd.DataFrame
            DataFrame contendo os clientes e seus segmentos correspondentes.
        """
        return df  # Agora o DataFrame já tem a segmentação com base na pirâmide

    def _get_segment_distribution(self, df: pd.DataFrame) -> pd.DataFrame:
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
        return self.pyramid_score_table[self.pyramid_score_table['segment'] == segment].reset_index(drop=True)
