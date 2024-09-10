# rfm_pyramid_score/churn_prediction.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

class ChurnPrediction:
    """
    Classe para calcular a probabilidade de churn (cancelamento) usando um modelo preditivo.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo os dados de transações e comportamentos.
    target : str
        Nome da coluna que contém a variável de churn (0 = não churn, 1 = churn).

    Methods
    -------
    train_model(features)
        Treina o modelo preditivo de churn usando os comportamentos dos clientes.
    
    predict_churn(customer_data)
        Calcula a probabilidade de churn para um cliente específico.
    
    identify_churn_signs(customer_data)
        Identifica os sinais de churn com base em quedas na frequência de compra e valores gastos.
    """

    def __init__(self, df: pd.DataFrame, target: str):
        self.df = df
        self.target = target
        self.model = None

    def train_model(self, features: list):
        """
        Treina o modelo de regressão logística para prever churn.

        Parameters
        ----------
        features : list
            Lista de colunas com as variáveis preditoras para o modelo.

        Returns
        -------
        dict
            Resultados de avaliação do modelo.
        """
        X = self.df[features]
        y = self.df[self.target]

        # Dividindo o conjunto de dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Treinando o modelo de regressão logística
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

        # Fazendo previsões
        y_pred = self.model.predict(X_test)

        # Avaliação do modelo
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        return {"accuracy": accuracy, "report": report}

    def predict_churn(self, customer_data: pd.DataFrame) -> float:
        """
        Calcula a probabilidade de churn para um cliente específico.

        Parameters
        ----------
        customer_data : pd.DataFrame
            Dados do cliente para prever o churn.

        Returns
        -------
        float
            Probabilidade de churn (0 a 1).
        """
        if self.model is None:
            raise ValueError("O modelo de churn não foi treinado. Treine o modelo antes de fazer previsões.")
        
        churn_prob = self.model.predict_proba(customer_data)[:, 1]
        return churn_prob[0]

    def identify_churn_signs(self, customer_data: pd.DataFrame) -> dict:
        """
        Identifica sinais de churn, como quedas na frequência de compra e valores gastos.

        Parameters
        ----------
        customer_data : pd.DataFrame
            Dados históricos de transações do cliente.

        Returns
        -------
        dict
            Dicionário com os indícios de churn (frequência e valor médio).
        """
        # Calcular a variação da frequência de compra e do valor médio gasto
        freq_change = customer_data['frequency'].pct_change().iloc[-1]
        value_change = customer_data['monetary_value'].pct_change().iloc[-1]

        churn_signs = {
            "frequency_drop": freq_change < -0.5,  # Se a frequência cair mais de 50%
            "value_drop": value_change < -0.5      # Se o valor gasto cair mais de 50%
        }

        return churn_signs
