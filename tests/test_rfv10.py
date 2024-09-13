# tests/test_rfv10.py
import pandas as pd
from pyramid_score.rfv10 import RFV10

def test_rfv10_analysis():
    # Criação de dados sintéticos
    data = {
        'customer_id': ['A', 'B', 'C', 'D'],
        'transaction_date': ['2022-01-01', '2022-03-01', '2022-05-01', '2022-07-01'],
        'amount': [100, 150, 200, 250]
    }
    df = pd.DataFrame(data)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])

    # Testando a análise RFV10
    rfv10_analysis = RFV10(df, 'customer_id', 'transaction_date', 'amount')
    
    assert not rfv10_analysis.rfv_table.empty
    print(rfv10_analysis.rfv_table.head())

    # Testando a função de encontrar clientes por classe
    customers = rfv10_analysis.find_customers('Loyal Accounts')
    print(customers)
