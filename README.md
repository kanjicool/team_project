# team_project
# Team Project
**Team Project** เป็น Project พยากรณ์ค่า Pm2.5 ในอีก 7 วันข้างหน้าโดยใช้ Machine Learning Library  Pycaret ในการสร้างโมเดล โดยรูปแบบที่ใช้ในการ Train มี 2 รูปแบบ
ได้แก่ Time series และ Regession
 - **Time Series model** (ใช้ข้อมูลในอดีต มาทำนายข้อมูลในอนาคต)
 -  **Regession model** (สามารถใช้ปัจจัยอื่น ๆ ที่เกี่ยวข้องเป็นส่วนประกอบของการทำ Model ได้)

สมาชิก
6610110034 คุณานนต์ หนูแสง 
6610110655 นายศุภเศรษฐ์ ทองคำชู



## การติดตั้ง 
``` bash
git clone https://github.com/kanjicool/web_racha888.git
```
```
pip install -r requirement.txt
```
##  สร้าง Virtual Environment & Run

**windown**
``` bash
pip install virtualenv

py -m venv env
```
```
.\env\Scripts\Activate.ps1
```
**linux**
``` bash
python3 -m venv venv
```
```
source venv/bin/activate
```

##  คำอธิบาย
**Dashboard**
PM25_Forecasting_APP.py  : แสดงผลหน้า Dashboard

**Model**
อยู่ใน folder ชื่อ model มี 2 ไฟล์ (คำอธิบายโค้ดอยู่ในไฟล์แล้ว)
 - Time series
 - Regession


