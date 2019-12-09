from Recommendation.utils import get_movie_id_dict
import random
import pickle
import os
import codecs


def write_movie_doc_cvs(moviefile='movie_plus.pkl', doc_list=['summary']):
    """
    # doc_list1 = ['title', 'year', 'directors', 'writers', 'actors', 'type', 'countries']
    # doc_list1 = ['summary']
    :param doc_list: choose one or some of the followings
    ['number', 'id', 'title', 'year', 'rate', 'rating_people', 'detail',
       'betterthan', 'directors', 'writers', 'actors', 'type', 'countries',
       'language', 'pubdate', 'episodes', 'durations', 'aka', 'summary',
       'award', 'comments_count', 'questions_count', 'reviews_count', 'tags',
       'watching_count', 'collect_count', 'wish_count']
    :return:
    """
    with open(os.path.join('../Data/Douban', moviefile), 'rb') as file2:
        movies = pickle.load(file2)

    # all_doc_type = set(movies.columns)
    # del_doc_type = all_doc_type - set(doc_list)
    # new_movies = movies.drop(list(del_doc_type), axis=1)
    # new_movies.to_csv("movies" + doc_list[1] + str(len(doc_list)) + ".csv", index=False, encoding="utf_8")

    with codecs.open("movies" + doc_list[0] + str(len(doc_list)) + ".txt", 'w', 'utf8') as file:
        for i in movies.index:
            current_movie = movies.iloc[i]
            movie_doc = ""
            for doc in doc_list:
                movie_doc += '/' + current_movie[doc].replace('\n', '').replace('\r', '')
            file.write(movie_doc + '\n')


def write_rating_csv(moviefile='movie_plus.pkl', userfile='user_plus.pkl', rename='rates_plus.csv'):
    movie_id_dict = get_movie_id_dict(moviefile=moviefile)
    p = 0
    q = 0
    with open(os.path.join('../Data/Douban', userfile), 'rb') as file2:
        users = pickle.load(file2)
    with open(rename, 'w') as file:
        for i in users.index:
            # current_user = users.iloc[i]['user']
            rates = users.iloc[i]['rates'].replace(' ', '').replace('u', '') \
                .replace("'", '').strip('{').strip('}').split(',')
            for entry in rates:
                item_id = entry.split(':')[0]
                rating = entry.split(':')[1]
                if item_id not in movie_id_dict:
                    p = p + 1
                else:
                    q = q + 1
                    item_new_id = movie_id_dict[item_id]
                    file.write(str(i) + ',' + item_new_id + ',' + rating + '\n')
    print(p, q)


def train_test_split(testratio=0.2, filename='rates.csv'):
    with open(filename) as f:
        with open('rates_train.csv', 'w') as train_file:
            with open('rates_test.csv', 'w') as test_file:
                for line in f.readlines():
                    if random.random() < testratio:
                        test_file.write(line)
                    else:
                        train_file.write(line)


if __name__ == '__main__':
    write_rating_csv(userfile='users.pkl', moviefile='movies.pkl', rename='rates.csv')
    write_movie_doc_cvs(moviefile='movies.pkl', doc_list=['title', 'directors', 'year', 'actors',
                                                          'type', 'countries', 'summary'])
    train_test_split()
