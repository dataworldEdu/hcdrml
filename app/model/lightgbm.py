import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from lightgbm import LGBMClassifier



def run(data):
    hyper_parameter_dic ={
        'n_jobs': 4,
        'n_estimators': 1000,
        'learning_rate': 0.01,
        'max_dept': 11,
        'num_leaves': 58,
        'colsample_bytree': 0.613,
        'subsample': 0.708,
        'max_bin': 407,
        'min_child_samples': 165,
        'silent': False,
        'verbose': -1,
    }

    train_x, valid_x, train_y, valid_y = train_test_split(data, data['TARGET'], test_size=0.3, random_state=2020)
    train_x = train_x.drop(['SK_ID_CURR', 'TARGET'], axis=1)
    valid_x = valid_x.drop(['SK_ID_CURR', 'TARGET'], axis=1)
    classifier = LGBMClassifier(
        n_jobs=hyper_parameter_dic['n_jobs'],
        n_estimators=hyper_parameter_dic['n_estimators'],
        learning_rate=hyper_parameter_dic['learning_rate'],
        max_depth=hyper_parameter_dic['max_depth'],
        num_leaves=hyper_parameter_dic['num_leaves'],
        colsample_bytree=hyper_parameter_dic['colsample_bytree'],
        subsample=hyper_parameter_dic['subsample'],
        max_bin=hyper_parameter_dic['max_bin'],
        min_child_samples=hyper_parameter_dic['min_child_samples'],
        silent=hyper_parameter_dic['silent'],
        verbose=hyper_parameter_dic['verbose']
    )
    classifier.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)], eval_metric='auc', verbose=100, early_stopping_rounds=200)
    
    #TODO: Model Save


def print_metric_score(predictions, labels):
    print("Accuracy = {}".format(accuracy_score(labels, predictions)))
    print("Precision = {}".format(precision_score(labels, predictions)))
    print("Recall = {}".format(recall_score(labels, predictions)))

    return accuracy_score(labels, predictions), precision_score(labels, predictions), recall_score(labels, predictions)


def model_predict(classifier):
    os.chdir('')
    valid_x = pd.DataFrame()
    valid_y = pd.DataFrame()
    y_pred = classifier.predict(valid_x)
    y_pred_proba = classifier.predict_proba(valid_x)
    print_metric_score(y_pred, valid_y)


def test_result_save():
    ...
    #TODO: test result save