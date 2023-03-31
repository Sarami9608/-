import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense

# 다음으로, 학습 데이터와 미래 예측 데이터를 생성합니다. 예시에서는 하루에 24시간, 1시간 단위로 전력 소비 데이터를 생성합니다.

# 학습 데이터 생성 (과거 60일간의 시계열 데이터와 이에 해당하는 1일 뒤의 전력 소비 값을 출력)
x_train = []
y_train = []
for i in range(60, 1440):
    x_train.append(np.array([np.random.randint(90, 100) if j >= 15 and j <= 21 else 0 for j in range(i-60, i)]))
    y_train.append(np.array([np.random.randint(90, 100) if i+1 >= 15 and i+1 <= 21 else 0]))

x_train = np.array(x_train)
print(x_train)
# y_train = np.array(y_train)

# # 미래 예측 데이터 생성 (최근 7일간의 시계열 데이터로부터 1일 뒤의 전력 소비 값을 예측)
# x_test = []
# for i in range(1433, 1440):
#     x_test.append(np.array([np.random.randint(90, 100) if j >= 15 and j <= 21 else 0 for j in range(i-60, i)]))

# x_test = np.array(x_test)

# # LSTM 모델 생성
# model = Sequential()
# model.add(LSTM(50, input_shape=(60, 1)))
# model.add(Dense(1))
# model.compile(loss='mean_squared_error', optimizer='adam')
# model.fit(x_train.reshape(x_train.shape[0], x_train.shape[1], 1), y_train, epochs=10, batch_size=1, verbose=2)


# # 미래 값을 예측
# predicted_y = model.predict(x_test.reshape(1, x_test.shape[0], 1))
# print("Predicted value:", predicted_y)