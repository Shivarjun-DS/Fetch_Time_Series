#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")

def load_file(Path:str):
    #reading Data Frame
    df = pd.read_csv(Path)
    #renaming Date column
    df.rename(columns={'# Date':'Date'}, inplace=True)
    #converting Date column to datetime
    df['Date']=pd.to_datetime(df['Date'])
    #assigning date column to index
    df.set_index('Date', inplace = True)
    #taking first order difference of the Receipt_Count column and adding it to DF
    df['first_order'] = df['Receipt_Count'].diff()
    #log transformation of Receipt_Count
    df['log_transformation'] = np.log(df['Receipt_Count'])
    #taking first order difference of the log transformation and adding it to the DF
    df['log_first_order'] = df['log_transformation'].diff()
    #dropping the Na or inf values from DF
    df.dropna(inplace=True)
    return df

def Prediction(df):
    #generating random numbers with mean 0 and std 1
    np.random.seed(42)
    E = np.random.normal(0, 1, 12)            
    E.sort()
    while True:
        print("Enter the month (1-12) to predict for 2022")
        print("(or)")
        print("'Q' to Quit:")
        #taking prediction month from user
        user_input = input()
        if user_input.upper() == 'Q' or user_input.lower() == 'q':
            break
        try:
            user_input = int(user_input)
            if user_input < 1 or user_input > 12:
                print('enter a valid month number')
                continue
        except ValueError:
            print("Please enter a valid month number or 'Q' to Quit")
            continue
        
        #method -1
        #genrating Hsitoric mean
        Historic_mean = np.exp(df['log_transformation'].mean() + df['log_first_order'].mean())
        
        #method-2
        #calculating constant value
        C = df['log_first_order'].mean()
        #calculating pre value which is the mean of log_transformation
        pre = df['log_transformation'].mean()
        #setting aplha value to 0.9
        Aplha = 0.9
        #list to add genereated values
        pred = []
        for i in range(12):
            #formula which generetes the predicted values which is stationary and randomized
            value = C  + Aplha*pre + E[i]
            rounded_value = round(value, 6)
            #applying inveres logarithm
            inverse = np.exp(rounded_value)
            pred.append(inverse)
        #printing predicted values
        print(f'predicted value using method - 1 for {user_input}/2022 is {int(pred[user_input - 1])}')
        print(f'predicted value using method - 2 for {user_input}/2022 is {int(Historic_mean)}')
        print()
        
if __name__ == '__main__':
    df = load_file(r"C:\Users\SHIVARJUN\Downloads\data_daily.csv")
    Prediction(df)