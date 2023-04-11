# 230404
import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense

def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length - 1):
        x.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

# 데이터 불러오기
data = pd.read_csv('power_consumption_data.csv')

# 시간 정보를 추가 (파생변수 생성)
# 시간 정보를 추가 (파생변수 생성)
data['date'] = pd.to_datetime(data['datetime'])
data['hour'] = data['date'].dt.hour
data['minute'] = data['date'].dt.minute
# 데이터 정규화
scaler = MinMaxScaler()
data[['power_consumption', 'hour', 'minute']] = scaler.fit_transform(data[['power_consumption', 'hour', 'minute']])

# 시퀀스 생성
seq_length = 1440
x, y = create_sequences(data[['power_consumption', 'hour', 'minute']].values, seq_length)

# 학습 데이터와 테스트 데이터로 분할
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, shuffle=False)

# LSTM 모델 구성
model = Sequential()
model.add(LSTM(128, input_shape=(seq_length, 3), return_sequences=True))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(3))

# 모델 학습
model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, batch_size=128, epochs=20, validation_data=(x_test, y_test))

# 예측
predictions = model.predict(x_test)

# 정규화된 값을 원래 스케일로 되돌림
predictions_inv = scaler.inverse_transform(predictions)
# # 결과 그래프 출력
# plt.figure(figsize=(12, 6))
# plt.plot(predictions_inv, label='Predicted')
# plt.xlabel('Day')
# plt.ylabel('Power Consumption')
# plt.title('Power Consumption Prediction')
# plt.legend()
# plt.show()
pData = pd.DataFrame(predictions_inv)
pData.to_csv('Power_consumption_pData.csv', index=False)

# 예측 결과를 저장할 빈 리스트 생성
predictions_list = []

for pred in predictions_inv:
    power, hour, minute = pred
    hour = int(round(hour))
    minute = int(round(minute))
    
    # 예측 결과를 리스트에 추가
    predictions_list.append({"hour": f"{hour:02d}:{minute:02d}", "power_consumption": power})

# 리스트를 사용하여 DataFrame 생성
predictions_df = pd.DataFrame(predictions_list)
pData.to_csv('Power_consumption_pHData.csv', index=False)