import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

# 데이터 로드
data = pd.read_csv('power_consumption_data.csv', parse_dates=['datetime'], index_col='datetime')

# 전력 소비 데이터 정규화
scaler_y = MinMaxScaler()
y_scaled = scaler_y.fit_transform(data[['power_consumption']])

# 데이터를 시계열 형태로 변환
X_train = []
y_train = []
n_past = 24 * 60  # 하루를 분 단위로 표현
print(len(data))
for i in range(n_past, len(data), n_past):
    X_train.append(np.array(range(0, 1440)).reshape(-1, 1))
    y_train.append(y_scaled[i:i+n_past])

X_train, y_train = np.array(X_train), np.array(y_train).squeeze()

print(X_train)
print(y_train)
# X_train, y_train = np.array(X_train), np.array(y_train)

# # LSTM 모델 구성
# model = Sequential()
# model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
# model.add(Dropout(0.2))
# model.add(LSTM(units=50, return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(units=50))
# model.add(Dropout(0.2))
# model.add(Dense(units=1))

# # 모델 컴파일 및 학습
# model.compile(optimizer='adam', loss='mean_squared_error')
# history = model.fit(X_train, y_train, epochs=30, batch_size=32, validation_split=0.2, shuffle=False)

# # 다음 날 분 단위 인덱스 데이터 생성
# X_next_day = np.array(range(len(data), len(data)+24*60)).reshape(1, -1, 1)

# # 다음 날 전력 소비 예측
# y_next_day_predicted = model.predict(X_next_day)

# # 예측된 전력 소비 데이터 스케일 원상복구
# y_next_day = scaler_y.inverse_transform(y_next_day_predicted)

# print("Next day's power consumption predictions: \n", y_next_day)