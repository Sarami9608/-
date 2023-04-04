# 230404

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping

# 데이터 불러오기
data = pd.read_csv('power_consumption_data.csv', parse_dates=['datetime'], index_col='datetime')

# 정규화
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)

# 시퀀스 데이터 생성 (1일 간격)
def create_sequences(data, seq_length):
    x = []
    y = []

    for i in range(len(data) - seq_length - 1):
        x.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])

    return np.array(x), np.array(y)

seq_length = 24 * 60
x, y = create_sequences(data_scaled, seq_length)

# 학습 및 테스트 데이터로 분류 (다음 날만 예측)
train_size = int(len(x) * 0.99)
x_train, x_test = x[:train_size], x[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# LSTM 모델 구축
model = Sequential()
model.add(LSTM(50, input_shape=(x_train.shape[1], x_train.shape[2]), return_sequences=False))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 훈련
early_stop = EarlyStopping(monitor='val_loss', patience=10)
history = model.fit(x_train, y_train, epochs=100, batch_size=64, validation_split=0.1, callbacks=[early_stop], shuffle=False)

# 테스트 데이터 예측
y_pred = model.predict(x_test)

# 예측 결과 역정규화
y_test_inv = scaler.inverse_transform(y_test)
y_pred_inv = scaler.inverse_transform(y_pred)

# 예측 결과 출력
pred_df = pd.DataFrame({'Actual': y_test_inv.flatten(), 'Predicted': y_pred_inv.flatten()})
print(pred_df.head(1440))  # 다음 날 하루에 대한 1분 간격 예측치 출력


# 예측 결과 역정규화 및 평가
y_test_inv = scaler.inverse_transform(y_test)
y_pred_inv = scaler.inverse_transform(y_pred)

# 예측 결과 출력
pred_df = pd.DataFrame({'Actual': y_test_inv.flatten(), 'Predicted': y_pred_inv.flatten()})
print(pred_df)
predictions = scaler.inverse_transform(pred_df)  # 정규화된 값을 원래 스케일로 변환
pData = pd.DataFrame(predictions)
pData.to_csv('temperature_pData.csv', index=False)
# 예측 결과 시각화
plt.figure(figsize=(16, 8))
plt.plot(y_test_inv, label='Actual')
plt.plot(y_pred_inv, label='Predicted')
plt.legend()
plt.show()