import numpy as np
import os
import time as tm

from sklearn import datasets
from sklearn.cross_validation import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

from sklearn.decomposition import RandomizedPCA


docs = datasets.load_files(container_path="../../sklearn_data/problemI")

X, y = docs.data, docs.target

baseline = 1/float(len(list(np.unique(y))))

# Split the dataset into testing and training sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=2)

# define a pipeline combining a text feature extractor/transformer with a classifier
pipeline = Pipeline([
    ('vect', CountVectorizer(decode_error='ignore', analyzer='char', ngram_range=(1,2))),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB(alpha=0.0001))
])

# features to cross-check
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
location = "results" + tm.strftime("%Y%m%d-%H%M%S") + ".txt"

with open( os.path.join(sub_dir, location), 'w+') as f:
    for score in scores:
        f.write("%s \n" % score)
        clf = GridSearchCV(pipeline, parameters, cv=2, scoring=score, verbose=0)
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