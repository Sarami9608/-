from sklearn.cluster import KMeans
import pandas as pd 
import numpy as np


class Kmean:
    kmeans = None
    def __init__(self):
        # KMeans 모델 초기화
        print('kmeans 객체를 생성합니다.')
        self.kmeans = KMeans(n_clusters=2, random_state=0)
    # Series 형태의 데이터를????? 리스트 to pd(Sereis)
    # 모델 생성
    def newLabel(self,data):
        self.kmeans.fit(data['energy'].values.reshape(-1, 1))
        print('kmean 학습을 완료합니다.')

    # set a labeling
    def predictLabel_concent(self,data):
        # self.kmeans.fit(data.values.reshape(-1, 1))
        # print('kmean 학습을 완료합니다.')
        print(data)
        print(self.kmeans)
        predict_label = self.kmeans.predict(data)
        # 클러스터링 결과 출력
        clust_list = []
        for i, label in enumerate(self.kmeans.labels_):
            clust_list.append(label)   
        clust_s = pd.Series(clust_list)
        clust_s.name = "p_state" 
        return clust_s

