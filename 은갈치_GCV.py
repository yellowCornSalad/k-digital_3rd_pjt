import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# 파일 불러오기 (df 타입 변경 후에 df 통합해야됨. 그래야 타입 변경 시 오류 안남)
file1 = '/home/ubuntu/kdt_pjt03_fish/seafood_2022-06-30.csv'
file2 = '/home/ubuntu/kdt_pjt03_fish/갈치2022.csv'

file1 = pd.read_csv(file1)
file2 = pd.read_csv(file2)

df1 = pd.DataFrame(file1)
df2 = pd.DataFrame(file2)

df1.columns = ['date', 'species', 'origin', 'standard', 'unit', 'amount', 'weight', 'avg_price']
df2.columns = ['date', 'species', 'origin', 'standard', 'unit', 'amount', 'weight', 'avg_price']

df1 = df1[df1.species=='(선)은갈치']

# df1 데이터 타입 변경
df1['avg_price'] = df1.avg_price.str.replace(',', '').astype('int')
df1['weight'] = df1['weight'].astype('float')
df1['amount'] = df1.amount.str.replace(',', '').astype('int')

# df2 데이터 타입 변경 (df2는 평균가만 바꿔주면 됨)
df2['avg_price'] = df2.avg_price.str.replace(',', '').astype('int')

# df = df1 + df2
df = pd.concat([df1, df2], axis=0)

# 날짜 데이터 년, 월, 일로 나누고 int형으로 변환
df['yyyy'], df['mm'], df['dd'] = df['date'].str.split('-').str
df = df.drop('date', axis=1)

for i in ['yyyy', 'mm', 'dd']:
  df[i] = list(map(int, df[i]))
  
# df2 통합 후 필요 어종만 가져오기
eg_pdf = df[df.species == '(선)은갈치']

# 데이터 특정 값만 가져오기
eg_pdf = eg_pdf[eg_pdf.origin == '제주도']

standard_mask = (eg_pdf.standard == '10미')|(eg_pdf.standard == '20미')|(eg_pdf.standard == '25미')|(eg_pdf.standard == '5미')
eg_pdf = eg_pdf.loc[standard_mask, :]

eg_pdf = eg_pdf[eg_pdf.unit == 'S/P']

# 불필요 컬럼 드랍
eg_pdf = eg_pdf.drop(['species', 'unit'], axis=1)

# 범주형 데이터 OHE 수행
eg_pdf = pd.get_dummies(eg_pdf, columns=['origin', 'standard'])

# 결측치 제거
eg_pdf = eg_pdf[eg_pdf.weight < 40]

# --------------- 회귀 모델 만들기 --------------------

X = eg_pdf.drop(columns='avg_price')
y = eg_pdf['avg_price']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 20, shuffle =True, test_size = 0.2)

###### 랜덤포레스트
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
rf = RandomForestRegressor()
rf_grid_cv = GridSearchCV(rf, param_grid=rf_parameters, cv=cv, n_jobs=1, scoring='r2')
rf_grid_cv.fit(X_train, y_train)
 
print('RF 최적 하이퍼 파라미터:', rf_grid_cv.best_params_)
print('RF 최적 예측 정확도: {0:.4f}'.format(rf_grid_cv.best_score_))

eg_model_rf = rf_grid_cv.best_estimator_
eg_rf_y_pred = eg_model_rf.predict(X_test)

MSE = mean_squared_error(y_test, eg_rf_y_pred)
RMSE = np.sqrt(MSE)
r2 = r2_score(y_test, eg_rf_y_pred)

print('랜덤 포레스트 성능평가>>>>>>>>')
print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
print("r2_score : ", r2)

###### XGBoost
## 그리드 서치
xg_parameters ={'max_depth' : [3,4,5,6] , 
                # 'n_estimators': [12,24,32], 
                'n_estimators': [100,200,300], 
                'learning_rate':[0.01, 0.1], 
                # 'learning_rate':[0.1, 0.3, 0.5], 
                'gamma': [1, 2, 4], 
                'random_state':[99]}

xgb = XGBRegressor()
xgb_grid_cv = GridSearchCV(xgb, param_grid=xg_parameters, cv=6, n_jobs=-1, scoring='r2')
xgb_grid_cv.fit(X_train, y_train)
 
 
print('XGB 최적 하이퍼 파라미터:', xgb_grid_cv.best_params_)
print('XGB 최적 예측 정확도: {0:.4f}'.format(xgb_grid_cv.best_score_))

eg_model_xgb = xgb_grid_cv.best_estimator_
eg_xgb_y_pred = eg_model_xgb.predict(X_test)

MSE = mean_squared_error(y_test, eg_xgb_y_pred)
RMSE = np.sqrt(MSE)
r2 = r2_score(y_test, eg_xgb_y_pred)

print('XGBoost 성능평가>>>>>>>>')
print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
print("r2_score : ", r2)

###### LightGBM
## 그리드 서치
lgb_parameters ={
    'n_estimators': [200, 500, 1000, 2000],
    'learning_rate': [0.1, 0.05, 0.01],
    'max_depth': [6, 7, 8],
    'colsample_bytree': [0.8, 0.9, 1.0],
    'subsample': [0.8, 0.9, 1.0] 
                }

lgb = LGBMRegressor()
lgb_grid_cv = GridSearchCV(lgb, param_grid=lgb_parameters, cv=6, n_jobs=-1, scoring='r2')
lgb_grid_cv.fit(X_train, y_train)
 
 
print('LGBM 최적 하이퍼 파라미터:', lgb_grid_cv.best_params_)
print('LGBM 최적 예측 정확도: {0:.4f}'.format(lgb_grid_cv.best_score_))

eg_model_lgb = lgb_grid_cv.best_estimator_
eg_lgb_y_pred = eg_model_lgb.predict(X_test)

MSE = mean_squared_error(y_test, eg_lgb_y_pred)
RMSE = np.sqrt(MSE)
r2 = r2_score(y_test, eg_lgb_y_pred)

print('LightGBM 성능평가>>>>>>>>')
print('MSE : {0:.5f}, RMSE : {1:.5f}'.format(MSE, RMSE))
print("r2_score : ", r2)