from lightgbm import LGBMClassifier
import pandas as pd
import os, pickle, joblib
from app.common import logger
from ..common import utils as c_utils
from app.data import utils
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report


logger = logger.getLogger(__name__)
default_dir = './models/'


class LightGBM:

    def __init__(self):
        global clf
        # 모델 선언
        clf = LGBMClassifier(
            # 하이퍼 파라미터
            nthread=4,
            n_estimators=10000,
            learning_rate=0.01,
            max_depth=11,
            num_leaves=58,
            colsample_bytree=0.613,
            subsample=0.708,
            max_bin=407,
            # reg_alpha=3.564,
            # reg_lambda=4.930,
            # min_child_weight= 6,
            min_child_samples=165,
            silent=-1,
            verbose=-1,
        )

    def train_lightgbm(self, train_x, train_y, valid_x, valid_y, next_dgr):
        # 모델 학습
        clf.fit(train_x, train_y, eval_set=[(train_x, train_y), (valid_x, valid_y)]
                , eval_metric='binary_logloss', verbose=100
                , early_stopping_rounds=200)

        # db insert 준비
        y_pred = clf.predict(valid_x)
        acc_rto, pre_rto, rec_rto = self.func_print_stats(y_pred, valid_y)

        insert_df = pd.DataFrame()
        insert_df['MDL_CODE'] = '22010001'
        insert_df['LNG_DGR'] = str(next_dgr)
        insert_df['ACC_RTO'] = acc_rto
        insert_df['PRE_RTO'] = pre_rto
        insert_df['REC_RTO'] = rec_rto
        insert_df['APLY_YN'] = 'N'
        now = c_utils.strnow()
        insert_df['FRST_RGTR'] = 'INIT_PYTHON'
        insert_df['FRST_REG_DT'] = now
        insert_df['LAST_CHNRG'] = 'INIT_PYTHON'
        insert_df['LAST_CHG_DT'] = now

        engine = utils.create_engine()

        insert_df.to_sql('MDLL', engine,  if_exists='append')

        # 모델파일 생성
        modelPath = os.path.join(default_dir, 'lightgbm/')
        os.chdir(modelPath)
        joblib.dump(clf, 'toyProjLGBM_Md.h5')

        # 모델파일 로드
        # os.chdir(modelPath)
        # LGBMDM_from_joblib = joblib.load('toyProjLGBM_Md.h5')

        logger.info('학습 종료')

    # 결과 확인 함수
    def func_print_stats(self, predictions, labels):
        logger.info("Accuracy = {}".format(accuracy_score(labels, predictions)))
        logger.info("Precision = {}".format(precision_score(labels, predictions)))
        logger.info("Recall = {}".format(recall_score(labels, predictions)))
        return accuracy_score(labels, predictions), precision_score(labels, predictions), recall_score(labels, predictions)