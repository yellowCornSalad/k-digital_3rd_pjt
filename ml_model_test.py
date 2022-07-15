import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import mlflow


# MLflow  실험실 추가 
mlflow.set_experiment('lab_test')
## 클렌징 완료된 csv파일 불러오기

# 전복, 가자미, 은갈치 순
csvs = ['cleaned_jb', 'cleaned_gj', 'cleaned_eg']

mlflow.autolog(log_input_examples=True)

for csv in csvs:
  # 파일 불러오기 (df 타입 변경 후에 df 통합해야됨. 그래야 타입 변경 시 오류 안남)
  file = f'./{csv}.csv'
  # file = f'/home/ubuntu/kdt_pjt03_fish/{csv}.csv'
  print(f'--------------------- {csv} ---------------------')
  print()

  file = pd.read_csv(file)

  pdf = pd.DataFrame(file)

  # --------------------- 회귀 모델 만들기 ---------------------

  X = pdf.drop(columns='avg_price')
  y = pdf['avg_price']

  X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 20, shuffle =True, test_size = 0.2)

  ###### 랜덤포레스트
  model_rf = RandomForestRegressor()

  model_rf.fit(X_train, y_train)
  rf_y_pred = model_rf.predict(X_test)

  MSE = mean_squared_error(y_test, rf_y_pred)
  RMSE = np.sqrt(MSE)
  r2 = r2_score(y_test, rf_y_pred)

  print('랜덤 포레스트 성능평가>>>>>>>>')
  print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
  print("r2_score : ", r2)
  print()
  print('*'*50)


