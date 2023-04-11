# 230402 데이터 생성하기
import numpy as np
import pandas as pd

# 가상의 시간별 기온 데이터 생성 (30일, 분 단위)
np.random.seed(0)
data = pd.DataFrame(data={'temperature': 25 + 3 * np.sin(np.linspace(0, 60*24*30, 60*24*30)) + np.random.normal(0, 1, 60*24*30)},
                    index=pd.date_range(start='2023-01-01', periods=60*24*30, freq='T'))

# 저장
data.to_csv('temperature_data.csv', index=True)
