from Recommendation.collabotm import CollaborativeTopicModel

import csv
import codecs
from Recommendation.corpus import get_ids_cnt

N_topic = 100
N_voca = 8000
N_user = 5000
N_item = 41785

ctr = CollaborativeTopicModel(n_topic=N_topic, n_voca=N_voca, n_user=N_user, n_item=N_item)

corpus = []
for line in codecs.open('movies_plus.csv', 'r', 'utf8').readlines():
    corpus.append(line)
corpus.pop(0)

voca_list, doc_ids, doc_cnt = get_ids_cnt(corpus, max_voca=N_voca)
ctr.set_doc(doc_ids, doc_cnt)

filename = './rates_plus.csv'
with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        user = int(row[0])
        item = int(row[1])
        rating = int(row[2])
        ctr.set_ratings(user, item, rating)
