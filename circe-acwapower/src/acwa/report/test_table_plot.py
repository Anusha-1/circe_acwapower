import pandas as pd

def generate_test_table_plot():

    lst_records = [
        {
            'month': 'January',
            'energy': 40.97,
            'P50': 36.11,
            'P90': 23.35
        },
        {
            'month': 'February',
            'energy': 42.96,
            'P50': 37.77,
            'P90': 21.63
        },
        {
            'month': 'March',
            'energy': 39.65,
            'P50': 36.97,
            'P90': 26.68
        },
        {
            'month': 'April',
            'energy': 31.05,
            'P50': 36.25,
            'P90': 24.45
        },
        {
            'month': 'May',
            'energy': 32.74,
            'P50': 32.22,
            'P90': 21.90
        },
        {
            'month': 'June',
            'energy': 39.95,
            'P50': 28.88,
            'P90': 22.35
        },
        {
            'month': 'July',
            'energy': 26.39,
            'P50': 32.42,
            'P90': 18.61
        },
        {
            'month': 'August',
            'energy': 23.42,
            'P50': 29.87,
            'P90': 16.72
        },
        {
            'month': 'September',
            'energy': 17.75,
            'P50': 38.29,
            'P90': 22.62
        },
        {
            'month': 'October',
            'energy': 0.0,
            'P50': 32.31,
            'P90': 20.22
        },
        {
            'month': 'November',
            'energy': 0.0,
            'P50': 33.96,
            'P90': 25.21
        },
        {
            'month': 'December',
            'energy': 0.0,
            'P50': 35.64,
            'P90': 23.12
        }

    ]

    df = pd.DataFrame.from_records(lst_records)

    return df