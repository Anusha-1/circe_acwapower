
import pandas as pd

def generate_test_table1_data():

    lst_records = [
        {
            "Day": 951.10,
            "MTD": 17750.69,
            "YTD": 294250.30
        },    
        {
            "Day": " ",
            "MTD": 17927.58,
            "YTD": 297707.16
        },   
        {
            "Day": " ",
            "MTD": '0.99%',
            "YTD": '1.16%'
        },   
        {
            "Day": 1276.33,
            "MTD": 38290,
            "YTD": 308780
        },   
        {
            "Day": "74.52%",
            "MTD": "46.36%",
            "YTD": "95.29%"
        },   
        {
            "Day": 753.73,
            "MTD": 22612,
            "YTD": 198334
        },   
        {
            "Day": "126.19%",
            "MTD": "78.50%",
            "YTD": "148.36%"
        },   
        {
            "Day": 897.00,
            "MTD": 26910,
            "YTD": 253470
        },   
        {
            "Day": "106.03%",
            "MTD": "65.96%",
            "YTD": "116.09%"
        }, 
        {
            "Day": 349.4,
            "MTD": "-",
            "YTD": "-"
        },  
        {
            "Day": "100%",
            "MTD": "-",
            "YTD": "-"
        },    
        {
            "Day": 1038.91,
            "MTD": "-",
            "YTD": "-"
        },  
        {
            "Day": "91.55%",
            "MTD": "-",
            "YTD": "-"
        },  
    ]

    df = pd.DataFrame.from_records(lst_records)
    df = df.astype(str)

    return df