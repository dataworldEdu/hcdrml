import pandas as pd
from app.data import utils
from app.common import logger
logger = logger.getLogger(__name__)


def nvl(data: pd.DataFrame):
    ...


def one_hot_encoding(data: pd.DataFrame):
    logger.debug('one hot encoding start')
    # object type 확인 --> 원핫인코딩
    logger.debug('one hot encoding step - 1')
    object_columns = data.dtypes[data.dtypes == 'object'].index.tolist()
    object_columns = object_columns[1:]

    # object feature에 대한 one-hot encoding
    # 해당 규칙은 실시간 예측시에 사용해야 함으로 불변할 수 있도록 해야한다.
    # NAME_CONTRACT_TYPE 컬럼에 값이 뭔지를 확인 하고, NAME_CONTRACT_TYPE_0, NAME_CONTRACT_TYPE_1 컬럼을 생성 후 해당 값이 Cash loans 이면 0번 컬럼에, Revolving loans 이면 1번 컬럼에 '1'을 생성, 나머지는 '0', 정의되지 않은 값은 기타컬럼에 '1'생성
    encodingColsTemp = []
    encodingCols = []
    logger.debug('one hot encoding step - 2')
    for idx, col in enumerate(object_columns):
        uniVal = data[col].value_counts().index
        for jdx, val in enumerate(uniVal):
            newCol = col + '_' + str(jdx)
            encodingColsTemp.append([newCol, val])
            # one hot 컬럼 생성
            data[newCol] = data[col].apply(lambda x: 1 if x == val else 0)
            etcIdx = jdx + 1
        # 기타 값 컬럼 생성(실시간 예측시 학습에 없던 데이터가 들어오면 기타컬럼에 1을 생성)
        newCol = col + '_' + str(etcIdx)
        data[newCol] = 0
        encodingColsTemp.append([newCol, 0])
        # 원본 컬럼 삭제
        data = data.drop([col], axis=1)
        # 원핫 기준정보 저장
        encodingCols.append([col, encodingColsTemp])
    logger.debug('one hot encoding end')
    return data


def fill_na(data: pd.DataFrame):
    object_columns = data.dtypes[data.dtypes == 'object'].index.tolist()
    num_columns = data.dtypes[data.dtypes != 'object'].index.tolist()
    #num_columns = num_columns[2:]

    for col in object_columns:
        data[col] = data[col].fillna('XX')

    for col in num_columns:
        data[col] = data[col].fillna(0)

    return data
