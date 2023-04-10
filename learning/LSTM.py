
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense

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
            prediction = model.predict(last_day_data)
            power, hour, minute = self.scaler.inverse_transform(prediction)[0]
            hour, minute = int(round(hour)), int(round(minute))
            predictions_list.append({'time': f"{hour:02d}:{minute:02d}", 'energy': power})
            last_day_data = np.roll(last_day_data, -1, axis=1)
            last_day_data[0, -1] = prediction

        return pd.DataFrame(predictions_list)

    def run(self, data_df):
        x_train, x_test, y_train, y_test = self.preprocess_data(data_df)
        model = self.build_model()
        model.fit(x_train, y_train, batch_size=128, epochs=5, validation_data=(x_test, y_test))
        predictions_df = self.predict_next_day(model, x_train)
        predictions_df['date'] = (pd.datetime.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        predictions_df['p_date'] = pd.to_datetime(predictions_df['date'] + ' ' + predictions_df['time'], format='%Y-%m-%d %H:%M')
        predictions_df.drop(['date', 'time'], axis=1, inplace=True)
        predictions_df = predictions_df[['p_date', 'energy']]
        return predictions_df