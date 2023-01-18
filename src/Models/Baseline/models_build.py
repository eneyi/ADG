from FeatureTransform.featureselection import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from keras.models import Sequential
from keras.layers import Dense, Activation

class PreProcess:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y
        self.split()

    def split(self, test_size=0.33):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=test_size,
                                                                                random_state=42)
        return self.x_train, self.x_test, self.y_train, self.y_test



class Models(PreProcess):
    def __init__(self, X, Y):
        super(Models, self).__init__(X, Y)
        self.seed = 42

    def LogReg(self, random_state=42, penalty=None, solver="liblinear", multi_class="auto"):
        '''
        :param random_state: An integer that defines what pseudo-random number generator to use.
        :param penalty: Can be l1,l2,none or elasticnet, decides whether there is regularization and which approach to use
        :param solver: decides what solver to use for fitting the model. can be 'liblinear', 'newton-cg', 'lbfgs', 'sag', and 'saga'
        :param multi_class: decides the approach to use for handling multiple classes.
        :return: Class LogisticRegression
        '''
        logreg = LogisticRegression(solver=solver, random_state=self.seed, penalty=penalty,multi_class=multi_class)
        logreg.fit(self.x_train, self.y_train)
        return logreg

    def XgBoost(self, objective = 'binary:logistic', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 3, alpha = 10, n_estimators = 1000, seed = 28, nb_classes = 2):
        '''
        :param objective:
        :param colsample_bytree:
        :param learning_rate:
        :param max_depth:
        :param alpha:
        :param n_estimators:
        :param seed:
        :param nb_classes:
        :return:
        '''
        xgboost = xgb.XGBClassifier()
        xgboost.fit(self.x_train.values, self.y_train, objective=objective, colsample_bytree=colsample_bytree,
                learning_rate=learning_rate, max_depth=max_depth, alpha=alpha, n_estimators=n_estimators,
                seed=self.seed, nb_classes=2)
        return xgboost





