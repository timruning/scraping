import pandas as pd

if __name__ == '__main__':
    path = "/data/data.csv"
    df = pd.read_csv(path)
    print(df)
    print(df.head())
