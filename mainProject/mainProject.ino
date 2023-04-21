#include <Wire.h> // I2C 통신을 위한 라이브러리
#include <ArduinoJson.h> // JSON 라이브러리
// network 통신을 위한 라이브러리 - 다운로드 필요
#include <PubSubClient.h>
#include <WiFi.h>
#include <math.h>


// WiFi 설정
const char* ssid = "youngHS";
const char* password = "1234567890987654321";

// MQTT 설정
const char* mqttServer = "119.200.31.252";
const int mqttPort = 8883;
const char* mqttUser = "";
const char*  mqttPassword  = "";
const char* mqttTopic = "esp32/acha1/recEnergy";
// client 객체 생성
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// 콘센트 ID 정의
const String id_con = "acha1";

// pin 번호 정의
const int currentPin = 34;
const int relayPin = 27;

unsigned long lastTime = 0;  // 마지막 전류 측정 시간
int relayState = 0;
int buttonState = HIGH;

// 전류 측정을 위한 setting
float sensitivity = 66;  // ACS712 모듈의 감도 값 (mV/A)
float zeroOffset = 2047;  
float VRMS = 0;  
float AmpsRMS = 0;  
float Watt = 0;  
double totalARMS = 0; // 평균 전류 값을 계산하기 위한 전류 제곱 합
int count  = 0; // 전압 측정 횟수 

StaticJsonDocument<100> doc; // JSON 데이터를 저장할 버퍼 생성

// median filter 를 적용하기 위한 셋팅
const int BUFFER_SIZE = 60; // 측정할 전류 값의 개수
float currentBuffer[BUFFER_SIZE]; // 전류 값을 저장할 버퍼
int bufferIndex = 0; // 버퍼 인덱스

