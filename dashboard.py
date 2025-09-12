import pandas as pd


def get_value_counts(df):
    return dict(df['subject'].value_counts())


def get_level_count(df):
    return dict(list(df.groupby(['level'])['num_subcribers'].count().items())[1:])


def get_subjects_per_level(df):
    ans = list(dict(df.groupby(['subject'])['level'].value_counts()).keys())
    all_labels = [ans[i][0]+'_'+ans[i][1] for i in range(len(ans))]
    ans_values = list(dict(df.groupby(['subject'])['level'].value_counts()).values())
    complete_dict = dict(zip(all_labels, ans_values))
    return complete_dict