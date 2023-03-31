// 아두이노용 코드
const int currentPin = 14;
const int relayPin = 12;
const int buttonPin = 19;
const int ledPin = 13;

int relayState = 0;
int buttonState = HIGH;
float sensitivity = 0.066;  // ACS712 모듈의 감도 값 (mV/A)
float zeroOffset = 2047;  
float VRMS = 0;  
float AmpsRMS = 0;  
float Watt = 0;  

void setup() {
  pinMode(currentPin, INPUT);
  pinMode(relayPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.begin(115200); // 시리얼 통신 시작
}

void loop() {
  // 현재 전류 값 읽기
  // Serial.println(analogRead(currentPin)); // 시리얼 모니터로 전류 값 출력
  int analogValue = analogRead(currentPin);
  float voltage = 3.3 * analogValue / 4096 + 0.05; // 아날로그 값을 전압 값으로 변환
  float current = (voltage - zeroOffset * 3.3 / 4096.0) / sensitivity; // 전류 값으로 변환
  Serial.print("voltage value raw(V):");
  Serial.println(voltage);
  Serial.print("current value raw(A):");
  Serial.println(current);
//   VRMS = (voltage/2.0) *0.707;   //root 2 is 0.707
//   AmpsRMS = ((VRMS * 1000)); 
//   Serial.print("VRMS(V): ");
//   Serial.println(VRMS);
//   Serial.print("AmpsRMS(mA): ");
//   Serial.println(AmpsRMS);

//   Serial.println(" Amps RMS  ---  ");

//   Watt = (AmpsRMS*240/1.2);

//   // note: 1.2 is my own empirically established calibration factor

// // as the voltage measured at D34 depends on the length of the OUT-to-D34 wire

// // 240 is the main AC power voltage – this parameter changes locally

//   Serial.print(Watt);

//   Serial.println(" Watts");


//   Serial.print (AmpsRMS);

//   Serial.print (" Amps ");

//   //Here cursor is placed on first position (col: 0) of the second line (row: 1)


//   Serial.print (Watt);

//   Serial.print (" watt ");
//   AmpsRMS = ((VRMS * 1000)/sensitivity); //0.3 is the error I got for my sensor


  // // 버튼 값 읽기
  int buttonValue = digitalRead(buttonPin);

  // 버튼 상태 업데이트
  if (buttonValue == HIGH) {
    if (relayState == 0){
      relayState = 1;
    } else{
      relayState = 0;
    }
  }
  Serial.println(relayState);
  // 릴레이 상태 업데이트
  digitalWrite(relayPin, relayState);
  
  // LED 상태 업데이트
  // digitalWrite(ledPin, relayState);

  delay(1000); // 딜레이를 추가하여 버튼 debounce 처리
}