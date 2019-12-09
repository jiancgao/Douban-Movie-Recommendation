import pandas as pd
import numpy as np
import pickle
from sklearn.decomposition import PCA 


def movie_embedding(movie_item, year_mean, year_std, rate_mean, rate_std, type_dict, country_dict):
    movie_embedding_vector = np.zeros((114,1))

    type_dict['other'] = 0
    country_dict['other'] = 0

    type_dict_len = len(type_dict)

    type_dict_index = {item:index + 2 for index, item in enumerate(type_dict)}
    country_dict_index = {item:index + 2 + type_dict_len for index, item in enumerate(country_dict)}
    try:
        year_norm = (float(movie_item['year']) - year_mean)/year_std
    except:
        year_norm = 0

    try:
        rate_norm = (float(movie_item['rate']) - rate_mean)/rate_std
    except:
        rate_norm = 0
    movie_embedding_vector[0], movie_embedding_vector[1] = year_norm, rate_norm

    type_label = movie_item['type']
    try:
        movie_embedding_vector[type_dict_index[type_label]] = 1
    except:
        movie_embedding_vector[type_dict_index['other']] = 1

    country_label = movie_item['countries']
    try:
        movie_embedding_vector[country_dict_index[country_label]] = 1
    except:
        movie_embedding_vector[country_dict_index['other']] = 1

    return movie_embedding_vector

def user_embedding(user_item):
    pass
    return user_embedding_vetor

def get_movie_embedding_table(movie_table):
    movie_num = len(movie_table)

    year_list = []
    rate_list = []
    type_dict = {}
    country_dict = {}

    for i in range(movie_num):
        try:
            year_list.append(int(movie_table.iloc[i]['year']))
        except:
            pass

        try:
            rate_list.append(float(movie_table.iloc[i]['rate']))
        except:
            pass

        temp_country_list = movie_table.iloc[i]['countries'].strip().split('/')
        for each_country in temp_country_list:
            each_country = each_country.strip().split(' ')[0]
            try:
                country_dict[each_country] += 1
            except:
                country_dict[each_country] = 1

        temp_type_list = movie_table.iloc[i]['type'].strip().split('/')
        for each_type in temp_type_list:
            each_type = each_type.strip()
            try:
                type_dict[each_type] += 1
            except:
                type_dict[each_type] = 1

    type_dict = {i:type_dict[i] for i in type_dict if type_dict[i] > 20}
    country_dict = {i:country_dict[i] for i in country_dict if country_dict[i] > 10}

    year_mean = np.mean(year_list)
    year_std = np.std(year_list)
    rate_mean, rate_std = np.mean(rate_list), np.std(rate_list)
    print(year_mean, year_std)
        
    movie_embedding_table = {}
    for i in range(movie_num):
        movie_item = movie_table.iloc[i]
        movie_id = movie_item['id']
        movie_embedding_vector = movie_embedding(movie_item, year_mean, year_std,rate_mean, rate_std, type_dict, country_dict)
        movie_embedding_table[movie_id] = movie_embedding_vector
        
    return movie_embedding_table, country_dict, type_dict

def get_user_embedding_table(user_table):
    user_num = len(user_table)
    pass

def artist_embedding(movie_table, spliter = '/', show_time = 1, embedding_dimen = 100):

    def util(index, type):
        artist_list = movie_table.iloc[index][type].strip().split(spliter)
        for each_artist in artist_list:
            each_artist = each_artist.strip()
            if not each_artist: 
                continue
            try:
                artists[each_artist] += 1
            except:
                artists[each_artist] = 1
        return 0

    artists = {}
                    
    for i in range(len(movie_table)):
        util(i,'directors')
        # util(i,'writers')
        util(i,'actors')

    artists = {i:artists[i] for i in artists if artists[i] > show_time and i != 'None'}
    artists_index = {item:index for index, item in enumerate(artists)}

    artist_num = len(artists)
    artists_matrix = np.zeros((artist_num, artist_num))

    for i in range(len(movie_table)):
        artist_list = [i.strip() for i in movie_table.iloc[i]['directors'].strip().split(spliter)]
        artist_list += [i.strip() for i in movie_table.iloc[i]['actors'].strip().split(spliter)]
        # print(artist_list)
        # print(artists_index)
        for i in artist_list:
            for j in artist_list:
                try:
                    artists_index_i = artists_index[i]
                    artists_index_j = artists_index[j]
                    artists_matrix[artists_index_i][artists_index_j] += 1
                except:
                    pass
    
    pca = PCA(n_components=embedding_dimen)
    artists_matrix_pca = pca.fit_transform(artists_matrix)
    # artists_matrix_pca = 0

    return artists, artists_matrix, artists_matrix_pca, artists_index


if __name__ == '__main__':
    with open('C:/Users/Leon/OneDrive/DataScience/7_Social Network Mining/douban_plus/movie_plus.pkl','rb') as file1:
        movie_table_plus = pickle.load(file1)
    with open('C:/Users/Leon/OneDrive/DataScience/7_Social Network Mining/douban_plus/user_plus.pkl','rb') as file2:
    	user_table_plus = pickle.load(file2)
    
    # with open('./Data/Douban/movies.pkl','rb') as file1:
    #     movie_table = pickle.load(file1)
    # with open('./Data/Douban/users.pkl','rb') as file2:
    # 	user_table = pickle.load(file2)
    
    # movie_embedding_table, country_dict, type_dict = get_movie_embedding_table(movie_table_plus)
    movie_plus_eg = movie_table_plus.head(20000)
    artists, artists_matrix, artists_matrix_pca,artists_index = artist_embedding(movie_plus_eg, 
                                                                spliter='/', show_time=8, embedding_dimen=100)



