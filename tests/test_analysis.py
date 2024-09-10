# tests/test_analysis.py
import pandas as pd
from rfm_pyramid_score import PyramidScoreAnalysis

def test_pyramid_analysis():
    # Criação de dados sintéticos simples
    data = {
        'customer_id': ['A', 'B', 'C'],
        'transaction_date': ['2021-01-01', '2021-06-01', '2021-12-01'],
        'amount': [100, 150, 200]
    }
    df = pd.DataFrame(data)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Teste da análise
    analysis = PyramidScoreAnalysis(df, 'customer_id', 'transaction_date', 'amount')
    assert analysis.pyramid_score_table is not None
