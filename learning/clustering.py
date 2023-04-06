# 230404


from sklearn.cluster import KMeans
import pandas as pd 
import numpy as np


# 데이터 읽어오기 이 부분을 오라클 db에서 읽어오고 형식을 바꾸는 식으로 변환 필요
data = pd.read_csv('./../power_consumption_data.csv')

data1 = data[['power_consumption']]


# KMeans 모델 초기화
kmeans = KMeans(n_clusters=2, random_state=0)

# 모델 학습
kmeans.fit(data1)

# new 데이터에 대한 분류
new_data = np.array([10,1,100]).reshape(-1,1)
print(new_data)

predict_label = kmeans.predict(new_data)
print(predict_label)


# 클러스터링 결과 출력
clust_list = []
for i, label in enumerate(kmeans.labels_):
    clust_list.append(label+1)   


clust_s = pd.Series(clust_list)
clust_s.name = "power_clust" 

rs = pd.concat([data, clust_s], axis = 1)

rs.to_csv('clustering.csv')
