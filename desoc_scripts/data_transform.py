import pandas as pd

# Define functions to extract the hour, day of the week, and month from the timestamp
def extract_hour(timestamp):
    return timestamp.hour

def extract_day_of_week(timestamp):
    return timestamp.weekday()

def extract_month(timestamp):
    return timestamp.month

# ----analyze by hour -----
df = pd.read_csv("casts_output.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].apply(extract_hour)
casts_df_hour = df[df['parent_hash_encode'].isnull()]
reply_df_hour = df[df['parent_hash_encode'].notnull()]
casts_count_hour = casts_df_hour.groupby('hour').size().reset_index(name='casts_c')
reply_count_hour = reply_df_hour.groupby('hour').size().reset_index(name='reply_c')
result_df_hour = casts_count_hour.merge(reply_count_hour, on='hour', how='left')
result_df_hour.to_csv("casts_by_hour.csv", index=False)
print("Processing completed and saved to casts_by_hour.csv")

# ----analyze by week-----
df['day_of_week'] = df['timestamp'].apply(extract_day_of_week)
casts_df_dow = df[df['parent_hash_encode'].isnull()]
reply_df_dow = df[df['parent_hash_encode'].notnull()]
casts_count_dow = casts_df_dow.groupby('day_of_week').size().reset_index(name='casts_c')
reply_count_dow = reply_df_dow.groupby('day_of_week').size().reset_index(name='reply_c')
result_df_dow = casts_count_dow.merge(reply_count_dow, on='day_of_week', how='left')
result_df_dow.to_csv("casts_by_day_of_week.csv", index=False)
print("Processing completed and saved to casts_by_day_of_week.csv")

# ----analyze by month-----
df = pd.read_csv('casts_output.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
reply_df = df[df['parent_hash_encode'].notnull()]
reply_df = reply_df.groupby(reply_df['timestamp'].dt.to_period("M")).size().reset_index(name='reply_c')
reply_df.columns = ['month', 'reply_c']
cast_count_df = df[df['parent_hash_encode'].isnull()]
cast_count_df = cast_count_df.groupby(cast_count_df['timestamp'].dt.to_period("M")).size().reset_index(name='casts_c')
cast_count_df.columns = ['month', 'casts_c']
result_df_month = reply_df.merge(cast_count_df, on='month', how='outer').sort_values(by='month')
result_df_month['total'] = result_df_month['reply_c'].fillna(0) + result_df_month['casts_c'].fillna(0)
result_df_month['rolling_sum'] = result_df_month['total'].cumsum()
result_df_month.to_csv("casts_by_month.csv", index=False)
print("Processing completed and saved to casts_by_month.csv")