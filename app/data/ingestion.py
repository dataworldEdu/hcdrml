import pandas as pd
import numpy as np
import traceback
import os
from warnings import filterwarnings
from ..common import utils as c_utils
from . import utils
from . import preprocessing
from ..model import lightgbm
from app.common import logger
from sklearn.model_selection import train_test_split

logger = logger.getLogger(__name__)
default_dir = './data/external/'
filterwarnings('ignore')


def train_model():
    try:
        # 데이터 취합
        apps = select_application_train()

        prev_agg = select_previous_application()
        apps_all = apps.merge(prev_agg, on='SK_ID_CURR', how='left', indicator=False)

        bureau_agg = select_bureau()
        apps_all = apps_all.merge(bureau_agg, on='SK_ID_CURR', how='left', indicator=False)

        pos_agg = select_pos_cash_balance()
        apps_all = apps_all.merge(pos_agg, on='SK_ID_CURR', how='left', indicator=False)

        install_agg = select_installments_payments()
        apps_all = apps_all.merge(install_agg, on='SK_ID_CURR', how='left', indicator=False)

        card_agg = select_credit_card_balance()
        apps_all = apps_all.merge(card_agg, on='SK_ID_CURR', how='left', indicator=False)

        #전처리 시작
        apps_all = preprocessing.fill_na(apps_all)

        apps_all = preprocessing.one_hot_encoding(apps_all)

        # number type 확인 --> minmax, log
        num_columns = apps_all.dtypes[apps_all.dtypes != 'object'].index.tolist()
        #num_columns = num_columns[2:]

        # 최대값, 최소값 생성
        numList = []
        for idx, val in enumerate(num_columns):
            maxVal = apps_all[val].max()
            minVal = apps_all[val].min()

            numList.append([val, minVal, maxVal])

        for idx, val in enumerate(numList):
            col = val[0]
            min = val[1]
            max = val[2]

            apps_all[col] = utils.min_max_scaler(apps_all[col], min, max)

        for col in num_columns:
            apps_all[col] = np.log1p(apps_all[col])

        apps_all = preprocessing.fill_na(apps_all)

        apps_all = apps_all.astype({'TARGET': 'int'})

        apps_all.to_csv('after.csv')

        # 전처리 종료
        target_app = apps_all['TARGET'] # 예측 정답

        # 학습을 위한 학습, 검증 데이터로 분리
        train_x, valid_x, train_y, valid_y = train_test_split(apps_all, target_app, test_size=0.3, random_state=2020)
        # 학습결과 정보 생성을 위해 임시 DataFrame 생성
        train_x = train_x.drop(['SK_ID_CURR', 'TARGET'], axis=1)
        valid_x_ori = valid_x.copy()
        valid_x = valid_x.drop(['SK_ID_CURR', 'TARGET'], axis=1)

        # 학습 차수 조회
        sql = "SELECT IFNUll(MAX(LNG_DGR),0) + 1 AS NEXT_DGR FROM MDLL WHERE MDL_CODE = '2201'"

        db = utils.create_engine()
        conn = db.connect()
        next_dgr = pd.read_sql(sql, conn)
        next_dgr = next_dgr['NEXT_DGR'].max()

        # lightGBM 학습
        lgbm = lightgbm.LightGBM()
        lgbm.train_lightgbm(train_x, train_y, valid_x, valid_y, next_dgr)

    except Exception as e:
        logger.error(traceback.format_exc())  # 로깅

    # return apps_all


def select_application_train():
    cols = ['SK_ID_CURR', 'TARGET', 'NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
            'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'NAME_TYPE_SUITE',
            'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE',
            'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH',
            'OWN_CAR_AGE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE',
            'FLAG_EMAIL', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY',
            'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START', 'REG_REGION_NOT_LIVE_REGION',
            'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
            'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE', 'OBS_30_CNT_SOCIAL_CIRCLE',
            'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE',
            'DAYS_LAST_PHONE_CHANGE', 'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY',
            'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT',
            'AMT_REQ_CREDIT_BUREAU_YEAR']
    app_dtype = {
        'SK_ID_CURR': np.uint32
    }

    db = utils.create_engine()
    conn = db.connect()
    apps = pd.read_sql_table('APPLICATION_TRAIN', conn, columns=cols)
    apps.astype(app_dtype)
    conn.close()
    db.dispose()

    apps = utils.under_sampler(apps, 'TARGET')

    return apps


