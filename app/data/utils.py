import pandas as pd
import sqlalchemy
from sqlalchemy import event
from .. import config
from app.common import logger

logger = logger.getLogger(__name__)


def under_sampler(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    dfT1 = df[df[condition] == 1]
    dfT0 = df[df[condition] == 0]
    dfT0_temp = dfT0.sample(len(dfT1), random_state=2022)

    new_df = pd.concat([dfT1, dfT0_temp])

    del dfT1, dfT0, dfT0_temp

    return new_df


def create_engine():
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{config.DBSETTING.get("user")}:{config.DBSETTING.get("passwd")}'
                                      f'@{config.DBSETTING.get("host")}:{config.DBSETTING.get("port")}'
                                      f'/{config.DBSETTING.get("database")}?{config.DBSETTING.get("charset")}')

    @event.listens_for(engine, "before_cursor_execute")
    def receive_before_cursor_execute(
            conn, cursor, statement, params, context, executemany
    ):
        if executemany:
            cursor.fast_executemany = True

    return engine


def min_max_scaler(df_col, min, max):
    df_col = (df_col - min) / (max - min)
    return df_col


def func_create_agg_df(columns, gr_df):
    agg_df = pd.DataFrame()
    for col in columns:
        sum_col = col + '_SUM'
        agg_df[sum_col] = gr_df[col].sum()

    agg_df = agg_df.reset_index()
    return agg_df
