import pickle


def write_rating_csv():
    with open('rates.csv', 'w') as file:
        for i in users.index:
            current_user = users.iloc[i]['name']
            rates = users.iloc[i]['rates'].replace(' ', '').replace('u', '') \
                .replace("'", '').strip('{').strip('}').split(',')
            for entry in rates:
                item = entry.split(':')[0]
                rating = entry.split(':')[1]
                file.write(current_user + ',' + item + ',' + rating + '\n')


with open('../Data/Douban/users.pkl', 'rb') as file2:
    users = pickle.load(file2)

write_rating_csv()
