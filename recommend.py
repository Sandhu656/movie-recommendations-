# -*- coding: utf-8 -*-
"""Recommend.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V7zNStpHcKj31EbDCkLP-obyw49eluJ4
"""

import numpy as np # linear algebra
import pandas as pd

movies=pd.read_csv("/content/tmdb_5000_movies.csv")
credits=pd.read_csv("/content/tmdb_5000_credits.csv")



movies.head()

credits.head()

movies.shape

movies=movies.merge(credits,on='title')

movies.shape

movies.head()

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.head()

movies.isnull().sum()



movies.dropna(inplace=True)

movies.isnull().sum()

movies.duplicated().sum()

movies.iloc[0].genres

def convert(obj):
  L=[]
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

movies['genres']=movies['genres'].apply(convert)

movies.head()

import ast
#keywords
movies['keywords']=movies['keywords'].apply(convert)

movies.head()

import ast



def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L

movies['cast'] = movies['cast'].apply(convert3)
movies.head()



#crew
movies['crew'][0]

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

movies['crew']=movies['crew'].apply(fetch_director)

movies.head()

#overview
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies.head()

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']

movies.head()

data=movies[['movie_id','title','tags']]
data.head()

data['tags']=data['tags'].apply(lambda x:" ".join(x))

data['tags'][0]

data['tags']=data['tags'].apply(lambda x:x.lower())
data.head()

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

data['tags']=data['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')

vectors=cv.fit_transform(data['tags']).toarray()

vectors

feature_names=cv.get_feature_names_out()
np.set_printoptions(threshold=np.inf)
print(feature_names)

vectors[0]

#Calculate distance(Cosine distance)
#Cosine similarity
from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vectors)

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

def recommend(movie):
  movie_index=data[data['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  for i in movies_list:
    print(data.iloc[i[0]].title)

recommend("Avatar")

import pickle

pickle.dump(data,open('movies.pkl','wb'))

data['title'].values

pickle.dump(data.to_dict(),open('movie_dict.pkl','wb'))