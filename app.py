from flask import Flask, request, render_template

import pandas as pd
import numpy as np
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


def read_data():
    df = pd.read_csv('UdemyCleanedTitle.csv')
    return df


def get_clean_title(df):
    df['Clean_title'] = df['course_title'].apply(nfx.remove_stopwords)
    df['Clean_title'] = df['title'].apply(nfx.remove_special_characters)
    return df


def get_cosine_mat(df):
    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(df['Clean_title'])
    return cvmat


def cosine__sim_mat(cvmat):
    return cosine_similarity(cvmat)


def recommend_course():
    pass
def extracted_features():
    pass
def search_term():
    pass




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        my_dict = request.form
        titlename = my_dict['course']
        print(titlename)
    return render_template('index.html')
