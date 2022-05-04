import pandas as pd


def under_sampler(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    df_t1 = df[df[condition] == 1]
    df_t0 = df[df[condition] == 0].sample(len(df_t1), random_state=2022)

    return pd.concat([df_t1, df_t0])


def min_max_scaler(df_col, min, max):
    df_col = (df_col - min) / (max - min)
    return df_col


def aggregate_df(cols: list, gr_df: pd.DataFrame) -> pd.DataFrame:
    aggr_df = pd.DataFrame()
    for col in cols:
        aggr_df[col + '_SUM'] = gr_df[col].sum()

    agg_df = aggr_df.reset_index()
    return aggr_df