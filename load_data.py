import pandas
import pymysql
import pickle

def load_database():

    conn = pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='1234', db='douban', use_unicode=True, charset="utf8")
    movies_table = pandas.read_sql("select * from douban.movie;", con=conn)
    users_table = pandas.read_sql("select * from douban.user;", con=conn)
    return movies_table, users_table

movies_table, users_table = load_database()

with open('./Data/Douban/movies.pkl','wb') as file1:
    pickle.dump(movies_table, file1)

with open('./Data/Douban/users.pkl','wb') as file2:
    pickle.dump(users_table, file2)