import pandas
import pymysql
import pickle

def load_database():

    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='1234', db='rcmd', use_unicode=True, charset="utf8")
    movies_table = pandas.read_sql("select * from movie;", con=conn)
    users_table = pandas.read_sql("select * from user;", con=conn)
    return movies_table, users_table

movies_table, users_table = load_database()

with open('C:/Users/Leon/OneDrive/DataScience/7_Social Network Mining/douban_plus/movie_plus.pkl','wb') as file1:
    pickle.dump(movies_table, file1)

with open('C:/Users/Leon/OneDrive/DataScience/7_Social Network Mining/douban_plus/user_plus.pkl','wb') as file2:
    pickle.dump(users_table, file2)