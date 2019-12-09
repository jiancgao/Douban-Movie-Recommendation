import pickle

with open('./Data/Douban/movies.pkl','rb') as file1:
	movies_table = pickle.load(file1)
with open('./Data/Douban/users.pkl','rb') as file2:
	users_table = pickle.load(file2)