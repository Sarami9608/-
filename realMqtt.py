import paho.mqtt.client as mqtt
import threading
import pandas as pd
import json
import learning.Kmean
import learning.LSTM
import DB.ConcentDAO
class MQTTClient:
    def __init__(self,con_id):
        # MQTT 브로커 정보
        self.broker_address = "119.200.31.252"
        self.broker_port = 8883
        self.mqtt_user = ""
        self.mqtt_password = ""
        self.client = mqtt.Client()
        self.client.username_pw_set(self.mqtt_user, self.mqtt_password)
        self.con_id = con_id
        self.relay_topic = f"esp32/{con_id}/conRelay"
        self.energy_topic = f"esp32/{con_id}/recEnergy"
        self.count = 0
        self.kmeans = learning.Kmean.Kmean()
        self.lstm = learning.LSTM.PowerConsumptionPredictor()
        self.dao = DB.ConcentDAO.ConcentDAO()
        # 콜백 함수 등록
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.state
        # 브로커에 연결
        self.client.connect(self.broker_address, self.broker_port)
        self.stateNow = False
        # 토픽 구독
        self.client.subscribe(self.energy_topic)
        
        # MQTT 루프를 실행하는 스레드 생성
        self.loop_thread = threading.Thread(target=self.run_loop)
        self.loop_thread.start()
        
    # 연결 콜백 함수
    def on_connect(self, client, userdata, flags, rc):
        print(f"{self.con_id} Connected with result code {str(rc)}")

    # 메시지 수신 콜백 함수
    def on_message(self, client, userdata, msg):
        data_str = str(msg.payload.decode("utf-8"))
        # json 문자열을 파이썬 딕셔너리로 변환
        data_dict = json.loads(data_str)
        
        if self.stateNow == True:
            # TODO 생성된 kmean 모델에 데이터를 넣어 상태를 구분한다.
            data_dict["p_state"]= self.kmeans.predictLabel_concent(data_dict["energy"])
            # TODO 상태가 포함된 데이터를 테이블에 추가한다.
            self.dao.insert_Energy(data_dict)
            # TODO 예측치 중 현재 시간 HH:MM 이 동일한 부분의 state를 가져온다.
            states = self.dao.compareState(self.con_id)
            # TODO state 값을 비교한다.
            # 1. 같은 경우 무시
            if states[0] == states[1]:
                # count 초기화
                self.count = 0
                pass
            # 2. 다른 경우
                # a. 현재 1, 예측 0 - 사용자 설정 확인 - 차단
            elif states[0] == 1 and states[1] == 0:
                if self.dao.getWait(self.con_id)[0] == 'waiton':
                    pass
                else:
                    # 10분 지속 될 경우 차단
                    self.count += 1 
                    if self.count == 10:
                        self.publish_relay(0)
                        self.count = 0
                # b. 현재 0, 예측 1 - 일정 시간 지속될 경우 전원 차단
            elif states[0] == 0 and states[0] == 1:
                # 15분 지속 될 경우 차단
                self.count += 1 
                if self.count == 15:
                    self.publish_relay(0)
                    self.count = 0 
        else:
            data_dict["p_state"]= 0
            self.dao.insert_Energy(concentVO=data_dict,conid=self.con_id)


    # MQTT 루프를 실행하는 스레드 메서드
    def run_loop(self):
        self.client.loop_forever()
    # 발행 메시지 전송 스레드 메서드
    def publish_relay(self, relayValue):
        data = {
            "conID": f"{self.con_id}",
            "relayValue": relayValue
        }
        # dictionary 형태 데이터 JSON화
        payload = json.dumps(data)
        self.client.publish(self.publish_relay, payload)

    def new_kmean(self):
        # 데이터 가져오기 
        data = self.dao.learningData(self.con_id)
        # 데이터프레임으로 변환
        df = self.pd.DataFrame(data, columns=['p_date', 'energy']) 
        # 데이터의 수가 충분하지 않을 경우 동작하지 않는다.
        # 데이터의 양이 28일을 초과하는 경우에만 동작을 수행
        if df.shape[0] > 1440*28:
            self.kmeans.newLabel(df)
            if self.stateNow == False:
                p_state = self.kmeans.predictLabel_concent(df['energy'])
                df['p_state'] = p_state
                self.updateState(df,self.con_id)
                self.stateNow = True
    def new_LSTM(self):
        # 데이터 가져오기 
        data = self.dao.learningData(self.con_id)
        # 데이터프레임으로 변환
        df = self.pd.DataFrame(data, columns=['p_date', 'energy'])  
        # 데이터의 수가 충분하지 않을 경우 동작하지 않는다.
        # 데이터의 양이 28일을 초과하는 경우에만 동작을 수행
        if df.shape[0] > 1440*28 and self.stateNow == True:
            predict_data = self.lstm.run(df)
            p_state = self.kmeans.predictLabel_concent(predict_data['energy'])
            predict_data['p_state'] = p_state
            self.dao.insert_Predict(concentVO=predict_data, conid=self.con_id)