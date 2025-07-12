import pandas as pd

def clean_data(df):
    df = df.drop_duplicates()
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['amount'].fillna(df['amount'].median(), inplace=True)
    df['country'] = df['country'].str.upper()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df[df['amount'] >= 0]
    cap = df['amount'].quantile(0.99)
    df.loc[df['amount'] > cap, 'amount'] = cap
    return df