def select_previous_application():
    preCols = ['SK_ID_CURR', 'AMT_ANNUITY_PRE_SUM', 'AMT_APPLICATION_SUM', 'AMT_CREDIT_PRE_SUM', 'AMT_DOWN_PAYMENT_SUM',
               'AMT_GOODS_PRICE_PRE_SUM', 'HOUR_APPR_PROCESS_START_PRE_SUM', 'NFLAG_LAST_APPL_IN_DAY_SUM',
               'RATE_DOWN_PAYMENT_SUM', 'RATE_INTEREST_PRIMARY_SUM', 'RATE_INTEREST_PRIVILEGED_SUM',
               'DAYS_DECISION_SUM', 'SELLERPLACE_AREA_SUM', 'CNT_PAYMENT_SUM', 'DAYS_FIRST_DRAWING_SUM',
               'DAYS_FIRST_DUE_SUM', 'DAYS_LAST_DUE_1ST_VERSION_SUM', 'DAYS_LAST_DUE_SUM', 'DAYS_TERMINATION_SUM',
               'NFLAG_INSURED_ON_APPROVAL_SUM']
    db = utils.create_engine()
    conn = db.connect()
    prev_agg = pd.read_sql_table('PREVIOUS_APPLICATION', conn, columns=preCols)
    conn.close()
    db.dispose()

    return prev_agg


def select_bureau():
    bureCols = ['SK_ID_CURR', 'DAYS_CREDIT_SUM', 'CREDIT_DAY_OVERDUE_SUM', 'DAYS_CREDIT_ENDDATE_SUM',
                'DAYS_ENDDATE_FACT_SUM', 'AMT_CREDIT_MAX_OVERDUE_SUM', 'CNT_CREDIT_PROLONG_SUM', 'AMT_CREDIT_SUM_SUM',
                'AMT_CREDIT_SUM_DEBT_SUM', 'AMT_CREDIT_SUM_LIMIT_SUM', 'AMT_CREDIT_SUM_OVERDUE_SUM',
                'DAYS_CREDIT_UPDATE_SUM', 'AMT_ANNUITY_BRUE_SUM']

    db = utils.create_engine()
    conn = db.connect()
    bureau_agg = pd.read_sql_table('BUREAU', conn, columns=bureCols)
    conn.close()
    db.dispose()

    return bureau_agg


def select_pos_cash_balance():
    pos_cols = ['SK_ID_CURR', 'MONTHS_BALANCE_SUM', 'CNT_INSTALMENT_SUM', 'CNT_INSTALMENT_FUTURE_SUM', 'SK_DPD_SUM',
                'SK_DPD_DEF_SUM']

    db = utils.create_engine()
    conn = db.connect()
    pos_agg = pd.read_sql_table('POS_CASH_BALANCE', conn, columns=pos_cols)
    conn.close()
    db.dispose()

    return pos_agg


def select_installments_payments():
    install_cols = ['SK_ID_CURR', 'NUM_INSTALMENT_VERSION_SUM', 'NUM_INSTALMENT_NUMBER_SUM', 'DAYS_INSTALMENT_SUM',
                    'DAYS_ENTRY_PAYMENT_SUM', 'AMT_INSTALMENT_SUM', 'AMT_PAYMENT_SUM']

    db = utils.create_engine()
    conn = db.connect()
    install_agg = pd.read_sql_table('INSTALLMENTS_PAYMENTS', conn, columns=install_cols)
    conn.close()
    db.dispose()

    return install_agg


