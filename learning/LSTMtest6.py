import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
data['date'] = pd.to_datetime(data['datetime'])
data['hour'] = data['date'].dt.hour
data['minute'] = data['date'].dt.minute
data['day'] = data['date'].dt.day

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

# 가장 최근 1일치 데이터를 가져옴
last_day_data = x[-1]
last_day_data = np.expand_dims(last_day_data, axis=0)

# 예측 결과를 저장할 빈 리스트 생성
predictions_list = []

for i in range(1440):
    # 가장 최근 데이터를 사용하여 예측 수행
    prediction = model.predict(last_day_data)
    
    # 예측 결과를 저장할 빈 딕셔너리 생성
    prediction_dict = {}
    
    # 예측 결과에서 소비 전력과 시간을 가져옴
    power, hour, minute = scaler.inverse_transform(prediction)[0]
    
    # 시간을 반올림하여 정수로 변환
    hour = int(round(hour))
    minute = int(round(minute))
    
    # 예측 결과를 딕셔너리에 추가
    prediction_dict['time'] = f"{hour:02d}:{minute:02d}"
    prediction_dict['power_consumption'] = power
    
    # 예측 결과를 리스트에 추가
    predictions_list.append(prediction_dict)
    
    # 가장 최근 데이터를 업데이트
    last_day_data = np.roll(last_day_data,-1, axis=1)
last_day_data[0, -1] = prediction

#리스트를 사용하여 DataFrame 생성
predictions_df = pd.DataFrame(predictions_list)

#현재 날짜를 기준으로 다음 날짜를 계산
from datetime import datetime, timedelta
next_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

#'date' column 추가
predictions_df['date'] = next_day

#column 순서 변경
predictions_df = predictions_df[['date', 'time', 'power_consumption']]

#결과를 CSV 파일로 저장
predictions_df.to_csv('Power_consumption_prediction_next_day.csv', index=False)

# #결과 출력
# print(predictions_df.head())