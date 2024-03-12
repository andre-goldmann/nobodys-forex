# Bellow the import create a job that will be executed on background
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the data
data = """Date,Open,High,Low,Close
03/07/2024,1.0897,1.0951,1.0868,1.0950
03/06/2024,1.0858,1.0917,1.0843,1.0899
03/05/2024,1.0857,1.0877,1.0842,1.0859
03/04/2024,1.0840,1.0868,1.0838,1.0856
03/01/2024,1.0805,1.0846,1.0799,1.0841
02/29/2024,1.0835,1.0858,1.0796,1.0807
02/28/2024,1.0844,1.0850,1.0797,1.0840
02/27/2024,1.0850,1.0868,1.0833,1.0846
02/26/2024,1.0839,1.0863,1.0813,1.0854
02/23/2024,1.0824,1.0842,1.0812,1.0823
02/22/2024,1.0821,1.0891,1.0804,1.0825
02/21/2024,1.0808,1.0827,1.0790,1.0819
02/20/2024,1.0779,1.0842,1.0762,1.0809
02/19/2024,1.0778,1.0792,1.0762,1.0781
02/16/2024,1.0772,1.0791,1.0733,1.0779
02/15/2024,1.0728,1.0788,1.0725,1.0773
02/14/2024,1.0712,1.0737,1.0695,1.0729
02/13/2024,1.0772,1.0805,1.0701,1.0709
02/12/2024,1.0782,1.0808,1.0757,1.0773
02/09/2024,1.0780,1.0797,1.0762,1.0784
02/08/2024,1.0773,1.0791,1.0742,1.0779
02/07/2024,1.0757,1.0787,1.0752,1.0774
02/06/2024,1.0743,1.0764,1.0724,1.0755"""

if __name__ == "__main__":
    # Create DataFrame
    data = data.split('\n')
    data = [x.split(',') for x in data]
    df = pd.DataFrame(data[1:], columns=data[0])

    # Convert columns to numerical types
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)

    # Prepare the data
    X = df[['Open', 'High', 'Low']]
    y = df['Close']

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror')
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate root mean squared error
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("Root Mean Squared Error:", rmse)

    # Predict the closing price for the next day
    next_day = df[['Open', 'High', 'Low']].iloc[-1].values.reshape(1, -1)
    predicted_close = model.predict(next_day)
    print("Predicted Close for the next day:", predicted_close[0])
    # TODO stored the predicted value together with the actual value in new table