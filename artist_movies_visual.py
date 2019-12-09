from sklearn.manifold import TSNE
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10) 

# data_pca_tsne = TSNE(n_components=2).fit_transform(artists_matrix_pca)

def plot_artist():
    label_index = {artists_index[i]:i for i in artists_index}

    X = data_pca_tsne[:,0]
    Y = data_pca_tsne[:,1]
    plt.scatter(X,Y,s=0.5)

    for i in range(1998):
        actor = label_index[i]
        # if i % 50 == 0:
        if artists[actor] > 30:
            x = data_pca_tsne[i][0]
            y = data_pca_tsne[i][1]
            label = label_index[i]
            print(label)
            plt.text(x,y,label,fontsize=10,color='green',fontproperties=font)
    plt.show()
    return 0

if __name__ == '__main__':
    plot_artist()