void setup() {

  Serial.begin(115200); // 시리얼 통신 시작
  pinMode(currentPin, INPUT);
  pinMode(relayPin, OUTPUT);
  //  // WiFi 연결 ------------------------------------
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // MQTT 브로커 연결 ------------------------------
  mqttClient.setServer(mqttServer, mqttPort);

  mqttClient.setCallback(callback);
  while (!mqttClient.connected()) {
    Serial.println("Connecting to MQTT Broker...");
    if (mqttClient.connect("ArduinoClient", mqttUser, mqttPassword )) {
      Serial.println("Connected to MQTT Broker");
            //  구독하는 토픽 설정
      mqttClient.subscribe("esp32/acha1/conRelay");
    } else {
      Serial.println("Failed with state ");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
  // ------------------- wifi & broker 연결 ---------- 
  lastTime = millis(); // 마지막 전류 측정 시간 초기화

}

void loop() {
//------------------------hole effect 전압 읽기 ------------------------------------------------------
  int analogValue = analogRead(currentPin);
  float voltage = 3.3 * (analogValue-zeroOffset+100) / 4095; // 아날로그 값을 전압 값으로 변환(V)
  AmpsRMS = ((voltage)/sensitivity)*1000; // 전압 값을 전류 A 단위로 변환
    // Serial.print("first AmpsRMS : ");
    // Serial.println(AmpsRMS);
  // totalVolts += voltage; // 평균 전류 값을 계산하기 위한 전류 합에 현재 전류 값을 더합니다.
  // median filter 적용
  currentBuffer[bufferIndex] = AmpsRMS; // 버퍼에 전류 값을 저장
  bufferIndex = (bufferIndex + 1); // 버퍼 인덱스를 업데이트
  if(bufferIndex == 60){
    AmpsRMS = median(currentBuffer,BUFFER_SIZE);
    // Serial.print("median AmpsRMS : ");
    // Serial.println(AmpsRMS);
    totalARMS += AmpsRMS*AmpsRMS; // 평균 rms 값을 구합니다
    count++; // 전류 측정 횟수를 증가시킵니다.
    bufferIndex = 0;
  }

  unsigned long currentTime = millis(); // 현재 시간을 읽어옵니다.
  // if(currentTime - lastTime >= 60000){ // 1분이 경과한 경우
  if(currentTime - lastTime >= 5000){ // 1분이 경과한 경우

    Serial.print("sampling : ");
    Serial.println(count);
    Serial.print("analogValue : ");
    Serial.println(analogValue);
    Serial.print("voltage : ");
    Serial.println(voltage);
    Serial.print("AmpsRMS : ");
    Serial.println(AmpsRMS);
    Serial.print("count : ");
    Serial.println(count);
    Serial.print("totalARMS : ");
    Serial.println(totalARMS);
    double avgARMS = sqrt(totalARMS/count); // 1분간의 평균 전류 값을 계산합니다.
    Serial.print("avgARMS : ");
    Serial.println(avgARMS);
    
    Watt = getWatt(avgARMS);  // 단위 출력
    Serial.print("Watt : ");
    Serial.println(Watt);
    delay(3000); 

        // -------------------Json Data 만들기------------------------------------------------------------------------------
        doc.clear(); // 이전에 저장된 데이터를 삭제
        doc["CONID"] = id_con;
        doc["energy"] = Watt;
        // JSON 데이터를 MQTT 브로커 서버에 전송
        char buffer[100];
        serializeJson(doc, buffer); // JSON 데이터를 문자열로 변환
        //-----------------------------------------------------------------------------------------------------------------
        // mqtt 데이터 발행
         mqttClient.publish(mqttTopic, buffer);
        // --------------------------------------------------------------------------------------------------------------------  
    totalARMS = 0; // 1분간의 전류 합과 전류 측정 횟수를 초기화합니다.
    count = 0;
    delay(100);

    lastTime = currentTime; // 마지막 전류 측정 시간을 현재 시간으로 갱신합니다.
  }

  // client 객체에서 토픽 읽기
  mqttClient.loop();
  //------------------------------------------------------------------------------------------------------------

}

float getWatt(float avgARMS){


  Watt = (avgARMS*220);


  Serial.print (Watt);

  Serial.println (" watt ");
  // //0.3 is the error I got for my sensor
  return Watt;
}

void relayControl(int control){
  // 릴레이 상태 업데이트
  if(control == 1){
    digitalWrite(relayPin, HIGH);
  } else{
    digitalWrite(relayPin, LOW);
  }
  Serial.println("control Relay :");
  Serial.println(control);
}


// median filter
float median(float *values, int size) {
  float sorted[size];
  // values  값 checking
  // // 정상적으로 들어가는 것 확인
  // for (int i = 0; i < size; i++) {
  //     Serial.print("\nvalues+");
  //     Serial.print(i);
  //     Serial.print(" :");
  //     Serial.print(*(values+i));
  //   }
  // sorted 값 넣기
  for (int i = 0; i < size; i++) {
      sorted[i]  = *(values+i);
      // Serial.print("\nsorted[");
      // Serial.print(i);
      // Serial.print("] :");
      // Serial.print(sorted[i]);
      // Serial.println("값을 넣었습니다.");  
    }
  for (int i = 0; i < size - 1; i++) {
    for (int i = 0; i < size - 1; i++) {
    }
    for (int j = 0; j < size - i - 1; j++) {
      if (sorted[j] > sorted[j + 1]) {
        float temp = sorted[j];
        sorted[j] = sorted[j + 1];
        sorted[j + 1] = temp;
      }
    }
  }

  float median;
  if (size % 2 == 0) {
    median = (sorted[size / 2 - 1] + sorted[size / 2]) / 2.0;
  } else {
    median = sorted[size / 2];
  }
  return median;
}


void callback(char* topic, byte* payload, unsigned int length) {
   // Parse JSON payload
   doc.clear();
   String receivedTopic = String(topic);
  if(receivedTopic == "esp32/acha1/conRelay"){
    deserializeJson(doc, payload);
    
    // Get values from JSON payload
    String conID = doc["conID"];
    int relayValue = doc["relayValue"];
    relayControl(relayValue);
    // Print values
    Serial.print("Received message: ");
    Serial.print("conID: ");
    Serial.print(conID);
    Serial.print(", relayValue: ");
    Serial.println(relayValue);
  }
}