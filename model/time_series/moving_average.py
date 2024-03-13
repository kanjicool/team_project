import pandas as pd
from datetime import timedelta

# load data
data = pd.read_csv("/home/kunanon/kanjicool2077/1-2/model_test/FS_final/air4thai2024-01-01TO2024-03-10.csv")
del data["Unnamed: 0"]
print(data)


# Clean data 
# แปลงข้อมูลในคอลัมน์ DATETIMEDATA เป็น Timestamp errors='coerce' จะเปลี่ยนค่าที่แปลงไม่ได้เป็นค่า NaN (Not a Number)
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], errors='coerce')
# ลบแถวที่มีค่า NaN
data = data.dropna(subset=["DATETIMEDATA"])


# find start_date and end_date
start_date = data["DATETIMEDATA"].min()
start_date = pd.to_datetime(start_date)

end_date = data["DATETIMEDATA"].max()
end_date = start_date + timedelta(hours=23, minutes=59, seconds=59)


# วนลูปหาค่าเฉลี่ย PM2.5 ของทุกวัน
n = int(input('total day : '))
results = []
for i in range(0, n):
    # หา end_date ของแต่ละวัน
    current_date = start_date + timedelta(days=i)
    next_date = current_date + timedelta(days=1)


    print("timedelta >>>", timedelta(days=i))
    print(f'end_date >>> {current_date}, {next_date}')

    # กรองข้อมูลตามวันที่
    filldate_index = data.index[data["DATETIMEDATA"].between(pd.to_datetime(current_date), pd.to_datetime(next_date))]

    # หาค่าเฉลี่ย PM2.5
    result = round(data["PM25"].loc[filldate_index].mean(),2)

    # เก็บผลลัพธ์
    results.append((current_date.strftime('%Y-%m-%d'), result))

# แปลง results เป็น pandas DataFrame
df = pd.DataFrame(results, columns=["Date", "PM25"])

# บันทึก DataFrame เป็น csv
df.to_csv("avg_pm25.csv")
print('!!!end!!!')