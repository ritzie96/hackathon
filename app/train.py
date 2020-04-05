import time
import os
import numpy as np
import pandas as pd
import re
from collections import defaultdict
from sqlalchemy.inspection import inspect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models import LdaModel, Word2Vec
from scipy.stats import entropy
from nltk.tokenize import word_tokenize
from .models import Employee
from app import db
import warnings
warnings.simplefilter('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

lemmatizer = WordNetLemmatizer()
stop = stopwords.words('english')

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

def get_cv_comment():
    cvs = Employee.query.all()
    df = pd.DataFrame(query_to_dict(cvs))
    df = df.fillna('')
    df['result'] = df['skills'] + ' ' +df['role']
    return df[['id', 'result']]

def filtered_cv_comment(filters):
    cvs = Employee.query.filter(Employee.id.in_(filters)).all()
    df = pd.DataFrame(query_to_dict(cvs))
    df = df.fillna('')
    df['result'] = df['skills'] + '' + df['role']
    return df[['id', 'result']]


class Preprocess:

    def remove_special_characters(self, text, remove_digits=True):
        re_date = re.compile(r'\d+[-:]\d+[-:]\d+')  # removes date and time
        remove_date = re.sub(re_date, '', text)
        remove_date = remove_date.replace("\\", "").replace("/", "")
        pattern = r'[^a-zåäö0-9\s]' if not remove_digits else r'[^a-zåäö\s]'  # only retains alphas n numerics
        text = re.sub(pattern, '', remove_date)
        return text

    def apply_all(self, text):
        text = self.remove_special_characters(text.strip().lower())
        text = " ".join(x for x in text.split() if x not in stop)  # removes stop words
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])  # lemmatizes
        text = " ".join(x for x in text.split() if x not in stop)
        return text

    def clean_text_description(self, df: pd.DataFrame, column_name: str) -> pd.DataFrame:
        df[column_name + "_cleaned"] = df[column_name]
        column_name = column_name + "_cleaned"
        df[column_name] = df[column_name].apply(lambda text: self.apply_all(text))
        return df


class vector_cos:  
    project = os.getcwd()
    model_path = os.path.join(project, r'Models')
    ob1 = Preprocess()

    def __init__(self, fresh=False):
        self.fresh = fresh
        dat = get_cv_comment()
        self.cleaned_data = self.ob1.clean_text_description(dat, "result")
        self.cleaned_data['tokenized'] = self.cleaned_data['result_cleaned'].apply(lambda text: word_tokenize(text))
        self.w2v_corpus = []
        for i in self.cleaned_data['tokenized']:
            self.w2v_corpus.append(i)

        if fresh:
            w2v = Word2Vec(iter=5)
            w2v.build_vocab(self.w2v_corpus)
            w2v = Word2Vec(self.w2v_corpus, min_count=1, workers=4)
            w2v.save(self.model_path+'/gensim_data/my_model')

        self.model = Word2Vec.load(self.model_path+'/gensim_data/my_model')

    def vectorize(self, words): 
        word_vecs = []
        for word in words:
            try:
                vec = self.model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        vector = np.mean(word_vecs, axis=0)
        return vector

    def cosine_sim(self, vecA, vecB):
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def cos_similarity(self, source_doc):
        source_vec = self.vectorize(source_doc)
        results = []
        for i in range(len(self.cleaned_ress)): 
            target_vec = self.vectorize(self.cleaned_ress['tokenized'][i])
            sim_score = self.cosine_sim(source_vec, target_vec)
            results.append(sim_score)
        return dict(zip(self.indi, results)) 

    def get_results(self, filters, keyss):
        if filters == []:
            ress = get_cv_comment()
        else:
            ress = filtered_cv_comment(filters)
        self.cleaned_ress = self.ob1.clean_text_description(ress, "result") 
        self.cleaned_ress['tokenized'] = self.cleaned_ress['result_cleaned'].apply(lambda text: word_tokenize(text))

        self.indi = self.cleaned_ress.index.to_list()
        self.cvs = []
        for j in self.indi:
            self.cvs.append(self.cleaned_ress['tokenized'][j])

        sorted_names = []
        cl_in = self.ob1.apply_all(keyss).split()
        res_dict = self.cos_similarity(cl_in)
        res2 = sorted(res_dict.items(), key=lambda kv: kv[1], reverse=True)
        for j in res2[:10]:
            sorted_names.append(self.cleaned_ress['id'][j[0]])
        return sorted_names
