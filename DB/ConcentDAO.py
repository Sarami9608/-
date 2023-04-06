import cx_Oracle
import logging
from datetime import datetime

class ConcentDAO:
    concentID = set()

    def __init__(self):
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
        try:
            self.connection = cx_Oracle.connect('username/password@hostname:port/servicename')
            self.cursor = self.connection.cursor()
        except cx_Oracle.DatabaseError as e:
            # 데이터베이스와의 연결이 실패한 경우, 예외를 발생시킵니다.
            error_code = 1
            self.write_error_log(error_code)
            raise Exception(self.error_codes[error_code])

    # TODO : 1. MEMEBER 테이블에서 concentID 갯수 반환  count
    # TODO : 2. member 테이블에서 concentID 전부 가져와서 비교
    #           없는 값을 concentID set type에 추가하고 그 값을 반환



    def disconnect(self):
        try:
            self.cursor.close()
        except cx_Oracle.DatabaseError as e:
            # 커서를 닫는 중 에러가 발생한 경우, 예외를 발생시킵니다.
            error_code = 5
            self.write_error_log(error_code)
            raise Exception(self.error_codes[error_code])
        finally:
            try:
                self.connection.close()
            except cx_Oracle.DatabaseError as e:
                # 연결을 닫는 중 에러가 발생한 경우, 예외를 발생시킵니다.
                error_code = 2
                self.write_error_log(error_code)
                raise Exception(self.error_codes[error_code])

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