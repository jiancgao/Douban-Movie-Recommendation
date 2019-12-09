from Recommendation.collabotm import CollaborativeTopicModel

import pickle
import csv
import codecs
import numpy as np
from Recommendation.corpus import get_ids_cnt
from Recommendation.utils import get_top_movies, get_RMSE, get_average_rating_dict

N_topic = 20
N_voca = 1000
N_user = 238
# N_user = 100
N_item = 1000

ctr = CollaborativeTopicModel(n_topic=N_topic, n_voca=N_voca, n_user=N_user, n_item=N_item)

with open('../Data/Douban/movies.pkl', 'rb') as file2:
    movies = pickle.load(file2)

corpus = []
for line in codecs.open('moviestype7.txt', 'r', 'utf8').readlines():
    corpus.append(line)

voca_list, doc_ids, doc_cnt = get_ids_cnt(corpus, max_voca=N_voca)
ctr.set_doc(doc_ids, doc_cnt)

average_rating_dict = get_average_rating_dict('movies.pkl')
average_ratings = np.array(list(average_rating_dict.values())).reshape(-1, N_item)

rating_matrix = np.zeros([N_user, N_item])
with open('./rates_train.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        user = int(row[0])
        if user >= N_user:
            break
        item = int(row[1])
        rating = int(row[2])
        ctr.set_ratings(user, item, rating - average_rating_dict[item])
        rating_matrix[user, item] = rating
ctr.fit(10)

pred = ctr.predict_item()
pred_real = pred + average_ratings
get_RMSE(pred_real,'rates_test.csv')

get_top_movies(20, pred[0], movies)
get_top_movies(20, pred_real[0], movies)
