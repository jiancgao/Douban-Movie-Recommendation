# -*-coding:utf-8-*-
import numpy as np
import pickle
from six.moves import xrange
import os
import csv


def get_average_rating_dict(moviefile='movie_plus.pkl'):
    '''
    set movie number to rating
    :return:a dict {number:average rating}
    '''
    rating_dict = {}
    with open(os.path.join('../Data/Douban', moviefile), 'rb') as file2:
        movies = pickle.load(file2)
        for i in movies.index:
            rating = float(movies.iloc[i]['rate']) / 2
            rating_dict[i] = rating
    return rating_dict


def get_movie_id_dict(moviefile='movie_plus.pkl'):
    '''
    set movie id to number
    :return:a dict {id:number}
    '''
    id_dict = {}
    with open(os.path.join('../Data/Douban', moviefile), 'rb') as file2:
        movies = pickle.load(file2)
        for i in movies.index:
            id_dict[movies.iloc[i]['id']] = str(i)
    return id_dict


def get_RMSE(pred_matrix, filename='./rates_test.csv'):
    rmse = 0
    i = 0
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            user = int(row[0])
            item = int(row[1])
            rating = int(row[2])
            rmse += (pred_matrix[user][item] - rating) \
                    * (pred_matrix[user][item] - rating)
            i += 1
    return rmse / i


def get_MAE(pred_matrix, filename='./rates_test.csv'):
    mae = 0
    i = 0
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            user = int(row[0])
            item = int(row[1])
            rating = int(row[2])
            mae += abs(pred_matrix[user][item] - rating)

            i += 1
    return mae / i


def get_top_movies(n_movies, user_ratings, movies):
    '''
    :param user_ratings: a numpy array, shape of [1, n_item]
    :return:
    '''
    top_ids = user_ratings.argsort()[::-1][:n_movies]
    name_list = []
    score_list = []
    for i in top_ids:
        name_list.append(movies.iloc[i]['title'])
        score_list.append(user_ratings[i])
    return name_list, score_list


def write_top_words(topic_word_matrix, vocab, filepath, n_words=20, delimiter=',', newline='\n'):
    with open(filepath, 'w') as f:
        for ti in xrange(topic_word_matrix.shape[0]):
            top_words = vocab[topic_word_matrix[ti, :].argsort()[::-1][:n_words]]
            f.write('%d' % (ti))
            for word in top_words:
                f.write(delimiter + word)
            f.write(newline)


def get_top_words(topic_word_matrix, vocab, topic, n_words=20):
    if not isinstance(vocab, np.ndarray):
        vocab = np.array(vocab)
    top_words = vocab[topic_word_matrix[:, topic].argsort()[::-1][:n_words]]
    return top_words

