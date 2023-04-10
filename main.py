import realMqtt
from DB import ConcentDAO
import time
# MQTT 객체들을 리스트로 관리
mqttList = []
# 데이터 베이스 연결
dao = ConcentDAO.ConcentDAO()
# 시간 시작 시간
last_run_time = time.time()
while True:
    # TODO  특정 시간에 동작을 한다.
        # 현재 동작 시간 측정
        current_time = time.time()
        # 00시에 동작하도록
        # 00시 부분만 문자열로 가져온다.
        time = current_time.strftime("%H")
        if time == "00":
            print("학습합니다.")
            for mqtt in mqttList:
                 mqtt.new_kmean()
                 mqtt.new_LSTM()


        # 1분이상일 때, id 개수 판단
        if current_time - last_run_time > 60:
            print("check 합니다.")
            last_run_time = current_time
            if dao.get_concent_ids() == False:
                # 새롭게 추가된 콘센트를 가져온다.
                newConcent = dao.get_member_concent_ids()
                for new in newConcent:
                     mqttList.append(realMqtt.MQTTClient(new))