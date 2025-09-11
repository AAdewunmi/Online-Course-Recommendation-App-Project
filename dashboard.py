import pandas as pd


def get_value_counts(df):
    return dict(df['subject'].value_counts())


def get_level_count(df):
    return dict(list())