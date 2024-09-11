import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

class RFV10:
    def __init__(self, df, customer_id, transaction_date, amount, automated=True):
        self.df = df
        self.customer_id = customer_id
        self.transaction_date = transaction_date
        self.amount = amount
        
        if automated:
            df_grp = self.produce_rfv_dataset(df)
            df_grp = self.calculate_rfv_score_percentiles(df_grp)
            self.rfv_table = self.assign_uniform_class(df_grp)

    def produce_rfv_dataset(self, df):
        df = df.copy()
        for col in df.columns:
            if col != self.customer_id and df[col].dtype == 'float64':
                df[col] = df[col].astype(str).apply(lambda x: x.strip()[:-2] if '.0' in x else x.strip())
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col])
    
        df = df.sort_values(by=self.transaction_date, ascending=False)
        df[self.amount] = df[self.amount].apply(lambda x: float(x) if x not in ['', 'nan'] else 0)
        df = df.dropna(subset=[self.customer_id, self.amount])
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        df[self.customer_id] = df[self.customer_id].astype(str).apply(lambda x: x.strip()[:-2] if '.0' in x else x.strip())
        df_grp = df.groupby(self.customer_id).agg({
            self.transaction_date: lambda x: (df[self.transaction_date].max() - x.max()).days,
            self.amount: ['count', 'sum']
        }).reset_index()
        df_grp.columns = [self.customer_id, 'recency', 'frequency', 'monetary_value']
        return df_grp
    
    def calculate_rfv_score_percentiles(self, df):
        df['r_score'] = pd.qcut(df['recency'], 10, labels=range(10, 0, -1))
        df['f_score'] = pd.qcut(df['frequency'], 10, labels=range(1, 11))
        df['v_score'] = pd.qcut(df['monetary_value'], 10, labels=range(1, 11))
        return df

    def assign_uniform_class(self, df):
        class_name = {
                        'classe 1': 'Potential Champions',
                        'classe 2': 'Loyal Accounts',
                        'classe 3': 'Low Spenders',
                        'classe 4': 'Potential',
                        'classe 5': 'Promising',
                        'classe 6': 'Standard Client',
                        'classe 7': 'Need Attention',
                        'classe 8': 'About to Sleep',
                        'classe 9': 'At Risk',
                        'classe 10': 'Potential Lost'}
        df['composite_score'] = (df['r_score'].astype(int) + df['f_score'].astype(int) + df['v_score'].astype(int))/3
        df['class'] = pd.qcut(df['composite_score'], 10, labels=[f'classe {i}' for i in range(1, 11)])
        df['class'] = df['class'].map(class_name)
        return df

    def find_customers(self, classe:str)->pd.DataFrame:
        """
        find_customers(classe)
        |  returns dataframe of entered classe
        |  Parameters:
        |  ----------
        |  classe : str, one of the 10 categories : ['Potential Champions', 'Loyal Accounts', 'Low Spenders', 'Potential', 'Promising', 'Standard Client', 'Need Attention', 'About to Sleep', 'At Risk', 'Potential Lost']
        |  Returns dataframe of customers with specified classe
        """
        return self.rfv_table[self.rfv_table['class'] == classe].reset_index(drop=True)