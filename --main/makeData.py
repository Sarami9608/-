import cx_Oracle
import random
import datetime
oracle_client_path = "C:\\Program Files\\instantclient-basiclite-windows.x64-21.9.0.0.0dbru\\instantclient_21_9"
cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)
# Oracle 데이터베이스 접속 정보
conn = cx_Oracle.connect("campus_b_230329_3","smhrd3","project-db-stu3.ddns.net:1525/XE")
cursor = conn.cursor()

# 데이터 생성 및 삽입
start_date = datetime.datetime(2023, 3, 1, 0, 0, 0)
end_date = datetime.datetime(2023, 3, 30, 23, 59, 0)
delta = datetime.timedelta(minutes=1)

while start_date <= end_date:
    p_date = start_date.strftime('%Y-%m-%d %H:%M:%S')
    energy = round(random.uniform(70, 100), 5) if start_date.hour in range(9, 13) else round(random.uniform(20, 40), 5)
    sql = "INSERT INTO p_concent (CONID, P_DATE, ENERGY, P_STATE) VALUES ('acha1', TO_DATE('" + p_date + "', 'YYYY-MM-DD HH24:MI:SS'), " + str(energy) + ", 0)"
    cursor.execute(sql)
    start_date += delta

conn.commit()
cursor.close()
conn.close()