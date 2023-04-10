from sklearn.cluster import KMeans
import pandas as pd 
import numpy as np
import DB.ConcentDAO as DAO


class Kmean:

    def __init__(self):
        # KMeans 모델 초기화
        self.kmeans = KMeans(n_clusters=2, random_state=0)
        self.dao = DAO.ConcentDAO()
    # Series 형태의 데이터를????? 리스트 to pd(Sereis)
    # 모델 생성
    def newLabel(self,conid):
        data = self.dao.learningData(conid)
        # 데이터프레임으로 변환
        df = pd.DataFrame(data, columns=['p_date', 'energy'])  
        self.kmeans.fit(df['energy'])

    # set a labeling
    def predictLabel_concent(self,data):
        predict_label = self.kmeans.predict(data)
        # 클러스터링 결과 출력
        clust_list = []
        for i, label in enumerate(self.kmeans.labels_):
            clust_list.append(label)   
        clust_s = pd.Series(clust_list)
        clust_s.name = "p_state" 
        return clust_s

