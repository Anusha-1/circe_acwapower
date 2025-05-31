
import pandas as pd

def generate_test_table9_data():

    lst_records = [
        {
            "full_description": "V01, V02: Alarm A",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm B",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm C",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm D",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm E",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm F",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm G",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "V01, V02: Alarm H",
            "duration": 10.01,
            "losses": 10.01,
            "monthly_losses": 50.01,
            "yearly_losses": 100.01
        },
        {
            "full_description": "Total",
            "duration": 80.08,
            "losses": 80.08,
            "monthly_losses": 400.08,
            "yearly_losses": 800.08
        }
    ]

    df = pd.DataFrame.from_records(lst_records)
    df = df.astype(str)

    df = df.set_index("full_description")

    return df