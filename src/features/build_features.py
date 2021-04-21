import pandas as pd
from pathlib import Path
import json
from sklearn.preprocessing import MinMaxScaler

__all__ = ['Transform','Weekly']
PROJECT_DIR = Path(__file__).resolve().parents[2]

class Transform:
    def normalize(df,inverse=False):
        scaler = MinMaxScaler()
        scaler.fit(df)

        norm_array = scaler.transform(df)
        norm_df=pd.DataFrame(norm_array,index=df.index,columns=df.columns)
        
        return norm_df, scaler

class Weekly:
    def pivot_day_of_week(data_series,zip_code):
        df = data_series.copy().to_frame()
        df['weekday'] = df.index.dayofweek
        df['Date'] = df.index
        df['first_day_of_week'] =df.apply(lambda x:x['Date']-pd.Timedelta(days=x['weekday']),axis=1).drop(columns='Date')
        df = df.pivot(index='first_day_of_week',columns='weekday',values=zip_code).T
        df.columns = [col.strftime('%Y-%m-%d') for col in df.columns]
        return df

    def first_day_of_week(row):
        ans = row.index-pd.Timedelta(f'{row.index.dayofweek}')
        return ans

def process_covid_case(input_filename=f'{PROJECT_DIR}/data/raw/case_count.json',
                       output_filepath=f'{PROJECT_DIR}/data/interim/case_count.parquet'):
    with open(input_filename) as file:
        data = json.loads(file.read())

    data = pd.DataFrame(
        [item['properties'] for item in data['features']]
    )

    data = data.drop(columns=['Notes', 'FID']).rename(
        columns={'Date': 'Timestamp'})
    data.columns = [num.lstrip('Zip_') for num in data.columns]

    data['Timestamp'] = pd.to_datetime(data['Timestamp']).dt.normalize()
    data = data.set_index('Timestamp').sort_index().tz_localize(None)

    for col in data.columns:
        data[col] = data[col]-data[col].shift(1)
        data.loc[data[col] < 0, col] = 0
    data.to_parquet(output_filepath)


def main():
    process_covid_case()


if __name__ == "__main__":
    main()
