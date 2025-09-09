from flask import Flask, request, render_template

import pandas as pd
import numpy as np
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        my_dict = request.form
        titlename = my_dict['course']
        print(titlename)
    return render_template('index.html')
