from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import RandomizedPCA
from itertools import cycle
import numpy as np
from sklearn.cross_validation import ShuffleSplit
import string
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D
import os
import time as tm
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report



docs = datasets.load_files(container_path="../../sklearn_data/problemG")
X, y = docs.data, docs.target

X = TfidfVectorizer(decode_error='ignore', stop_words='english', analyzer='char', ngram_range=(2,4), strip_accents='unicode', sublinear_tf=True, max_df=0.5).fit_transform(X)
n_samples, n_features = X.shape

#print y

pca = RandomizedPCA(n_components=2)
X_pca = pca.fit_transform(X)

#print X_pca.shape

# colors = ['b', 'w', 'r']
# markers = ['+', 'o', '^']
# for i, c, m in zip(np.unique(y), cycle(colors), cycle(markers)):
#     pl.scatter(X_pca[y == i, 0], X_pca[y == i, 1], c=c, marker=m, label=i, alpha=0.5)

# _ = pl.legend(loc='best')

# pl.show()


X_reduced = RandomizedPCA(n_components=3).fit_transform(X)

# fig = pl.figure(1, figsize=(8, 6))
# ax = Axes3D(fig, elev=-150, azim=110)
# ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2], c=y, s=100)
# ax.set_title("A PCA Reduction of High Dimensional Data to 3 Dimensions")
# ax.set_xlabel("1st")
# ax.w_xaxis.set_ticklabels([])
# ax.set_ylabel("2nd")
# ax.w_yaxis.set_ticklabels([])
# ax.set_zlabel("3rd")
# ax.w_zaxis.set_ticklabels([])
# pl.legend(loc='best')

# pl.show()


X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.5, random_state=3)

parameters = {
    #'vect__max_df': (0.5, 0.75, 1),
    #'vect__max_features': (None, 100, 5000),
    #'vect__analyzer' : ('char', 'word'),
    #'vect__ngram_range': ((1, 1), (1, 2), (2,2), (2,3), (1,3), (1,4), (3,4), (1,5), (4,5), (3,5)),
    #'vect__ngram_range': ((1, 1), (1, 2), (1,3)),  # unigrams or bigrams or ngrams
    #'tfidf__use_idf': (True, False),
    #'clf__alpha': (1, 0.5, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001),
    #'clf__alpha': (0.001, 0.0001, 0.00001, 0.000001)
}

scores = ['precision', 'recall']

sub_dir = "Results/"
location = "results_pca" + tm.strftime("%Y%m%d-%H%M%S") + ".txt"

mnb = MultinomialNB(alpha=0.001)

with open( os.path.join(sub_dir, location), 'w+') as f:
    for score in scores:
        f.write("%s \n" % score)
        clf = GridSearchCV(estimator=mnb, param_grid=parameters, scoring=score)
        clf.fit(X_train, y_train)
        improvement = (clf.best_score_ - baseline) / baseline

        f.write("Best parameters from a %s stand point:\n" % score)
        f.write("Best score: %0.3f \n" % clf.best_score_)
        f.write("Baseline score: %0.3f \n" % baseline)
        f.write("Improved: %0.3f over baseline \n" % improvement)

        f.write("\n\nGrid scores from a %s stand point:\n" % score)
        
        for params, mean_score, scores in clf.grid_scores_:
            f.write("%0.3f (+/-%0.03f) for %r \n" % (mean_score, scores.std() / 2, params))
        f.write("\n\n")

    f.write("\n\nDetailed classification report:\n")
    f.write("The model is trained on the full development set.\n")
    f.write("The scores are computed on the full evaluation set.\n")
    
    y_true, y_pred = y_test, clf.best_estimator_.predict(X_test)
    
    f.write(classification_report(y_true, y_pred))