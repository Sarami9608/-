import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense

# 데이터 생성
# 30일간의 데이터 (일별, 분당 전력 소비량)
data = []
for i in range(30):
    day = []
    for j in range(1440):
        if j >= 15*60 and j <= 21*60:
            day.append(np.random.randint(90, 100))
        else:
            day.append(0)
    data.append(day)
data = np.array(data)

# 학습 데이터 생성
# 29일간의 데이터를 입력값으로 사용하고, 30일째 데이터를 출력값으로 사용
x_train = []
y_train = []
for i in range(29):
    for j in range(1440):
        x_train.append(data[i, j])
        if i == 28:
            y_train.append(data[i+1, j])
x_train = np.array(x_train)
y_train = np.array(y_train)

# 입력 데이터 reshape
x_train = np.reshape(x_train, (x_train.shape[0], 1, 1))

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(50, input_shape=(1, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=10, batch_size=1, verbose=2)

# 미래 값을 예측
predicted_y = model.predict(np.array([data[29]]).reshape(1, 1440, 1))
print("Predicted value:", predicted_y)