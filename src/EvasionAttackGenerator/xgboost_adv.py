from src.FeatureTransform.featureselection import *
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from art.attacks.evasion import BoundaryAttack, ZooAttack, HopSkipJump
from art.estimators.classification import XGBoostClassifier


class BuildXGBoostModel(FeatureSelection, FeatureTransformation):
    def __init__(self, x, y, use_feature_importance=True, transform=True):
        super(BuildXGBoostModel, self).__init__(x, y)
        self.description = "blahblah"
        self.x, self.y = x, y
        self.transform = transform
        self.use_feature_importance = use_feature_importance
        self._prepare_x_y()
        self._tune_xgb_params()

    def _prepare_x_y(self):
        self.x, self.y = self.run_ft()
        if self.use_feature_importance:
            self.selected_features = self.run_fs()

        if self.transform:
            self.x, self.y = self.run_ft()
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y_dummies, test_size=0.33,
                                                                                random_state=42)

    def _tune_xgb_params(self):
        params_test = {'max_depth': range(3, 5, 2), 'min_child_weight': range(1, 6, 2),
                       'gamma': [i / 10.0 for i in range(0, 5)]}
        grid_search = GridSearchCV(estimator=xgb.XGBClassifier(learning_rate=0.1, n_estimators=10, max_depth=5,
                                                               min_child_weight=1, objective='multi:softmax', nthread=4,
                                                               scale_pos_weight=1, seed=27), param_grid=params_test,
                                                                scoring='roc_auc', n_jobs=4, cv=5)
        grid_search.fit(self.x, self.y)
        self.gamma = grid_search.best_params_.gamma
        self.max_depth = grid_search.best_params_.max_depth
        self.min_child_weight = grid_search.best_params_.min_child_weight
        return grid_search.best_params_

    def build(self):
        xg_reg = xgb.XGBClassifier(objective='multi:softmax', colsample_bytree=0.3, learning_rate=0.1,
                                   max_depth=self.max_depth, alpha=10, n_estimators=1000, seed=28,
                                   nb_classes=3)
        xg_reg.fit(self.x_train.values, self.y_train)
        self.model = xg_reg
        return xg_reg

    def _build_classifier(self):
        classifier = XGBoostClassifier(model=self.model, nb_features=self.x_train.shape[1], nb_classes=len(set(self.y)))
        self.classifier = classifier
        return classifier

    def generate_zoo_attack(self, x, y):
        attack1 = ZooAttack(classifier=self.classifier, nb_parallel=3, confidence=0.0, targeted=True, use_resize=False,
                            use_importance=False)
        zoo_adv = attack1.generate(x=x, y=y)
        self.model.predict(zoo_adv)
        return

    def generate_hopskipjump_attack(self, x, y):
        attack2 = HopSkipJump(classifier=self.classifier, targeted=True)
        hsj_adv = attack2.generate(x=x, y=y)
        self.model.predict(hsj_adv)
        return 0

    def generate_boundary_attack(self, x, y):
        attack3 = BoundaryAttack(estimator=self.classifier, targeted=True)
        ba_adv = attack3.generate(x=x, y=y)
        self.model.predict(ba_adv)
        return 0







