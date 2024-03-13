import requests
from pprint import pformat

station_id = "44t"
param = "PM25"
data_type = "hr"
start_date = "2024-02-01"
end_date = "2024-02-29"
start_time = "00"
end_time = "23"
url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()
# print(pformat(response_json))

import pandas as pd
df = pd.DataFrame.from_dict(response_json["stations"][0]["data"])

# claen data
# O3_mean = df['O3'].mean()
# print(O3_mean)

# df['O3'].fillna(O3_mean, inplace=True)
# print(df)

# print(df['O3'].isnull().sum())

print(pformat(df))
df.to_csv(f"air4thai{start_date}TO{end_date}.csv")
