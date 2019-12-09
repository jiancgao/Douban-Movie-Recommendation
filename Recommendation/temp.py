from Recommendation.collabotm import CollaborativeTopicModel

import csv
import codecs
from Recommendation.corpus import get_ids_cnt

N_topic = 20
N_voca = 80
N_user = 100
N_item = 100

ctr = CollaborativeTopicModel(n_topic=N_topic, n_voca=N_voca, n_user=N_user, n_item=N_item)

corpus = []
for line in codecs.open('moviesdirectors7.txt', 'r', 'utf8').readlines():
    corpus.append(line)
corpus.pop(0)

voca_list, doc_ids, doc_cnt = get_ids_cnt(corpus, max_voca=N_voca)
ctr.set_doc(doc_ids[:N_item], doc_cnt[:N_item])

for i in range(99):
    ctr.set_ratings(i, i, int(i/20)+1)
    ctr.set_ratings(i, i-1, int(i/15)+1)
    ctr.set_ratings(i, i-1, int(i/25)+1)
