import pandas as pd


def get_value_counts(df):
    return dict(df['subject'].value_counts())

