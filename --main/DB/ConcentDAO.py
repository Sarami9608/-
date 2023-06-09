import cx_Oracle
import logging
from datetime import datetime,timedelta


class ConcentDAO:
    concentID = set()
    newID = []
    concentCount = 0
    def __init__(self):
        
# 
        # Oracle Instant Client 라이브러리가 있는 경로
        self.connection = None
        self.cursor = None
        self.error_codes = {
            0: "Unknown error occurred.",
            1: "Error occurred while connecting to database.",
            2: "Error occurred while disconnecting from database.",
            3: "Error occurred while executing SQL query.",
            4: "Error occurred while fetching data.",
            5: "Error occurred while closing cursor.",
        }

    def connect(self):
        self.connection = cx_Oracle.connect("campus_b_230329_3","smhrd3","project-db-stu3.ddns.net:1525/XE")
        try:
            # self.connection = cx_Oracle.connect("campus_b_230329_3","smhrd3","project-db-stu3.ddns.net:1525/XE")
            self.cursor = self.connection.cursor()
            print("connected")
        except cx_Oracle.DatabaseError as e:
            # 데이터베이스와의 연결이 실패한 경우, 예외를 발생시킵니다.
            error_code = 1
            self.write_error_log(error_code)
            # raise Exception(self.error_codes[error_code])


    def disconnect(self):
        try:
            self.cursor.close()
            self.cursor = None
            print("disconnected")
        except cx_Oracle.DatabaseError as e:
            # 커서를 닫는 중 에러가 발생한 경우, 예외를 발생시킵니다.
            error_code = 5
            self.write_error_log(error_code)
            raise Exception(self.error_codes[error_code])
        finally:
            try:
                self.connection.close()
                self.connection = None
            except cx_Oracle.DatabaseError as e:
                # 연결을 닫는 중 에러가 발생한 경우, 예외를 발생시킵니다.
                error_code = 2
                self.write_error_log(error_code)
                # raise Exception(self.error_codes[error_code])

    def write_error_log(self, error_code):
        if logging.getLogger().isEnabledFor(logging.ERROR):
            # 로그를 생성합니다.
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.ERROR)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            file_handler = logging.FileHandler('./errorLog/error.txt')
            file_handler.setLevel(logging.ERROR)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # 에러 로그를 저장합니다.
            logger.error(f"{datetime.now()} - {self.error_codes[error_code]} (error code: {error_code})")
            


#  TODO  return 값이  None인 경우 다루는 쪽에서 제어하는 에러로 인식하고 넘기는 코드가 필요!



# concent_ID의 갯수를 파악하는 메서드
# 기존의 콘센트ID 갯수와 다른 경우 True 값을 반환 
# 같을 경우 False 값을 반환
    def count_concent_ids(self):
        state = True
        self.connect()
        try:
            self.cursor.execute('SELECT COUNT(*) FROM P_MEMBER')
            result = self.cursor.fetchone()
            print(result[0])
            if result[0] != self.concentCount:
                self.concentCount = result[0]
                state = False
            else:
                state = True
                
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
            raise Exception(self.error_codes[error_code])
        finally:
            self.disconnect()
            return state   

# P_member에 존재하는 모든 memberID를 가져온다.
    def get_concent_ids(self):
        self.connect()
        id_list = []
        try:
            self.cursor.execute('SELECT MEMID FROM P_MEMBER')
            result = self.cursor.fetchall()
            id_list = [row for row in result]  # 모든 concentID를 리스트로 반환
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
            raise Exception(self.error_codes[error_code])
        finally:
            self.disconnect()
            return id_list      

# P_member에 존재하는 모든 concentID를 가져온다.
# 가져온 객체들 중 concentID 값 중 신규 콘센트 아이디 값을 판별하여 반환한다. for MQTT 통신 구독 및 발행을 위해
    def get_member_concent_ids(self):
        self.connect()
        rows = []
        try:
            # 멤버 테이블에서 모든 CONID 값을 가져옵니다.
            self.cursor.execute('SELECT DISTINCT(CONID) FROM P_MEMBER')
            rows = self.cursor.fetchall()
            
            # 가져온 값들을 순차적으로 concentID set 데이터에 존재하는지 확인합니다.
            # 값이 없을 경우 데이터를 newID()리스트에 데이터를 추가합니다.
            # 값이 있을 경우 통과합니다.
            for row in rows:
                if row not in self.concentID:
                    self.concentID.add(row)
                    self.newID.append(row)
            # return의 list가 비어있는 경우 mqtt 추가X
            result = self.newID
            #  newID 빈칸으로 초기화
            self.newID = []
           
            
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
        finally:
            self.disconnect()
            return result     
            
# TODO : 1. 학습을 위한 해당 콘센트 아이디의 date 값과 에너지 값을 가져온다.

    def learningData(self, conid):
        print("learing 데이터를 가져옵니다.")
        self.connect()
        rows = []
        try:
            # P_CONCENT 테이블에서 P_DATE, ENERGY 값을 가져옵니다.
            # 오늘 날짜
            # 어제 23시 59분 59초
            print("query 문을 실행합니다. 1")
            yesterday = datetime.now() - timedelta(days=1)
            print(yesterday)
            yesterday = yesterday.replace(hour=23, minute=59, second=59)
            print(yesterday)
            yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')
            print(yesterday_str)
            self.cursor.execute(f"SELECT P_DATE, ENERGY FROM P_CONCENT WHERE CONID = '{conid}' AND P_DATE >= TO_DATE('2023-03-01', 'YYYY-MM-DD') AND P_DATE <= TO_DATE('{yesterday_str}', 'YYYY-MM-DD HH24:MI:SS') order by P_DATE")
            # list 형태로 데이터를 반환합니다.
            rows = self.cursor.fetchall()
            print(rows)
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
        finally:
            self.disconnect()
            return rows
        
