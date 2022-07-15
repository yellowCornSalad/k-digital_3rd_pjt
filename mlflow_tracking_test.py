import numpy as np 
from sklearn.linear_model import LinearRegression
import mlflow

def main():
	#enable autologging
    mlflow.autolog(log_input_examples=True)
    
    #prepare training data
    X = np.array([[1,1],[1,2],[2,2],[2,3]])
    #print(X)
    #print(np.array([1, 2]))
    y = np.dot(X, np.array([1, 2]))
    y = y+3
    
    #train a model
    model = LinearRegression()
    
    with mlflow.start_run() as run:
        model.fit(X,y)
        print("Logged data and model in run {}".format(run.info.run_id))

if __name__ == "__main__":
    main()
