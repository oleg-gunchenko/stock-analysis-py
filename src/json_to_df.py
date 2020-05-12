import json
import pandas as pd


def df_from_response(file_name: str,
                     columns=['Date', 'Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']):

    def read_json_file(file_name: str) -> dict:
        with open(f'../data/data_raw/{file_name}') as f:
            return json.load(f)

    def convert_response(d):
        for date, stock_data in d['Time Series (Daily)'].items():
            r = {'Date': date}
            r.update(stock_data)
            yield r

    df = pd.DataFrame(convert_response(read_json_file(file_name)))
    # rename the columns
    df = df.rename(columns={'1. open': 'Open',
                            '2. high': 'High',
                            '3. low': 'Low',
                            '4. close': 'Close',
                            '5. adjusted close': 'AdjClose',
                            '6. volume': 'Volume'})

    df['Date'] = pd.to_datetime(df['Date'])
    df[["Open", "High", "Low", "Close", "AdjClose"]] = df[[
        "Open", "High", "Low", "Close", "AdjClose"]].astype("float64")
    df["Volume"] = df["Volume"].astype("int64")
    df["AdjFactor"] = df["AdjClose"] / df["Close"]
    df["AdjOpen"] = df["Open"] * df["AdjFactor"]
    df["AdjHigh"] = df["High"] * df["AdjFactor"]
    df["AdjLow"] = df["Low"] * df["AdjFactor"]

    # df.set_index('Date', inplace=True)
    # df.sort_index(inplace=True)
    # extract the default columns
    # df = df[columns]
    return df