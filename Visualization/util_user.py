# -*- coding: utf-8 -*-
import pickle

def write_csv():
	with open('users.csv', 'w') as file:
		for i in users.index:
			current_user = users.iloc[i]['name']
			following_id = users.iloc[i]['following_id'].strip('[').strip(']').split(',')
			friends = []
			for id in following_id:
				friends.append(id.strip().strip("u").strip("'"))
			for fri in friends:
				file.write(current_user + ',' + fri + '\n')
	return 0

with open('../Data/Douban/users.pkl', 'rb') as file2:
	users = pickle.load(file2)

write_csv()