# TODO : 2. esp32 모듈로 부터 들어온 데이터를 P_CONCENT 테이블에 추가한다.

    def insert_Energy(self,concentVO,conid):
        print('start')
        print(f'vo : {concentVO}')
        vo = concentVO
        self.connect()
#         query = f'INSERT INTO P_CONCENT VALUES ({vo.getConID()},sysdate,{vo.getEnergy()},{vo.getState()})'
#         dictionary로 작성을 하는 경우
        query = f'INSERT INTO P_CONCENT VALUES (\'{conid}\',sysdate,{vo["energy"]},{vo["p_state"]})'
        try:
            #  P_CONCENT 테이블로 데이터 값을 입력합니다.
            self.cursor.execute(query)
            print('execute')
            # 결과를 커밋
            self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            print('error')
            self.write_error_log(error_code)
        finally:
            self.disconnect()
            return None       

# TODO : 3. 학습한 데이터를 통해 예측한 데이터를 P_PREDICT 테이블에 추가합니다.
    def insert_Predict(self,concentVO,conid):
        vos = concentVO
        print("Predict 데이터를 DB 저장 시작합니다.")
        print(vos)
        self.connect()
        query = ""
        try:
            print(vos)
            for vo in  vos:
                date_str = vo['p_date'].strftime('%Y-%m-%d %H:%M:%S')
                print(vo)
                # dictionary로 작성을 하는 경우
                #  P_CONCENT 테이블로 데이터 값을 입력합니다.
                self.cursor.execute(f"INSERT INTO P_PREDICT VALUES ('{conid}', TO_DATE('{date_str}', 'YYYY-MM-DD HH24:MI:SS'), {round(vo['energy'], 5)}, {vo['p_state']})")
                # 결과를 커밋
                self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
            print('error')
        finally:
            self.disconnect()
            return None      
        
# TODO : 4. CONID를 기준으로 P_concent 테이블에서 P_date기준 가장 최근 값의 24HH:MM 
#        즉, 시간과 분에 해당하는 값이 동일한 튜플을 P_PREDICT 테이블에서 찾는다.
#        두 테이블에서 각각 P_STATE값을 반환한다.
    def compareState(self,conid):
        self.connect()
        querys = f"\'{conid}\'"
    
        states = ()
        try:
            # query문을 작성합니다.
            query = """
                SELECT c.P_STATE AS CONCENT_STATE, p.P_STATE AS PREDICT_STATE
                FROM P_CONCENT c
                INNER JOIN (
                    SELECT CONID, P_STATE, P_DATE
                    FROM P_PREDICT
                    WHERE CONID = :conid
                    ORDER BY P_DATE DESC
                    FETCH FIRST 1 ROWS ONLY
                ) p ON c.CONID = p.CONID AND TO_CHAR(c.P_DATE, 'YYYYMMDDHH24MI') = TO_CHAR(p.P_DATE, 'YYYYMMDDHH24MI')
                WHERE c.CONID = :conid
                ORDER BY c.P_DATE DESC
                FETCH FIRST 1 ROWS ONLY
            """
            self.cursor.execute(query, {'conid': conid})
            states = self.cursor.fetchall()
            print(states)
            
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
        finally:
            self.disconnect()
            return states
        
# TODO : 5. 사용자의 wait 설정을 값을 반환합니다.
    def getWait(self,conid):
        self.connect()
        row = []
        try:
            #  P_MEMBER 테이블에서 CONIDP_DATE,ENERGY 값을 가져옵니다.
            self.cursor.execute(f'SELECT WAIT FROM P_MEMBER WHERE CONID =\'{conid}\'')
            # list 형태로 데이터를 보낸다.
            row = self.cursor.fetchall()

            
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
        finally:
            self.disconnect()
            return row       
        
# TODO : 데이터의 상태를 업데이트 한다. how 기존의 콘센트 데이터를 전부 가져온다.
#        kmean 에 적용 해당 id의 시간에 따른 state를 update한다. 
#       과정 3. update set으로 concent 테이블의 시간에 따른 각 데이터의 state를 현재 비지도 학습의 결과로 업데이트 한다.
    def updateState(self,concentVO,conid):
        vos = concentVO
        self.connect()
        print(vos)
        try:
            for vo in  vos:
                # dictionary로 작성을 하는 경우
                date_str = vo['p_date'].strftime('%Y-%m-%d %H:%M:%S')
                #  P_CONCENT 테이블로 데이터 값을 입력합니다.
                print(vo)
                print(date_str)
                self.cursor.execute(f"UPDATE p_concent SET p_state={vo['p_state']} WHERE CONID='{conid}' AND p_date=TO_DATE('{date_str}', 'YYYY-MM-DD HH24:MI:SS')")
                # 결과를 커밋
            self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            error_code = 3
            self.write_error_log(error_code)
            print('error')
        finally:
            self.disconnect()
            return None      
# TODO : 6. P_MESSAGE 테이블의 사용자에게 전달할 메세지를 저장합니다.
# P_MESSAGE에 있는 테이블에서 P_DATE와 P_TIME의 차이는 무엇인가? - 이 부분은 수행하기 전에 테이블 구성을 파악할 필요가 있음



# TODO : 7. ?? 추가할 부분이 있을까? 상권씨와 상의를 할 필요가 있음