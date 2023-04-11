import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length - 1):
        x.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

# 데이터 불러오기
data = pd.read_csv('./-/power_consumption_data.csv')

# 시간 정보를 추가 (파생변수 생성)
data['date'] = pd.to_datetime(data['datetime'])
data['hour'] = data['date'].dt.hour
data['minute'] = data['date'].dt.minute
data['time'] = data['hour'] * 60 + data['minute']

# 데이터 정규화
scaler = MinMaxScaler()
data[['power_consumption', 'time']] = scaler.fit_transform(data[['power_consumption', 'time']])

# 시퀀스 생성
seq_length = 1440
x, y = create_sequences(data[['power_consumption', 'time']].values, seq_length)

# 학습 데이터와 테스트 데이터로 분할
train_size = int(len(x) * 0.8)
x_train, x_test = x[:train_size], x[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# LSTM 모델 구성
model = Sequential()
model.add(LSTM(128, input_shape=(seq_length, 2), return_sequences=True))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(2))

# 모델 학습
model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, batch_size=128, epochs=20, validation_data=(x_test, y_test))

# 예측
predictions = model.predict(x_test)

# 정규화된 값을 원래 스케일로 되돌림
predictions_inv = scaler.inverse_transform(predictions)

# 예측 결과를 저장할 빈 리스트 생성
predictions_list = []

for i, pred in enumerate(predictions_inv):
    power, time = pred
    hours = int(time // 60)
    minutes = int(time % 60)
    
    # 예측 결과를 리스트에 추가
    predictions_list.append({"datetime": data.iloc[train_size + i + seq_length]["datetime"], "hour": f"{hours:02d}:{minutes:02d}", "power_consumption": power})

# 리스트를 사용하여 DataFrame 생성
predictions_df = pd.DataFrame(predictions_list)
predictions_df.to_csv('Power_consumption_pData.csv', index=False)