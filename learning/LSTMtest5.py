import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense

# 시퀀스 생성 함수 정의
def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length - 1):
        x.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

# 데이터 불러오기
data = pd.read_csv('power_consumption_data.csv')

# 시간 정보를 추가 (파생변수 생성)
data['datetime'] = pd.to_datetime(data['datetime'])
data['hour'] = data['datetime'].dt.hour / 23
data['minute'] = data['datetime'].dt.minute / 59

# 소비 전력 데이터 정규화
scaler = MinMaxScaler()
data['power_consumption'] = scaler.fit_transform(data['power_consumption'].values.reshape(-1, 1))

# 시퀀스 생성
seq_length = 1440
x, y = create_sequences(data[['power_consumption', 'hour', 'minute']].values, seq_length)

# 학습 및 테스트 데이터로 분할
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=False)

# LSTM 모델 구성
model = Sequential()
model.add(LSTM(128, input_shape=(seq_length, 3), return_sequences=True))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(3))

# 모델 컴파일 및 학습
model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, batch_size=128, epochs=20, validation_data=(x_test, y_test))

# 가장 마지막 날 데이터 가져오기
last_day_data = data.iloc[-seq_length:][['power_consumption', 'hour', 'minute']].values
last_day_data = last_day_data.reshape((1, seq_length, 3))

# 다음 날 시간 범위 설정
next_day_time = np.arange(0, 24 * 60, 1) / (24 * 60 - 1)

# 예측 결과를 저장할 빈 리스트 생성
predictions_list = []

# 다음 날 0시 ~ 23시 59분까지 1분 간격의 예측 수행
for time_value in next_day_time:
    # 마지막 날 데이터의 시간 정보를 다음 날의 시간으로 갱신
    last_day_data[0, -1, 1:] = [time_value // (1/23), time_value % (1/59)]

    # 예측 수행
    pred = model.predict(last_day_data)
    predictions_inv = scaler.inverse_transform(pred)

    # 예측 결과를 리스트에 추가
    power, hour, minute = predictions_inv[0]
    hours = int(hour * 23)
    minutes = int(minute * 59)
    predictions_list.append({"hour": f"{hours:02d}:{minutes:02d}", "power_consumption": power})

# 리스트를 사용하여 DataFrame 생성
predictions_df = pd.DataFrame(predictions_list)
# 예측 결과 저장
predictions_df.to_csv('Power_consumption_pData.csv', index=False)