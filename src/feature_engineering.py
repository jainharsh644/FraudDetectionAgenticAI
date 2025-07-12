def engineer_features(df):
    df['txn_hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['night_txn'] = (df['txn_hour'] < 6).astype(int)

    risky_categories = ["JEWELRY", "LUXURY", "ELECTRONICS"]
    df['risky_category'] = df['merchant_category'].str.upper().isin(risky_categories).astype(int)

    # velocity: number of transactions for customer in last 1 day
    df = df.sort_values(by=['customer_id', 'timestamp'])
    df['txn_count_24h'] = (
        df.set_index('timestamp')
          .groupby('customer_id')['transaction_id']
          .rolling('1d').count()
          .reset_index(level=0, drop=True)
    )
    df['txn_count_24h'].fillna(0, inplace=True)

    # geo mismatch flag
    df['geo_mismatch'] = df.groupby('customer_id')['country'] \
                           .transform(lambda x: (x != x.shift()).astype(int))

    # device usage frequency
    device_freq = df.groupby('device_id')['transaction_id'].transform('count')
    df['device_usage_count'] = device_freq

    return df
