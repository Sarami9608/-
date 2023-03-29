import paho.mqtt.client as mqtt

# MQTT 브로커 정보
broker_address = ""
broker_port = 8883
mqtt_user = ""
mqtt_password = ""
mqtt_topic = "MQTT_Topic"

# MQTT 클라이언트 생성
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_user, mqtt_password)

# MQTT 브로커 연결
mqtt_client.connect(broker_address, broker_port)

# MQTT 메시지 수신 콜백 함수
def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode("utf-8")))

# MQTT 구독 시작
mqtt_client.subscribe(mqtt_topic)
mqtt_client.on_message = on_message

# MQTT 메시지 수신 대기
mqtt_client.loop_forever()