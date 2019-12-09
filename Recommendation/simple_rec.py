import os
import surprise
from surprise import Dataset, Reader, accuracy
from surprise.model_selection import cross_validate, KFold
from collections import defaultdict


def get_top_n(predictions, estimate=True, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        estimate: bool, True=estimate rates, False=true rates
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        if estimate:
            top_n[uid].append((iid, est))
        else:
            top_n[uid].append((iid, true_r))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        if len(user_ratings) > n:
            threshold = user_ratings[n - 1][1]
            i = n
            while user_ratings[i][1] == threshold and i + 1 < len(user_ratings):
                i += 1
            top_n[uid] = [x[0] for x in user_ratings[:i]]
        else:
            top_n[uid] = [x[0] for x in user_ratings[:n]]
    return top_n


def precision_recall(predictions, est_n=10, true_n=10):
    '''Return precision and recall at for n metrics for each user.'''
    est_top_n = get_top_n(predictions, estimate=True, n=est_n)
    true_top_n = get_top_n(predictions, estimate=False, n=true_n)
    hit = 0
    n_recall = 0
    n_precision = 0
    for uid in est_top_n.keys():
        hit += len(set(est_top_n[uid]) & set(true_top_n[uid]))
        n_precision += len(est_top_n[uid])
        n_recall += len(true_top_n[uid])
    return hit / n_precision, hit / n_recall


# define reader and load data
file_path = os.path.expanduser('./rates.csv')
reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5))
data = Dataset.load_from_file(file_path, reader=reader)
kf = KFold(n_splits=5, random_state=1)

algo = surprise.BaselineOnly()
# algo = surprise.KNNBasic()
# algo = surprise.KNNWithMeans()
# algo = surprise.KNNBaseline()
# algo = surprise.SVD()

precisions = []
recalls = []
rmse = []
mae = []
#
# # GridList = [(5, 5), (10, 10), (5, 10), (5, 20)]
# with open('result.txt', 'w') as file:
#     for est_n, true_n in GridList:
#         precisions = []
#         recalls = []
#         for trainset, testset in kf.split(data):
#             algo.fit(trainset)
#             predictions = algo.test(testset, verbose=False)
#             prec, rec = precision_recall(predictions, est_n, true_n)
#             precisions.append(prec)
#             recalls.append(rec)
#             # precisions, recalls = precision_recall_at_k(predictions)
#             # # Precision and recall can then be averaged over all users
#             # precision.append(sum(prec for prec in precisions.values()) / len(precisions))
#             # recall.append(sum(rec for rec in recalls.values()) / len(recalls))
#             # mae.append(accuracy.mae(predictions))
#             # rmse.append(accuracy.rmse(predictions))
#
#         precision = sum(precisions) / 5
#         recall = sum(recalls) / 5
#         print(precision,recall)
#         file.write(str(precision)+'\n')
#         file.write(str(recall)+'\n')
# print(sum(mae) / 5)
# print(sum(rmse) / 5)

cross_validate(surprise.BaselineOnly(), data, cv=5, verbose=True)
cross_validate(surprise.KNNBasic(), data, cv=5, verbose=True)
cross_validate(surprise.KNNWithMeans(), data, cv=5, verbose=True)
cross_validate(surprise.KNNBaseline(), data, cv=5, verbose=True)
cross_validate(surprise.SVD(), data, cv=5, verbose=True)