def select_credit_card_balance():
    card_cols = ['SK_ID_CURR', 'MONTHS_BALANCE_CARD_SUM', 'AMT_BALANCE_SUM', 'AMT_CREDIT_LIMIT_ACTUAL_SUM',
                 'AMT_DRAWINGS_ATM_CURRENT_SUM', 'AMT_DRAWINGS_CURRENT_SUM', 'AMT_DRAWINGS_OTHER_CURRENT_SUM',
                 'AMT_DRAWINGS_POS_CURRENT_SUM', 'AMT_INST_MIN_REGULARITY_SUM', 'AMT_PAYMENT_CURRENT_SUM',
                 'AMT_PAYMENT_TOTAL_CURRENT_SUM', 'AMT_RECEIVABLE_PRINCIPAL_SUM', 'AMT_RECIVABLE_SUM',
                 'AMT_TOTAL_RECEIVABLE_SUM', 'CNT_DRAWINGS_ATM_CURRENT_SUM', 'CNT_DRAWINGS_CURRENT_SUM',
                 'CNT_DRAWINGS_OTHER_CURRENT_SUM', 'CNT_DRAWINGS_POS_CURRENT_SUM', 'CNT_INSTALMENT_MATURE_CUM_SUM',
                 'SK_DPD_CARD_SUM', 'SK_DPD_DEF_CARD_SUM']

    db = utils.create_engine()
    conn = db.connect()
    card_agg = pd.read_sql_table('CREDIT_CARD_BALANCE', conn, columns=card_cols)
    conn.close()
    db.dispose()

    return card_agg


def collect_application_train():
    logger.info('collect_application_train  start!')
    now = c_utils.strnow()

    cols = ['SK_ID_CURR', 'TARGET', 'NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
            'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'AMT_GOODS_PRICE', 'NAME_TYPE_SUITE',
            'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE', 'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE',
            'REGION_POPULATION_RELATIVE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH',
            'OWN_CAR_AGE', 'FLAG_MOBIL', 'FLAG_EMP_PHONE', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE',
            'FLAG_EMAIL', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT', 'REGION_RATING_CLIENT_W_CITY',
            'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START', 'REG_REGION_NOT_LIVE_REGION',
            'REG_REGION_NOT_WORK_REGION', 'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
            'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE', 'OBS_30_CNT_SOCIAL_CIRCLE',
            'DEF_30_CNT_SOCIAL_CIRCLE', 'OBS_60_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE',
            'DAYS_LAST_PHONE_CHANGE', 'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY',
            'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON', 'AMT_REQ_CREDIT_BUREAU_QRT',
            'AMT_REQ_CREDIT_BUREAU_YEAR']
    app_dtype = {
        'SK_ID_CURR': np.object
    }

    app_train = pd.read_csv(os.path.join(default_dir, 'application_train.csv'), dtype=app_dtype)
    apps = app_train[cols]

    apps = preprocessing.fill_na(apps)

    apps['FRST_RGTR'] = 'INIT_PYTHON'
    apps['FRST_REG_DT'] = now
    apps['LAST_CHNRG'] = 'INIT_PYTHON'
    apps['LAST_CHG_DT'] = now

    engine = utils.create_engine()

    apps.to_sql('APPLICATION_TRAIN', engine, chunksize=1000, if_exists='append', method='multi', index=False)

    logger.info('collect_application_train end!!!')


def collect_application_test():
    ...


def collect_previous_application():
    logger.info('collect_previous_application start!')

    now = c_utils.strnow()

    preCols = ['SK_ID_PREV', 'SK_ID_CURR', 'NAME_CONTRACT_TYPE_PRE', 'AMT_ANNUITY_PRE', 'AMT_APPLICATION',
               'AMT_CREDIT_PRE', 'AMT_DOWN_PAYMENT', 'AMT_GOODS_PRICE_PRE', 'WEEKDAY_APPR_PROCESS_START_PRE',
               'HOUR_APPR_PROCESS_START_PRE', 'FLAG_LAST_APPL_PER_CONTRACT', 'NFLAG_LAST_APPL_IN_DAY',
               'RATE_DOWN_PAYMENT',
               'RATE_INTEREST_PRIMARY', 'RATE_INTEREST_PRIVILEGED', 'NAME_CASH_LOAN_PURPOSE', 'NAME_CONTRACT_STATUS',
               'DAYS_DECISION', 'NAME_PAYMENT_TYPE', 'CODE_REJECT_REASON', 'NAME_TYPE_SUITE_PRE', 'NAME_CLIENT_TYPE',
               'NAME_GOODS_CATEGORY', 'NAME_PORTFOLIO', 'NAME_PRODUCT_TYPE', 'CHANNEL_TYPE', 'SELLERPLACE_AREA',
               'NAME_SELLER_INDUSTRY', 'CNT_PAYMENT', 'NAME_YIELD_GROUP', 'PRODUCT_COMBINATION', 'DAYS_FIRST_DRAWING',
               'DAYS_FIRST_DUE', 'DAYS_LAST_DUE_1ST_VERSION', 'DAYS_LAST_DUE', 'DAYS_TERMINATION',
               'NFLAG_INSURED_ON_APPROVAL']
    app_dtype = {
        'SK_ID_PREV': np.object, 'SK_ID_CURR': np.object
    }
    prev = pd.read_csv(os.path.join(default_dir, 'previous_application.csv'), dtype=app_dtype)
    prev.columns = preCols
    prev_group = prev.groupby('SK_ID_CURR')
    # 집계대상 컬럼
    prev_number_columns = prev.dtypes[prev.dtypes != 'object'].index.tolist()
    # 집계정보 생성
    prev_agg = utils.func_create_agg_df(prev_number_columns, prev_group)

    prev_agg['FRST_RGTR'] = 'INIT_PYTHON'
    prev_agg['FRST_REG_DT'] = now
    prev_agg['LAST_CHNRG'] = 'INIT_PYTHON'
    prev_agg['LAST_CHG_DT'] = now

    engine = utils.create_engine()
    prev_agg.to_sql('PREVIOUS_APPLICATION', engine, chunksize=1000, if_exists='append', method='multi', index=False)

    logger.info('collect_previous_application end!!!')
    return 'aa'


