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
mlflow.set_experiment('넙치_다시돌림')

## 클렌징 완료된 csv파일 불러오기
mlflow.autolog(log_input_examples=True)

## 클렌징 완료된 csv파일 불러오기

# 갈치 고등어 꽃게 넙치 오징어 우럭 왕게
csvs = ['cleaned_nubchi_yoon']
# csvs = ['cleaned_galchi', 'cleaned_godunga', 'cleaned_kotgae','cleaned_nubchi','cleaned_ojinga','cleaned_uruk','cleaned_wangae']

for csv in csvs:
  # 파일 불러오기 (df 타입 변경 후에 df 통합해야됨. 그래야 타입 변경 시 오류 안남)
  file = f'./{csv}.csv'
  # file = f'/home/ubuntu/kdt_pjt03_fish/{csv}.csv'
  print(f'--------------------- {csv} ---------------------')
  print()

  file = pd.read_csv(file)

  pdf = pd.DataFrame(file)

  # --------------------- 회귀 모델 만들기 ---------------------

  X = pdf.drop(columns='평균가')
  y = pdf['평균가']

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

  ## 그리드 서치
  rf_parameters = {
      'n_estimators': [100, 150, 200, 250],
      'max_depth': [None, 5, 6, 9, 12],
      # 'max_depth': [5, 6, 9, 12],
      # 'min_samples_split': [0.01, 0.02, 0.1, 0.15],
      # 'max_features': ['auto', 'sqrt'],
      'random_state':[99]
  }
  cv = KFold(n_splits=6)
  rf_grid_cv = GridSearchCV(model_rf, param_grid=rf_parameters, cv=cv, n_jobs=1, scoring='r2')
  rf_grid_cv.fit(X_train, y_train)
  
  print('RF 최적 하이퍼 파라미터:', rf_grid_cv.best_params_)
  print('RF 최적 예측 정확도: {0:.4f}'.format(rf_grid_cv.best_score_))
  print()

  model_rf = rf_grid_cv.best_estimator_
  rf_y_pred = model_rf.predict(X_test)

  MSE = mean_squared_error(y_test, rf_y_pred)
  RMSE = np.sqrt(MSE)
  r2 = r2_score(y_test, rf_y_pred)

  print('GSC 후 랜덤 포레스트 성능평가>>>>>>>>')
  print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
  print("r2_score : ", r2)
  print()

  ###### XGBoost
  model_xgb = XGBRegressor()

  model_xgb.fit(X_train, y_train)
  xgb_y_pred = model_xgb.predict(X_test)

  MSE = mean_squared_error(y_test, xgb_y_pred)
  RMSE = np.sqrt(MSE)
  r2 = r2_score(y_test, xgb_y_pred)

  print('XGBoost 성능평가>>>>>>>>')
  print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
  print("r2_score : ", r2)
  print()
  print('*'*50)


  ## 그리드 서치
  xg_parameters ={'max_depth' : [3,4,5,6] , 
                  # 'n_estimators': [12,24,32], 
                  'n_estimators': [100,200,300], 
                  'learning_rate':[0.01, 0.1], 
                  # 'learning_rate':[0.1, 0.3, 0.5], 
                  'gamma': [1, 2, 4], 
                  'random_state':[99]}

  xgb_grid_cv = GridSearchCV(model_xgb, param_grid=xg_parameters, cv=6, n_jobs=-1, scoring='r2')
  xgb_grid_cv.fit(X_train, y_train)
  
  
  print('XGB 최적 하이퍼 파라미터:', xgb_grid_cv.best_params_)
  print('XGB 최적 예측 정확도: {0:.4f}'.format(xgb_grid_cv.best_score_))
  print()

  model_xgb = xgb_grid_cv.best_estimator_
  xgb_y_pred = model_xgb.predict(X_test)

  MSE = mean_squared_error(y_test, xgb_y_pred)
  RMSE = np.sqrt(MSE)
  r2 = r2_score(y_test, xgb_y_pred)

  print('GSC 후 XGBoost 성능평가>>>>>>>>')
  print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
  print("r2_score : ", r2)
  print()

  ###### LightGBM
  model_lgb = LGBMRegressor()

  model_lgb.fit(X_train, y_train)
  lgb_y_pred = model_lgb.predict(X_test)

  MSE = mean_squared_error(y_test, lgb_y_pred)
  RMSE = np.sqrt(MSE)
  r2 = r2_score(y_test, lgb_y_pred)

  print('LightGBM 성능평가>>>>>>>>')
  print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
  print("r2_score : ", r2)
  print()
  print('*'*50)


  ## 그리드 서치
  lgb_parameters ={
      'n_estimators': [200, 500, 1000, 2000],
      'learning_rate': [0.1, 0.05, 0.01],
      'max_depth': [6, 7, 8],
      'colsample_bytree': [0.8, 0.9, 1.0],
      'subsample': [0.8, 0.9, 1.0] 
                  }

  lgb_grid_cv = GridSearchCV(model_lgb, param_grid=lgb_parameters, cv=6, n_jobs=-1, scoring='r2')
  lgb_grid_cv.fit(X_train, y_train)
  
  
  print('LGBM 최적 하이퍼 파라미터:', lgb_grid_cv.best_params_)
  print('LGBM 최적 예측 정확도: {0:.4f}'.format(lgb_grid_cv.best_score_))
  print()

  model_lgb = lgb_grid_cv.best_estimator_
  lgb_y_pred = model_lgb.predict(X_test)

  MSE = mean_squared_error(y_test, lgb_y_pred)
  RMSE = np.sqrt(MSE)
  r2 = r2_score(y_test, lgb_y_pred)

  print('GSC 후 LightGBM 성능평가>>>>>>>>')
  print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
  print("r2_score : ", r2)
  print()

print('finish')