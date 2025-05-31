import pandas as pd
def generate_test_table4_data():

    lst_records = [
        {
            "Day": 15.25,
            "MTD": 283.45,
            "YTD": 3799.98
        },    
        {
            "Day": 0.06,
            "MTD": 63.63,
            "YTD": 1681.80
        },   
        # {
        #     "Day": 23.97,
        #     "MTD": 254.94,
        #     "YTD": 2542.21
        # },   
        # {
        #     "Day": 0.00,
        #     "MTD": 1.43,
        #     "YTD": 20.02
        # },
        {
            "Day": 0.04,
            "MTD": 185.74,
            "YTD": 8236.08
        },
        {
            "Day": 0.00,
            "MTD": 531.41,
            "YTD": 1477.41
        },
        {
            "Day":920.51,
            "MTD": 21719.25,
            "YTD": 239461.36
        },
        {
            "Day": "95.89%",
            "MTD": "94.27%",
            "YTD": "93.06%"
        },
        {
            "Day": "100%",
            "MTD": "99.60%",
            "YTD": "98.86%"
        },  
    ]

    df = pd.DataFrame.from_records(lst_records)
    df = df.astype(str)

    indices = [
        "Manufacturer Downtime (h)", "Unscheduled Maintenance (h)",
        "Environmental Downtime (h)", "Utility Downtime (h)", 
        "Wind Farm Available Hours (h)",
        "Plant Operational Availability Estimation (%)",
        "WTG Availability Calculated as per the contract (%)"]
    df['index'] = indices
    df = df.set_index("index")

    return df