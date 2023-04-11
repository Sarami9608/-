import pandas as pd
import numpy as np
from datetime import datetime, timedelta

start_date = datetime(2023, 3, 1)
end_date = datetime(2023, 3, 30, 23, 59)
datetimes = pd.date_range(start=start_date, end=end_date, freq='1min')

power_consumption_data = []

for dt in datetimes:
    if 15 <= dt.hour <= 21:
        power = np.random.uniform(90, 120)
    elif 10 < dt.hour < 15 :
        power = np.random.uniform(10, 15)
    else:
        power = np.random.uniform(-5, 5)

    power_consumption_data.append({'datetime': dt, 'power_consumption': power})

data = pd.DataFrame(power_consumption_data)
data.to_csv('power_consumption_data.csv', index=False)