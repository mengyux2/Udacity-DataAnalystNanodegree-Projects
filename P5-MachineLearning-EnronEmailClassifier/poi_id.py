#%writefile poi_id.py
# %load poi_id.py
# %load poi_id.py
#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.feature_selection import SelectKBest, f_classif
### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','fraction_from_poi','fraction_to_poi','salary', 'to_messages', 
                 'deferral_payments', 'total_payments', 'exercised_stock_options', 
  'bonus', 'restricted_stock', 'shared_receipt_with_poi', 'total_stock_value', 
  'expenses', 'from_messages', 'other', 'from_this_person_to_poi', 
  'deferred_income', 'long_term_incentive', 'from_poi_to_this_person']



### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers

### convert dict to dataframe
dt = pd.DataFrame.from_dict(data_dict, orient='index')
dt.replace('NaN', np.nan, inplace = True)  
#drop the outliner
dt.drop('TOTAL', inplace = True)




### Task 3: Create new feature(s)
dt['fraction_from_poi'] = dt['from_poi_to_this_person'] / dt['to_messages']
dt['fraction_to_poi'] = dt['from_this_person_to_poi'] / dt['from_messages']

### Store to my_dataset for easy export below.
#convert the numpy array to dict
dt.replace(np.nan, 'NaN', inplace = True)   
my_dataset=dt.to_dict(orient='index')


### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)




### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
# Provided to give you a starting point. Try a variety of classifiers.
#from sklearn.naive_bayes import GaussianNB
#clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
# Example starting point. Try investigating other evaluation techniques!
#from sklearn.cross_validation import train_test_split
#features_train, features_test, labels_train, labels_test = \
#    train_test_split(features, labels, test_size=0.3, random_state=42)
#clf = clf.fit(features_train, labels_train)

###Gaussian Naive-Bayes
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.naive_bayes import GaussianNB
folds = 100
kbest = SelectKBest(f_classif)

# A stratified shuffle split is used here to counter the effects of 
# the class imbalance problem
sss = StratifiedShuffleSplit(labels, folds, test_size=0.2, random_state = 42)
gnb = GaussianNB()

# A pipeline is used to chain the SelectKBest and algorithm.  
pipeline = Pipeline([('kbest', kbest), ('gnb', gnb)])

K_FEATURES = range(1,19)
K_FEATURES.append('all')

param_grid = {
    'kbest__k': K_FEATURES
}

gnb_grid_search = GridSearchCV(estimator = pipeline, 
                           param_grid = param_grid,
                        cv=sss,scoring='f1')

gnb_grid_search.fit(features, labels)

# Print the optimal value for k
print(gnb_grid_search.best_params_)

###Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier

folds = 100
kbest = SelectKBest(f_classif)

sss = StratifiedShuffleSplit(labels, folds, test_size=0.2, random_state = 42)
dtree = DecisionTreeClassifier(random_state = 42)
pipeline = Pipeline([('kbest', kbest), ('dtree', dtree)])


MIN_SAMPLES = [2,3,4,5,6]
CRITERION = ['gini', 'entropy']


param_grid = {
    'kbest__k': K_FEATURES,
    'dtree__min_samples_split': MIN_SAMPLES,
    'dtree__criterion': CRITERION,
}

tree_grid_search = GridSearchCV(estimator = pipeline, 
                           param_grid = param_grid,
                        cv=sss,scoring='f1')

tree_grid_search.fit(features, labels)

# Print the optimal value for k
print(tree_grid_search.best_params_)

###KNeighborsClassifier

from sklearn.neighbors import KNeighborsClassifier

folds = 100
kbest = SelectKBest(f_classif)

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
scaled_features = min_max_scaler.fit_transform(features)


sss = StratifiedShuffleSplit(labels, folds, test_size=0.2, random_state = 42)

knn = KNeighborsClassifier()

pipeline = Pipeline([('kbest', kbest), ('knn', knn)])


N_NEIGHBORS = [2,3,4,5,6]


param_grid = {
    'kbest__k': K_FEATURES,
    'knn__n_neighbors': N_NEIGHBORS
}

knn_grid_search = GridSearchCV(estimator = pipeline, 
                           param_grid = param_grid,
                        cv=sss,scoring='f1')

knn_grid_search.fit(scaled_features, labels)

# Print the optimal value for k
print(knn_grid_search.best_params_)

###AdaBoostClassifier

from sklearn.ensemble import AdaBoostClassifier

folds = 10
kbest = SelectKBest(f_classif)

sss = StratifiedShuffleSplit(labels, folds, test_size=0.2, random_state = 42)

dtree = DecisionTreeClassifier(random_state = 42)
ada=AdaBoostClassifier(base_estimator=dtree,random_state = 42)

pipeline = Pipeline([('kbest', kbest),('ada', ada)])


RATE = [2,3,4,5,6]
ESTIMATORS=[5,10,20,40,50]

param_grid = {
    'kbest__k': K_FEATURES,
        'ada__learning_rate': RATE,
    'ada__n_estimators':ESTIMATORS
}

ada_grid_search = GridSearchCV(estimator = pipeline, 
                           param_grid = param_grid,
                        cv=sss)

ada_grid_search.fit(features, labels)

# Print the optimal value for k
print(ada_grid_search.best_params_)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

###final algorithm
clf = gnb_grid_search.best_estimator_
dump_classifier_and_data(clf, my_dataset, features_list)