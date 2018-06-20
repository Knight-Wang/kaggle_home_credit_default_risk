

import numpy as np
import pandas as pd


def colYRatio(application_train, col, val):
    target_1 = np.logical_and(application_train[col] == val, application_train['target'] == 1)
    target_1_cnt = application_train.loc[target_1, :].shape[0]
    target_cnt = application_train.loc[application_train[col] == val, :].shape[0]
    target_0_cnt = target_cnt - target_1_cnt
    print('{}={}, target_1={}, target_0={}, target_1_ratio={}'.format(
                col, val, target_1_cnt, target_0_cnt, target_1_cnt / float(target_cnt)))

# 聚合函数，不同统计特征
def groupBy(df, grp_col, target_col):
    grp_df = df.groupby([grp_col])[target_col].agg(['count',
                    'mean', 'max', 'min', 'sum']).reset_index()
    # 最小值、最大值与均值的比重
    grp_df['min_mean_ratio'] = grp_df['min'] / (grp_df['mean'] + 0.9999)
    grp_df['max_mean_ratio'] = grp_df['max'] / (grp_df['mean'] + 0.9999)
    # 最小值与最大值的比重
    grp_df['min_max_ratio'] = grp_df['min'] / (grp_df['max'] + 0.9999)
    # 最小值、最大值、均值、中位数与总和的比重
    grp_df['min_sum_ratio'] = grp_df['min'] / (grp_df['sum'] + 0.9999)
    grp_df['max_sum_ratio'] = grp_df['max'] / (grp_df['sum'] + 0.9999)
    grp_df['mean_sum_ratio'] = grp_df['mean'] / (grp_df['sum'] + 0.9999)

    # 只保留占比
    feats_not_use = ['mean', 'max', 'min', 'sum']
    feats_in_use = [col for col in grp_df.columns if col not in feats_not_use]
    grp_df = grp_df[feats_in_use]

    # 重命名列
    grp_df.columns = [grp_col] + [target_col + '_' + col for col in grp_df.columns[1:]]
    return grp_df

# 重命名列
def renameColumns(grp_df, rename_col):
    grp_df.columns = ['sk_id_curr'] + [rename_col + '_' + col for col in grp_df.columns[1:]]
    return grp_df

# 转为哑变量
def getDummies(df, col):
    dummies_df = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummies_df], axis=1)
    return df

# 浮点数64位转为32位，整数型64位转为32位，节约内存
def convertType(df):
    for col in df.columns:
        if col != 'sk_id_curr':
            if df[col].dtype == np.dtype('float64'):
                df[col] = df[col].astype(np.float32)
            elif df[col].dtype == np.dtype('int64'):
                df[col] = df[col].astype(np.float32)
    return df

# xgb特征程度不高，丢弃
def notImportantfeat():
    lst = ['days_employed_365243', 'organization_type_XNA', 'hour_appr_process_start_22',
           'hour_appr_process_start_2', 'hour_appr_process_start_4', 'hour_appr_process_start_21',
           'hour_appr_process_start_20', 'hour_appr_process_start_1', 'wallsmaterial_mode_Monolithic',
           'wallsmaterial_mode_Mixed', 'organization_type_Insurance', 'organization_type_Security Ministries',
           'organization_type_Cleaning', 'organization_type_Electricity', 'organization_type_Telecom',
           'organization_type_Agriculture', 'organization_type_University', 'organization_type_Culture',
           'organization_type_Advertising', 'organization_type_Services', 'organization_type_Emergency',
           'organization_type_Mobile', 'Bad debt', 'days_credit_count', 'credit_day_overdue_min_mean_ratio',
           'credit_day_overdue7_ratio', 'credit_day_overdue_count', 'credit_day_overdue_min_max_ratio',
           'day_amt_overdue_min_mean_ratio_count', 'amt_credit_sum_overdue_min_mean_ratio',
           'amt_credit_sum_count', 'amt_credit_sum_overdue_count', 'amt_credit_sum_overdue_min_mean_ratio']
    return lst



'''
Index(['sk_id_prev', 'sk_id_curr', 'months_balance', 'amt_balance',
       'amt_credit_limit_actual', 'amt_drawings_atm_current',
       'amt_drawings_current', 'amt_drawings_other_current',
       'amt_drawings_pos_current', 'amt_inst_min_regularity',
       'amt_payment_current', 'amt_payment_total_current',
       'amt_receivable_principal', 'amt_recivable', 'amt_total_receivable',
       'cnt_drawings_atm_current', 'cnt_drawings_current',
       'cnt_drawings_other_current', 'cnt_drawings_pos_current',
       'cnt_instalment_mature_cum', 'name_contract_status', 'sk_dpd',
       'sk_dpd_def'],

credit_card_balance.loc[credit_card_balance['sk_id_curr']==378907, ['sk_id_prev', 'months_balance']]

df['sk_id_curr'].duplicated().value_counts()


'''
