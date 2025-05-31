import pandas as pd

def generate_test_table3_data():

    lst_records = [
        {
            "Day": 464.44,
            "MTD": 7754.19,
            "YTD": 128694.53
        },    
        {
            "Day": "48.83%",
            "MTD": "43.68%",
            "YTD": "43.74%"
        },   
        {
            "Day": 176.94,
            "MTD": 3989.24,
            "YTD": 62725.21
        },   
        {
            "Day": "18.60%",
            "MTD": "22.47%",
            "YTD": "21.32%"
        },
        {
            "Day": 309.73,
            "MTD": 6007.27,
            "YTD": 102830.55
        },
        {
            "Day": "32.56%",
            "MTD": "33.84%",
            "YTD": "34.95%"
        },
        {
            "Day": 951.10,
            "MTD": 17750.69,
            "YTD": 294250.30
        },   
    ]

    df = pd.DataFrame.from_records(lst_records)
    df = df.astype(str)

    return df