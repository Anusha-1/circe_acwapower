import pandas as pd

def generate_test_table2_data():

    lst_records = [
        {
            "Day": 8.6,
            "MTD": 7.5,
            "YTD": 9.10
        },    
        {
            "Day": 6.6,
            "MTD": 6.4,
            "YTD": 7.6
        },   
        {
            "Day": 18.10,
            "MTD": 36.10,
            "YTD": 51.50
        },   
        {
            "Day": 17.00,
            "MTD": 20.00,
            "YTD": 18.00
        },   
    ]

    df = pd.DataFrame.from_records(lst_records)
    df = df.astype(str)

    return df