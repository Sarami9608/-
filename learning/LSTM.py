# 230402 예시 lSTM

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

# 데이터 불러오기
data = pd.read_csv('temperature_data.csv', index_col=0, parse_dates=True)

# 입력 및 출력 변수 설정
y = data['temperature'].values
# print(y)
# 데이터 정규화
scaler_y = MinMaxScaler()
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

# 시간별 데이터로 나누기
n_past = 60*24  # 과거 1일 동안의 데이터 사용
n_future = 60*24  # 다음날 예측할 데이터의 크기
X_train = []
y_train = []

for i in range(n_past, len(data) - n_future):
    X_train.append(y_scaled[i-n_past:i])
    y_train.append(y_scaled[i:i+n_future])

X_train, y_train = np.array(X_train), np.array(y_train).squeeze()

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(units=64, activation='relu', input_shape=(X_train.shape[1], 1)))
model.add(Dense(units=n_future))

# 모델 컴파일 및 학습
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=10, batch_size=32)

# 예측 (새로운 데이터에 대한 예측을 수행해야 함)
X_new = np.array([y_scaled[-n_past:]]).reshape(1, n_past, 1)
predictions = model.predict(X_new)
predictions = scaler_y.inverse_transform(predictions)  # 정규화된 값을 원래 스케일로 변환
pData = pd.DataFrame(predictions)
pData.to_csv('temperature_pData.csv', index=False)
# 예측 결과 출력
for i, prediction in enumerate(predictions[0]):
    print(f"예측된 다음 날 {i//60:02d}:{i%60:02d} 시간 기온: {prediction:.2f}도")