def collect_bureau():
    logger.info('collect_bureau start!')
    now = c_utils.strnow()
    cols = ['SK_ID_CURR', 'SK_ID_BUREAU', 'CREDIT_ACTIVE', 'CREDIT_CURRENCY', 'DAYS_CREDIT', 'CREDIT_DAY_OVERDUE',
            'DAYS_CREDIT_ENDDATE', 'DAYS_ENDDATE_FACT', 'AMT_CREDIT_MAX_OVERDUE', 'CNT_CREDIT_PROLONG',
            'AMT_CREDIT_SUM', 'AMT_CREDIT_SUM_DEBT', 'AMT_CREDIT_SUM_LIMIT', 'AMT_CREDIT_SUM_OVERDUE', 'CREDIT_TYPE',
            'DAYS_CREDIT_UPDATE', 'AMT_ANNUITY_BRUE']
    app_dtype = {
        'SK_ID_BUREAU': np.object, 'SK_ID_CURR': np.object
    }
    bureau = pd.read_csv(os.path.join(default_dir, 'bureau.csv'), dtype=app_dtype)
    bureau.columns = cols
    bureau_group = bureau.groupby('SK_ID_CURR')
    bureau_number_columns = bureau.dtypes[bureau.dtypes != 'object'].index.tolist()

    bureau_agg = utils.func_create_agg_df(bureau_number_columns, bureau_group)

    bureau_agg['FRST_RGTR'] = 'INIT_PYTHON'
    bureau_agg['FRST_REG_DT'] = now
    bureau_agg['LAST_CHNRG'] = 'INIT_PYTHON'
    bureau_agg['LAST_CHG_DT'] = now

    engine = utils.create_engine()

    bureau_agg.to_sql('BUREAU', engine, chunksize=1000, if_exists='append', method='multi', index=False)

    logger.info('collect_bureau end!!!')


def collect_pos_cash_balance():
    logger.info('collect_pos_cash_balance start!')
    now = c_utils.strnow()

    app_dtype = {
        'SK_ID_PREV': np.object, 'SK_ID_CURR': np.object, 'MONTHS_BALANCE': np.int32, 'SK_DPD': np.int32,
        'SK_DPD_DEF': np.int32, 'CNT_INSTALMENT': np.float32, 'CNT_INSTALMENT_FUTURE': np.float32
    }

    pos_bal = pd.read_csv(os.path.join(default_dir, 'POS_CASH_balance.csv'), dtype=app_dtype)

    pos_balnumber_columns = pos_bal.dtypes[pos_bal.dtypes != 'object'].index.tolist()

    pos_group = pos_bal.groupby('SK_ID_CURR')

    pos_agg = utils.func_create_agg_df(pos_balnumber_columns, pos_group)

    pos_agg['FRST_RGTR'] = 'INIT_PYTHON'
    pos_agg['FRST_REG_DT'] = now
    pos_agg['LAST_CHNRG'] = 'INIT_PYTHON'
    pos_agg['LAST_CHG_DT'] = now

    engine = utils.create_engine()

    pos_agg.to_sql('POS_CASH_BALANCE', engine, chunksize=1000, if_exists='append', method='multi', index=False)

    logger.info('collect_pos_cash_balance end!!!')


