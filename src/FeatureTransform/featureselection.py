'''Feature Selection And Feature Transformation'''
import numpy as np
from sklearn.feature_selection import RFE
from pandas import DataFrame, concat, get_dummies
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier


## Feature Selection
class HyperParameterTuning(object):
    '''Tunes Hyperparameters multi_corr threshold and '''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.model = DecisionTreeClassifier()

    def _get_significant_features(self):
        ## build initial linear regression model
        y = LabelEncoder().fit_transform(self.y)
        f = self.x.columns
        model = sm.OLS(np.asarray(y), self.x).fit()
        p_values = model.summary2().tables[1]['P>|t|']
        self.sig_features = p_values[p_values < 0.05].index
        return self.sig_features

    def _remove_multi_corr_vars(self, x, mt):
        ##remove multi correlated features from X
        self._get_significant_features()
        x = x[self.sig_features]
        corr = x.corr()
        upper = corr.abs().where(np.triu(np.ones(corr.shape), k=1).astype(np.bool))

        # Find index of feature columns with correlation greater than threshold
        to_drop = [c for c in upper.columns if any(upper[c] > mt) or any(upper[c] < -mt)]
        x = x.drop(to_drop, axis=1).replace(np.nan, 0)
        return x

    def get_crossval(self, x):
        cv = cross_val_score(self.model, x, self.y, cv=10)
        self.cv = cv
        return cv

    def tune(self):
        cvs = {}

        thresholds = np.arange(0.1, 1.0, 0.1)
        for threshold in thresholds:
            x = self.__remove_multi_corr_vars(self.x, mt=threshold)
            self.get_crossval(x)
            cvs['{}'.format(round(threshold, 2))] = self.cv
        return cvs

    def run(self):
        cvs = self.tune()
        cvs_avg = {i: np.mean(cvs[i]) for i in cvs}
        optimal_threshold = float(max(cvs_avg, key=cvs_avg.get))
        x = self.__remove_multi_corr_vars(self.x, optimal_threshold)
        return cvs, x, self.y


class FeatureSelection(HyperParameterTuning):
    def __init__(self, X, y, scale=False):
        super(FeatureSelection, self).__init__(X, y)
        self.x = self._remove_multi_corr_vars(X, 90)
        self.y = y
        self.features = self.x.columns
        self.scale = True

    def _norm_(self, x):
        m = np.mean(x)
        std = np.std(x)
        return [(i - m) / std for i in x]

    '''Mean Normalize X Vestor for Scaling'''

    def scaler(self):
        self.x = self.x.apply(lambda x: self._norm_(x)).dropna(axis=1)
        return self.x

    def get_features_recurssive(self, x, y, rank):
        reg = DecisionTreeClassifier()
        rfe_model = RFE(reg, step=1)
        rankings = rfe_model.fit(x, y).ranking_
        ranked = DataFrame([x.columns, rankings]).T
        ranked.columns = ['Feature', 'Ranking']
        ranked = ranked.sort_values('Ranking')
        s = ranked[ranked.Ranking <= rank]['Feature']
        selected, ranked = x[s], ranked[ranked.Ranking <= rank]
        return selected, ranked

    def tune_feature_selection(self):
        self.scaler()
        x, y, cvs = self.x, self.y, {}
        for feature_rank in range(1, 10):
            selected = self.get_features_recurssive(x, y, feature_rank)
            x = selected[0]
            cv = HyperParameterTuning(x, y).get_crossval(x)
            cvs['{}'.format(feature_rank)] = cv
        avg_cvs = {i: np.mean(cvs[i]) for i in cvs}
        max_rank = max(avg_cvs, key=avg_cvs.get)
        return cvs, max_rank

    def run(self):
        max_rank = self.tune_feature_selection()[1]
        fs = self.get_features_recurssive(self.x, self.y, 5)
        features = fs[0].columns
        return fs, self.y