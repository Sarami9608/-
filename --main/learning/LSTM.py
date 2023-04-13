
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
import datetime
class PowerConsumptionPredictor:

    def __init__(self, seq_length=1440):
        self.seq_length = seq_length
        self.scaler = MinMaxScaler()
        
    def create_sequences(self, data):
        x, y = [], []
        for i in range(len(data) - self.seq_length - 1):
            x.append(data[i:(i + self.seq_length)])
            y.append(data[i + self.seq_length])
        return np.array(x), np.array(y)

    def preprocess_data(self, data_df):
        data_df[['energy', 'hour', 'minute']] = self.scaler.fit_transform(data_df[['energy', 'hour', 'minute']])
        x, y = self.create_sequences(data_df[['energy', 'hour', 'minute']].values)
        return train_test_split(x, y, test_size=0.5, shuffle=False)

    def build_model(self):
        model = Sequential()
        model.add(LSTM(128, input_shape=(self.seq_length, 3), return_sequences=True))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dense(3))
        model.compile(optimizer='adam', loss='mse')
        return model

    def predict_next_day(self, model, x):
        last_day_data = x[-1]
        last_day_data = np.expand_dims(last_day_data, axis=0)
        predictions_list = []

        for i in range(1440):
#             prediction = model.predict(last_day_data)
#             power, hour, minute = self.scaler.inverse_transform(prediction)[0]
#             hour, minute = (int(round(hour)) % 24), (int(round(minute)) % 60)  # hour와 minute을 24와 60으로 나눈 나머지 값으로 대체
# # 예측 결과를 딕셔너리에 추가
#             prediction_dict = {'time': f"{hour:02d}:{minute:02d}", 'energy': power}             # 예측 결과를 리스트에 추가
#             predictions_list.append(prediction_dict)
#             last_day_data = np.roll(last_day_data, -1, axis=1)
#             last_day_data[0, -1] = prediction
            # prediction = model.predict(last_day_data)
            # power, hour, minute = self.scaler.inverse_transform(prediction)[0]
            # predictions_list.append({'time': f"{int(hour):02d}:{int(minute):02d}", 'energy': power})
            # last_day_data = np.roll(last_day_data, -1, axis=1)
            # next_hour = (int(hour) + 1) % 24
            # next_minute = (int(minute) + 1) % 60
            # next_hour_norm = next_hour / 24.0
            # next_minute_norm = next_minute / 60.0
            # last_day_data[0, -1] = [prediction[0][0], next_hour_norm, next_minute_norm]
                current_hour = i // 60
                current_minute = i % 60
                current_hour_norm = current_hour / 24.0
                current_minute_norm = current_minute / 60.0
                last_day_data[0, -1, 1:] = [current_hour_norm, current_minute_norm]
                prediction = model.predict(last_day_data)
                power, _, _ = self.scaler.inverse_transform(prediction)[0]
                predictions_list.append({'time': f"{current_hour:02d}:{current_minute:02d}", 'energy': power})
                last_day_data = np.roll(last_day_data, -1, axis=1)

                # 에너지 값을 고정하고 시간(hour, minute) 값만 변경
                last_day_data[0, -1, 0] = last_day_data[0, -2, 0]
                last_day_data[0, -1, 1:] = [current_hour_norm, current_minute_norm]
        return pd.DataFrame(predictions_list)

    def run(self, data_df):
        print("학습을 시작합니다.")
        x_train, x_test, y_train, y_test = self.preprocess_data(data_df)
        model = self.build_model()
        model.fit(x_train, y_train, batch_size=128, epochs=3, validation_data=(x_test, y_test))
        predictions_df = self.predict_next_day(model, x_train)
        # 이전 코드
        # predictions_df['date'] = (pd.datetime.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        # 수정된 코드
        predictions_df['date'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        predictions_df['p_date'] = pd.to_datetime(predictions_df['date'] + ' ' + predictions_df['time'], format='%Y-%m-%d %H:%M')
        predictions_df.drop(['date', 'time'], axis=1, inplace=True)
        predictions_df = predictions_df[['p_date', 'energy']]
        print("predictions_df")
        print(predictions_df)
        print("학습을 종료합니다.")
        return predictions_df