def collect_installments_payments():
    logger.info('collect_installments_payments start!')
    now = c_utils.strnow()

    app_dtype = {
        'SK_ID_PREV': np.object, 'SK_ID_CURR': np.object, 'NUM_INSTALMENT_NUMBER': np.int32,
        'NUM_INSTALMENT_VERSION': np.float32, 'DAYS_INSTALMENT': np.float32, 'DAYS_ENTRY_PAYMENT': np.float32,
        'AMT_INSTALMENT': np.float32, 'AMT_PAYMENT': np.float32
    }
    install = pd.read_csv(os.path.join(default_dir, 'installments_payments.csv'), dtype=app_dtype)

    install_number_columns = install.dtypes[install.dtypes != 'object'].index.tolist()
    install_group = install.groupby('SK_ID_CURR')

    install_agg = utils.func_create_agg_df(install_number_columns, install_group)

    install_agg['FRST_RGTR'] = 'INIT_PYTHON'
    install_agg['FRST_REG_DT'] = now
    install_agg['LAST_CHNRG'] = 'INIT_PYTHON'
    install_agg['LAST_CHG_DT'] = now

    engine = utils.create_engine()

    install_agg.to_sql('INSTALLMENTS_PAYMENTS', engine, chunksize=1000, if_exists='append', method='multi', index=False)

    logger.info('collect_installments_payments end!!!')


def collect_credit_card_balance():
    logger.info('collect_credit_card_balance start!')
    now = c_utils.strnow()

    app_dtype = {
        'SK_ID_PREV': np.object, 'SK_ID_CURR': np.object, 'MONTHS_BALANCE': np.int16,
        'AMT_CREDIT_LIMIT_ACTUAL': np.int32, 'CNT_DRAWINGS_CURRENT': np.int32, 'SK_DPD': np.int32,
        'SK_DPD_DEF': np.int32, 'AMT_BALANCE': np.float32, 'AMT_DRAWINGS_ATM_CURRENT': np.float32,
        'AMT_DRAWINGS_CURRENT': np.float32, 'AMT_DRAWINGS_OTHER_CURRENT': np.float32,
        'AMT_DRAWINGS_POS_CURRENT': np.float32, 'AMT_INST_MIN_REGULARITY': np.float32,
        'AMT_PAYMENT_CURRENT': np.float32, 'AMT_PAYMENT_TOTAL_CURRENT': np.float32,
        'AMT_RECEIVABLE_PRINCIPAL': np.float32, 'AMT_RECIVABLE': np.float32, 'AMT_TOTAL_RECEIVABLE': np.float32,
        'CNT_DRAWINGS_ATM_CURRENT': np.float32, 'CNT_DRAWINGS_OTHER_CURRENT': np.float32,
        'CNT_DRAWINGS_POS_CURRENT': np.float32, 'CNT_INSTALMENT_MATURE_CUM': np.float32
    }
    card_bal = pd.read_csv(os.path.join(default_dir, 'credit_card_balance.csv'), dtype=app_dtype)

    card_bal.rename(
        columns={"MONTHS_BALANCE": "MONTHS_BALANCE_CARD", "NAME_CONTRACT_STATUS": "NAME_CONTRACT_STATUS_CARD",
                 "SK_DPD": "SK_DPD_CARD", "SK_DPD_DEF": "SK_DPD_DEF_CARD"}, inplace=True)

    card_number_columns = card_bal.dtypes[card_bal.dtypes != 'object'].index.tolist()
    card_group = card_bal.groupby('SK_ID_CURR')

    card_agg = utils.func_create_agg_df(card_number_columns, card_group)

    card_agg['FRST_RGTR'] = 'INIT_PYTHON'
    card_agg['FRST_REG_DT'] = now
    card_agg['LAST_CHNRG'] = 'INIT_PYTHON'
    card_agg['LAST_CHG_DT'] = now

    engine = utils.create_engine()

    card_agg.to_sql('CREDIT_CARD_BALANCE', engine, chunksize=1000, if_exists='append', method='multi', index=False)

    logger.info('collect_credit_card_balance end!!!')
