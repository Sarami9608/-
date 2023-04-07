import paho.mqtt.client as mqtt
import threading
import json
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
        
        # 콜백 함수 등록
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # 브로커에 연결
        self.client.connect(self.broker_address, self.broker_port)
        
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
        print(f"{self.con_id} {msg.topic} {str(msg.payload)}")
    
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