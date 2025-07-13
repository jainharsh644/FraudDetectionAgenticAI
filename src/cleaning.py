import pandas as pd

def clean_data(df):
    print(f"➡️ Original shape: {df.shape}")
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Strip whitespace from strings
    str_cols = df.select_dtypes(include='object').columns
    for col in str_cols:
        df[col] = df[col].str.strip()
    
    # Amount cleanup
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    median_amt = df['amount'].median()
    df['amount'].fillna(median_amt, inplace=True)
    df = df[df['amount'] >= 0]
    q99 = df['amount'].quantile(0.99)
    df.loc[df['amount'] > q99, 'amount'] = q99
    
    # Country
    if 'country' in df.columns:
        df['country'] = df['country'].str.upper().fillna('UNKNOWN')
    
    # Timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    
    # Merchant category
    if 'merchant_category' in df.columns:
        df['merchant_category'] = df['merchant_category'].str.lower().fillna('unknown')
    
    # Device & IP fallback
    for col in ['device_id', 'ip_address']:
        if col in df.columns:
            df[col] = df[col].fillna('unknown')
    
    print(f"✅ Cleaned shape: {df.shape}")
    return df
