# -*- coding: utf-8 -*-
import pickle

with open('./Data/douban_plus/movie_plus.pkl', 'rb') as file1:
    movies_table = pickle.load(file1)

with open('./Data/douban_plus/user_plus.pkl', 'rb') as file2:
    users_table = pickle.load(file2)
