import paho.mqtt.client as mqtt
import time
import json
# MQTT 브로커 정보
broker_address = "119.200.31.252"
broker_port = 8883
mqtt_user = ""
mqtt_password = ""
mqtt_topic = "MQTT_Topic"

# MQTT 클라이언트 생성
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
relayValue = 1 
# MQTT 브로커 연결
client.connect(broker_address, broker_port)

# MQTT 메시지 수신 콜백 함수
def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")))

# MQTT 구독 시작
client.subscribe(mqtt_topic)
client.on_message = on_message

# 1분마다 메시지 전송
while True:
    # 현재 시간을 메시지로 전송
    # 데이터 생성
    data = {
        "conID": "A001",
        "relayValue": 0
    }
    if data['relayValue'] == 0:
        data['relayValue'] = 1
    else:
        data['relayValue'] = 0
    # JSON 형식으로 데이터 전송
    payload = json.dumps(data)
    client.publish("conRelay", payload)
    print("published")
# MQTT 메시지 수신 대기
# publish도 진행하고자 한다면 스레드 분리가 필요
    client.loop_forever()