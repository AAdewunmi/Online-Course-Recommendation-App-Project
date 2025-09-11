from flask import Flask, request, render_template

import pandas as pd
import numpy as np
import neattext.functions as nfx
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


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


def recommend_course(df, title, cosine_mat, numrec):
    course_index = pd.Series(df.index, index=df['course_title']).drop_duplicates()
    index = course_index[title]
    scores = list(enumerate(cosine_mat[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    selected_course_index = [i[0] for i in sorted_scores[1:]]
    selected_course_score = [i[1] for i in sorted_scores[1:]]
    rec_df = df.iloc[selected_course_index]
    rec_df['Similarity_Score'] = selected_course_score
    final_recommended_courses = rec_df[['course_title', 'Similarity_Score',
                                       'url', 'price', 'num_subscribers']]
    return final_recommended_courses.head(numrec)


def extracted_features(recdf):
    course_url = list(recdf['url'])
    course_title = list(recdf['course_title'])
    course_price = list(recdf['price'])
    return course_url, course_title, course_price


def search_term(term, df):
    result_df = df[df['course_title'].str.contains(term)]
    top6 = result_df.sort_values(by='num_subscribers', ascending=False).head(6)
    return top6


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        my_dict = request.form
        titlename = my_dict['course']
        print(titlename)
        try:
            df = read_data()
            df = get_clean_title(df)
            cvmat = get_cosine_mat(df)
            num_rec = 6
            cosine_mat = cosine__sim_mat(cvmat)
            recdf = recommend_course(df, titlename, cosine_mat, num_rec)
            course_url, course_title, course_price = extracted_features(recdf)
            dictmap = dict(zip(course_title, course_url, course_price))
            if len(dictmap) != 0:
                return render_template('index.html', 
                                       coursemap=dictmap,
                                       coursename=titlename,
                                       showtitle=True)
            else:
                return render_template('index.html',
                                       showerror=True,
                                       coursename=titlename) 
        except Exception:
            resultdf = search_term(titlename, df)
            if resultdf.shape[0] > 6:
                resultdf = resultdf.head(6)
                course_url, course_title, course_price = extracted_features(
                    resultdf)
                coursemap = dict(zip(course_title, course_url, course_price))
                if len(coursemap) != 0:
                    return render_template('index.html', 
                                           coursemap=coursemap,
                                           coursename=titlename,
                                           showtitle=True)
                else:
                    return render_template('index.html',
                                           showerror=True,
                                           coursename=titlename)
            else:
                course_url, course_title, course_price = extracted_features(
                    resultdf)
                coursemap = dict(zip(course_title, course_url, course_price))
                if len(coursemap) != 0:
                    return render_template('index.html', 
                                           coursemap=coursemap,
                                           coursename=titlename,
                                           showtitle=True)
                else:
                    return render_template('index.html',
                                           showerror=True,
                                           coursename=titlename)
    return render_template('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    df = read_data()
    valuecounts = get_value_counts(df)
    levelcounts = get_level_counts(df)
    subjectcounts = get_subjects_per_level(df)
    year

