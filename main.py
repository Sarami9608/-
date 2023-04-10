
from mqtt import realMqtt
from DB import ConcentDAO
i = 0
mqttList = []
rows = ['a0001','a0002','a0003']
dao = ConcentDAO.ConcentDAO()

while True:
    # TODO  특정 시간에 동작을 한다.
        # 00시에 
        if dao.count_concent_ids() == False:
            rows = dao.get_member_concent_ids()
            for row in rows:
                mqttList.append(realMqtt.MQTTClient(row))
                print(mqttList[i].relay_topic)
                print(mqttList[i].energy_topic)
                print(mqttList)
                i +=1

        # 1분마다 id 개수 판단

        
# TODO 