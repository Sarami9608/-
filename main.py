# 전체적으로 다룰 코드를 작성합니다.


# TODO : 1. 아두이노와 통신하는 객체를 생성하고 객체를 통해 수신한 데이터를 다룹니다.
#           mosquitto 클래스를 생성하고 초기에 브로커와 연결을 진행합니다. 연결이 되었을 경우 객체를 정상적으로 동작시킵니다. 
#           pub, sub 메서드가 존재합니다. 
#           pub의 경우에는 'topic' '전달할 데이터 JSON 타입으로 구성을 진행한 후 매개변수로 사용합니다. 
#           suv의 경우에는 'topic' 을 매개변수로 구독하는 토픽을 생성합니다. 
#           이때 예상되는 문제점 구독하는 topic에서 데이터를 보내는 경우 어떻게 receive를 구현하지? callback이 일어나는 경우 해당 동작이 가능하도록 구현 call.loop()를 어디서 구현할 것인가?
#           loop()를 진행하더라도 다른 과정은 수행하며 callback 이 동작하는 경우만 따로 진행이 가능한가?

# TODO : 2. 오라클과 연동하기 위한 DAO 클래스와 데이터를 다루기 위한 VO를 생성합니다.
#           DB 폴더를 생성하고 해당 폴더에 VO와 DAO 를 생성합니다. 
#           VO의 경우에는 concent_id , date , consumption, state_label
#           DAO의 경우에는 현재 2개의 기능을 필요로 합니다.
#           학습을 위해 해당 콘센트 ID에 해당하는 데이터를 전부 가져옵니다. 필요한 데이터 date , consumption
#           아두이노 측에서 데이터가 들어온 경우, 학습을 통해 분류와 예측치 비교를 진행한 후 데이터를 테이블에 저장합니다. concent_id, date , consumption, state_label
#           ** 추가적인 부분 : 시계열 예측치를 전용 테이블에 저장 


# TODO : 3. 학습을 위한 비지도 학습 모듈, LSTM 모듈을 구성합니다.
#           learning 파일을 생성
#           LSTM을 구현하는 코드를 진행합니다 .초기에 모델 데이터를 self로 만듭니다ㅣ
#           method를 통해 학습을 진행하는 코드를 작성
#           predict를 진행하는 코드를 작성
#           비지도 학습ㅇ르 구현하는 코드를 작성
#           모델을 생성
#           method를 통해 학습을 진행하는 코드
#           mothod를 통해 분류하는 코드를 작성


# TODO : 4. 아두이노 릴레이를 컨트롤 하기 위한 모듈을 생성합니다. 
#           학습을 통해 나온 결과에 따라 동작을 판단하는 모듈을 생성합니다.


# TODO : 5. 아두이노를 어떻게 컨트롤 할 것인지 파악합니다
#           사용자에게 알림을 데이터 베이스에 전송합니다.
#           해당 콘센트 전원을 차단합니다.
#
from MQTT import realMqtt
from DB import ConcentDAO
i = 0
mqttList = []
rows = ['a0001','a0002','a0003']
dao = ConcentDAO.ConcentDAO()

while True:
    # TODO 특정 시간에 동작을 한다.
        if dao.count_concent_ids() == False:
            rows = dao.get_member_concent_ids()
            for row in rows:
                mqttList.append(realMqtt.MQTTClient(row))
                print(mqttList[i].relay_topic)
                print(mqttList[i].energy_topic)
                print(mqttList)
                i +=1
# TODO 