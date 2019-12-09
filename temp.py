userid=0
new_ctr.U[userid].argsort()[::-1][:5]

for i in movie_id:
    print(sum(rating_matrix[:,i]!=0)/1000)