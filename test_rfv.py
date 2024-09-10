# tests/test_rfv.py
import pandas as pd
from rfm_pyramid_score.rfv import RFV

def test_rfv_analysis():
    # Criação de dados sintéticos
    data = {
        'customer_id': ['A', 'B', 'C', 'D'],
        'transaction_date': ['2022-01-01', '2022-03-01', '2022-05-01', '2022-07-01'],
        'amount': [100, 150, 200, 250]
    }
    df = pd.DataFrame(data)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Testando a análise RFV
    rfv_analysis = RFV(df, 'customer_id', 'transaction_date', 'amount')
    
    assert not rfv_analysis.rfm_table.empty
    assert not rfv_analysis.segment_table.empty
    print(rfv_analysis.rfm_table.head())
