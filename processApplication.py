
import pandas as pd
import numpy as np
from util import colYRatio
from util import convertType
from util import getDummies
from util import notImportantfeat
from util import curPreCol

'''
统计缺失情况
name_contract_type: 贷款类型
code_gender: 性别, XNA为缺失
flag_own_car: 是否有车
flag_own_realty: 是否有房
children_cnt: 申请人拥有的孩子数
amt_income_total: 用户收入
amt_credit: 贷款信用额度
amt_annuity: 年金贷款
amt_goods_price: 贷款物品的价格
name_income_type: 陪申请人的人
name_income_type: 用户收入类型
name_education_type: 用户的最高学历
name_family_status: 用户的家庭状态
name_housing_type: 用户的住房情况如何
region_population_relative: 用户居住地区的规范化人口
days_birth: 用户申请贷款时的年龄
days_employed: 申请前多少天，用户开始当前工作
days_registration: 申请前多少天，更改注册
days_id_publish: 申请前多少天，更改申请贷款的身份证件
own_car_age: 车辆年龄
flag_mobil: 是否提高手机号
flag_emp_phone: 工作电话号码
flag_work_phone: 家庭电话号码
flag_cont_mobile: 移动电话能不能打得通
flag_phone: 家庭电话号码
flag_email: 是否提供邮箱地址
occupation_type: 职业
cnt_fam_members: 用户的家庭成员
region_rating_client: 用户地区评级
region_rating_client_w_city: region_rating_client_w_city
weekday_appr_process_start: 周一到周五，哪天申请贷款
hour_appr_process_start: 哪个时间段（小时）申请贷款
reg_region_not_live_region: 用户常驻地址与联系地址是否不同
reg_region_not_work_region: 常驻地址与工作地址是否不同
live_region_not_work_region: 联系地址与工作地址是否不同
reg_city_not_live_city: 常驻地址与联系地址，城市级别
reg_city_not_work_city: 常驻地址与工作地址，城市级别
live_city_not_work_city: 联系地址与工作地址，城市级别
organization_type: 客户工作的组织类型
ext_source_1: 外部来源
ext_source_2: 外部来源
ext_source_3: 外部来源
obs_30_cnt_social_circle: 30天内违约多少次
def_30_cnt_social_circle: 30天内违约多少次
obs_60_cnt_social_circle: 60天内违约多少次
def_60_cnt_social_circle: 60天内违约多少次
days_last_phone_change: 申请前多少天改变手机号
amt_req_credit_bureau_hour: 申请前一小时的查询次数
amt_req_credit_bureau_day: 申请前一天的查询次数
amt_req_credit_bureau_week: 申请前一星期的查询次数
amt_req_credit_bureau_mon: 申请前一个月的查询次数
amt_req_credit_bureau_qrt: 申请前一个季度的查询次数
amt_req_credit_bureau_year: 申请前一年的查询次数
'''

def processApplicationData(df, df2):
    # 现金贷款: 1, 循环贷款: 0, 主要为现金贷款326537, 循环贷款29718，没用丢弃
    df['name_contract_type'] = df['name_contract_type'].map(lambda x: 1 if x == 'Cash loans' else 0)

    # 女: 235126, 男: 121125, XNA: 4，统计男女的不同情况，如年金
    df['gender_female'] = df['code_gender'].map(lambda x: 1 if x == 'F' else 0)
    df['gender_male'] = df['code_gender'].map(lambda x: 1 if x == 'M' else 0)

    # 是否有车，121020
    df['flag_own_car'] = df['flag_own_car'].map(lambda x: 1 if x == 'Y' else 0)
    # 是否有房，246970
    df['flag_own_realty'] = df['flag_own_realty'].map(lambda x: 1 if x == 'Y' else 0)
    # 是否有房有车，没用丢弃
    # df['flag_own_car_realty'] = df['flag_own_car'] + df['flag_own_realty']
    # df['flag_own_car_realty'] = df['flag_own_car_realty'].map(lambda x: 1 if x == 2 else 0)

    # 申请人拥有的孩子数，用户收入和孩子数
    df['amt_income_per_child'] = df['amt_income_total'] / (df['children_cnt'] + 1.0)

    # 贷款信用额度 / 用户收入
    df['amt_credit_income_ratio'] = df['amt_credit'] / (df['amt_income_total'] + 1.0)

    # 年金贷款，也是一种类型贷款，https://www.finweb.com/loans/what-is-an-annuity-loan.html
    df['amt_annuity'].fillna(0, inplace=True)
    # 年金贷款 / 贷款信用额度
    df['amt_annuity_credit_ratio'] = df['amt_annuity'] / (df['amt_credit'] + 1.0)
    # 年金贷款 / 用户收入
    df['amt_annuity_income_ratio'] = df['amt_annuity'] / (df['amt_income_total'] + 1.0)

    # 用户贷款，给的价格
    df['amt_goods_price'].fillna(0, inplace=True)
    df['amt_goods_price_income_ratio'] = df['amt_goods_price'] / (df['amt_income_total'] + 1.0)
    df['amt_goods_price_credit_ratio'] = df['amt_goods_price'] / (df['amt_credit'] + 1.0)
    df['amt_goods_price_annuity_ratio'] = df['amt_goods_price'] / (df['amt_annuity'] + 1.0)

    # 陪客户申请贷款的人，没用丢弃
    # df = getDummies(df, 'name_type_suite')
    # drop_lst = ['Children', 'Other_B', 'Other_A', 'Group of people']
    # drop_lst = ['name_type_suite_' + col for col in drop_lst]
    # df.drop(drop_lst, axis=1, inplace=True)

    # 用户收入类型，可以丢弃
    df = getDummies(df, 'name_income_type')
    drop_lst = ['Unemployed', 'Student', 'Businessman', 'Maternity leave']
    drop_lst = ['name_income_type_' + col for col in drop_lst]
    df.drop(drop_lst, axis=1, inplace=True)

    # 用户的最高学历，是否为高学历
    df['name_education_type_Higher_education'] = df['name_education_type'].map(
                        lambda x: 1 if x == 'Higher education' else x)
    df['name_education_type_Secondary'] = df['name_contract_type'].map(
                        lambda x: 1 if x == 'Secondary / secondary special' else x)

    # 用户的家庭状态，结婚、单身这些，和小孩数结合做特征
    for i in range(0, 3):
        df['married_children_cnt_' + str(i)] = df.loc[
                        df['name_family_status'] == 'Married', 'cnt_children'].map(lambda x: 1 if x == i else 0)
        df['single_children_cnt_' + str(i)] = df.loc[
                        df['name_family_status'] == 'Single / not married', 'cnt_children'].map(lambda x: 1 if x == i else 0)

    df['name_family_status_Married'] = df['name_family_status'].map(lambda x: 1 if x == 'Married' else 0)
    # df = getDummies(df, 'name_family_status')
    # # unknown只有两个人，丢弃
    # df.drop(['name_family_status_Unknown'], axis=1, inplace=True)

    # 客户的住房情况如何（租房，与父母同住，...）
    # df = getDummies(df, 'name_housing_type')
    df['name_housing_type_house'] = (df['name_housing_type'] == 'House / apartment').astype('int')

    # 用户居住地区的规范化人口（数字越高意味着用户居住在人口较多的地区）
    # 用户的居住地区和用户收入、年金贷款等比重
    for col in ['amt_income_total', 'amt_credit', 'amt_annuity', 'amt_goods_price',
                'amt_income_per_child', 'amt_credit_income_ratio', 'amt_annuity_credit_ratio',
                'amt_annuity_income_ratio', 'amt_goods_price_income_ratio', 'amt_goods_price_credit_ratio',
                'amt_goods_price_annuity_ratio']:
        grp_mean_df = df.groupby(['region_population_relative'])[col].mean().reset_index().rename(columns={col: 'mean'})
        grp_mean_df = pd.merge(df[['sk_id_curr', 'region_population_relative', col]], grp_mean_df, on='region_population_relative', how='left')
        grp_mean_df[col + '_per_region_rate'] = grp_mean_df[col] / (grp_mean_df['mean'] + 1.0)
        df = df.merge(grp_mean_df[['sk_id_curr', col + '_per_region_rate']], on='sk_id_curr', how='left')

    # 用户申请贷款时的年龄，都为负数，脱敏？
    for i in range(1, 4):
        df['ext_source_' + str(i) + '_birth'] = df['ext_source_' + str(i)] / df['days_birth']
        df['ext_source_' + str(i) + '_birth'].fillna(-1, inplace=True)

    # 外部来源除以收入这些
    for col in ['amt_income_total', 'amt_credit', 'amt_annuity', 'amt_goods_price']:
        df['ext_source_' + col] = df['ext_source_1'] / (df[col] + 1)
        df['ext_source_' + col].fillna(-1, inplace=True)

    # 外部数据源
    for i in range(1, 4):
        df['ext_source_' + str(i)].fillna(-1, inplace=True)

    # 年龄 / 用户收入、贷款信用额度、年金贷款、贷款物品价格
    for col in ['amt_income_total', 'amt_credit', 'amt_annuity', 'amt_goods_price']:
        df['days_birth_' + col + '_rate'] / (df[col] + 1.0)

    # 年龄为权重，年金贷款 / 贷款信用额度
    df['birth_amt_annuity_credit_ratio'] = df['days_birth'] * df['amt_annuity_credit_ratio']

    # 申请前多少天，用户开始当前工作？数据脱敏，365243有64648条
    # xgb特征程度不高，丢弃
    #df['days_employed_365243'] = (df['days_employed'] == 365243).astype('int')
    df['days_employed'].fillna(365243, inplace=True)
    df['days_employed_birth'] = df['days_employed'] / df['days_birth']

    # 申请前多少天，更改注册，负数脱敏
    df['days_registration_birth'] = df['days_registration'] / df['days_birth']

    # 申请前多少天，更改申请贷款的身份证件，负数脱敏
    df['days_id_publish_birth'] = df['days_id_publish'] / df['days_birth']

    # 车辆年龄，注意有6名用户持有车，但不知道车龄，填充中位数9
    df.loc[df['flag_own_car'] == 1, 'own_car_age'].fillna(9, inplace=True)
    # 没车的，填充-1
    df['own_car_age'].fillna(-1, inplace=True)
    # 车龄 / 年龄
    df['own_car_age_birth'] = df['own_car_age'] / df['days_birth']

    # 只有两名用户没提供手机号，大部分为同一个值没用丢弃
    #df['flag_mobil']

    # 工作电话号码，没的可能没工作
    #df['flag_emp_phone']

    # 家庭电话号码
    #df['flag_work_phone']

    # 家庭电话和工作电话都没的
    # df['flag_emp_work_phone'] = df['flag_emp_phone'] + df['flag_work_phone']
    # df['flag_emp_work_phone'] = df['flag_emp_work_phone'].map(lambda x: 1 if x > 1 else x)

    # 移动电话能不能打得通，大部分为同一个值没用丢弃
    #df['flag_cont_mobile']

    # 家庭电话号码？数据不一样，但给的列名意思是这个
    #df['flag_phone']

    # 是否提供邮箱地址
    #df['flag_email']

    # 是否有联系方式
    df['flag_contact_nums'] = 0
    for col in ['flag_emp_phone', 'flag_work_phone', 'flag_phone', 'flag_email']:
        df['flag_contact_nums'] += df[col]
    # df['flag_contact'] = df['flag_contact_nums'].map(lambda x: 1 if x > 1 else 0)

    # 职业
    df['occupation_type'].fillna('unknown', inplace=True)
    # 合并下
    df['occupation_type'] = df['occupation_type'].replace('IT staff', 'High skill tech staff')
    df['occupation_type'] = df['occupation_type'].replace('Waiters/barmen staff', 'Low-skill Laborers')
    df['occupation_type'] = df['occupation_type'].replace('Realty agents', 'Sales staff')
    df['occupation_type'] = df['occupation_type'].replace('HR staff', 'High skill tech staff')
    df['occupation_type'] = df['occupation_type'].replace('Secretaries', 'High skill tech staff')
    df = getDummies(df, 'occupation_type')

    # 用户的家庭成员，两名缺失的填众数2
    df['cnt_fam_members'].fillna(2, inplace=True)
    # 家庭成员 / 用户收入、贷款信用额度、年金贷款、贷款物品价格
    for col in ['amt_income_total', 'amt_credit', 'amt_annuity', 'amt_goods_price']:
        df['cnt_fam_' + col] = df['cnt_fam_members'] / (df[col] + 1.0)

    # df.loc[df['cnt_fam_members'] > 4.0, 'cnt_fam_members'] = 4
    # df = getDummies(df, 'cnt_fam_members')

    df['region_city_rating_client'] = df['region_rating_client'] + df['region_rating_client_w_city']
    df = getDummies(df, 'region_city_rating_client')

    # 用户地区评级
    df = getDummies(df, 'region_rating_client')

    # 用户城市评级
    df = getDummies(df, 'region_rating_client_w_city')
    df.drop(['region_rating_client_w_city_-1'], axis=1, inplace=True)

    # 周一到周五，哪天申请贷款
    # df = getDummies(df, 'weekday_appr_process_start')
    #
    # # 哪个时间段（小时）申请贷款
    # df = getDummies(df, 'hour_appr_process_start')

    # 用户常驻地址与联系地址是否不同，不在同一区域，1不同，0相同
    # 常驻地址与工作地址是否不同，不在同一区域
    # 联系地址与工作地址是否不同，不在同一区域
    # df['not_reg_region_num'] = 0
    # for col in ['reg_region_not_live_region', 'reg_region_not_work_region', 'live_region_not_work_region']:
    #     df['not_reg_region_num'] += df[col]

    # 常驻地址与联系地址，城市级别
    # 常驻地址与工作地址，城市级别
    # 联系地址与工作地址，城市级别
    df['not_reg_city_city_num'] = 0
    for col in ['reg_city_not_live_city', 'reg_city_not_work_city', 'live_city_not_work_city']:
        df['not_reg_city_city_num'] += df[col]

    # 客户工作的组织类型
    # 把Industry的各种type合并
    df['organization_type_Self-employed'] = df['organization_type'].map(lambda x: 1 if x == 'Self-employed' else 0)
    df['organization_type_Business'] = df['organization_type'].map(
        lambda x: 1 if x in['Business Entity Type 2', 'Business Entity Type 1',
                            'Business Entity Type 3'] else 0)
    df['organization_type_Construction'] = df['organization_type'].map(lambda x: 1 if x == 'Construction' else 0)

    # 住宅面积和用户收入
    for col in ['amt_income_total', 'amt_credit', 'amt_annuity', 'amt_goods_price']:
        df['totalarea_mode_' + col] = df['totalarea_mode'] / (df[col] + 1.0)

    # 住宅信息，均值、众数、中位数
    for col in ['apartments_avg', 'basementarea_avg', 'years_beginexpluatation_avg',
                'years_build_avg', 'commonarea_avg', 'elevators_avg', 'entrances_avg',
                'floorsmax_avg', 'floorsmin_avg', 'landarea_avg',  'livingapartments_avg',
                'livingarea_avg', 'nonlivingapartments_avg', 'nonlivingarea_avg',
                'apartments_mode', 'basementarea_mode', 'years_beginexpluatation_mode',
                'years_build_mode', 'commonarea_mode', 'elevators_mode', 'entrances_mode',
                'floorsmax_mode', 'floorsmin_mode', 'landarea_mode', 'livingapartments_mode',
                'livingarea_mode', 'nonlivingapartments_mode', 'nonlivingarea_mode',
                'apartments_medi', 'basementarea_medi', 'years_beginexpluatation_medi',
                'years_build_medi', 'commonarea_medi', 'elevators_medi', 'entrances_medi',
                'floorsmax_medi', 'floorsmin_medi', 'landarea_medi', 'livingapartments_medi',
                'livingarea_medi', 'nonlivingapartments_medi', 'nonlivingarea_medi',
                'totalarea_mode', 'weekday_appr_process_start']:
        df[col].fillna(-1, inplace=True)

    # for col in ['fondkapremont_mode', 'housetype_mode', 'wallsmaterial_mode', 'emergencystate_mode']:
    #     #df[col].fillna('unknown', inplace=True)
    #     df = getDummies(df, col)

    # 30天内违约多少次，观察违约次数和y值关系, util.colYRatio
    # for i in range(10):
    #     colYRatio(df, 'obs_30_cnt_social_circle', i)
    # 缺失填充0
    df['obs_30_cnt_social_circle'].fillna(0, inplace=True)
    # df.loc[df['obs_30_cnt_social_circle'] > 5, 'obs_30_cnt_social_circle'] = 5
    # df = getDummies(df, 'obs_30_cnt_social_circle')

    # 30天内违约多少次
    df['def_30_cnt_social_circle_0'] = (df['def_30_cnt_social_circle'] == 0).astype('int')
    df['def_30_cnt_social_circle'].fillna(0, inplace=True)

    # 60天内违约多少次
    df['obs_60_cnt_social_circle'].fillna(0, inplace=True)

    # 60天内违约多少次
    df['def_60_cnt_social_circle'].fillna(0, inplace=True)

    # 申请前多少天改变手机号，重要变量
    df['days_last_phone_change'].fillna(0, inplace=True)
    # df['days_last_phone_change_0'] = (df['days_last_phone_change'] == 0).astype('int')

    # 提供文档和y值的关系，即通过比例
    # for doc in range(2, 22):
    #     print('flag_document_' + str(doc))
    #     for val in range(2):
    #         colYRatio(df, 'flag_document_' + str(doc), val)
    # 总共提交了文档数
    df['flag_document_nums'] = 0
    for doc in range(2, 22):
        df['flag_document_nums'] = df['flag_document_nums'] + df['flag_document_' + str(doc)]

    # 申请前一小时、前一天、前一星期、前一个月、前一个季度、前一年的查询次数
    # 随时间增大，重要性增加
    for col in ['amt_req_credit_bureau_hour', 'amt_req_credit_bureau_day',
                'amt_req_credit_bureau_week', 'amt_req_credit_bureau_mon',
                'amt_req_credit_bureau_qrt', 'amt_req_credit_bureau_year']:
        df[col].fillna(0, inplace=True)

    # ---------------------------------- 组合特征 ----------------------------------
    '''与previous_application_df进行组合对比'''

    # 年金贷款 / 过去的年金贷款
    df = curPreCol(df, df2, 'amt_annuity', 'amt_annuity', 'cur_pre_amt_annuity')
    # 年金贷款 / 过去的申请贷款金额
    df = curPreCol(df, df2, 'amt_annuity', 'amt_application', 'cur_pre_amt_annuity_application')
    # 贷款信用额度 / 过去的申请贷款金额
    df = curPreCol(df, df2, 'amt_credit', 'amt_application', 'cur_pre_amt_credit_application')
    # 用户收入 / 过去的申请贷款金额
    df = curPreCol(df, df2, 'amt_income_total', 'amt_application', 'cur_pre_amt_income_application')
    # 贷款物品价格 / 过去的申请贷款金额
    df = curPreCol(df, df2, 'amt_goods_price', 'amt_application', 'cur_pre_amt_goods_application')

    # 年金贷款 / 过去的批准贷款金额
    df = curPreCol(df, df2, 'amt_annuity', 'amt_credit', 'cur_pre_amt_annuity_credit')
    # 贷款信用额度 / 过去的批准贷款金额
    df = curPreCol(df, df2, 'amt_credit', 'amt_credit', 'cur_pre_amt_credit')
    # 用户收入 / 过去的批准贷款金额
    df = curPreCol(df, df2, 'amt_income_total', 'amt_credit', 'cur_pre_amt_income_credit')
    # 贷款物品价格 / 过去的批准贷款金额
    df = curPreCol(df, df2, 'amt_goods_price', 'amt_credit', 'cur_pre_amt_goods_credit')

    # 年金贷款 / 过去的首付
    df = curPreCol(df, df2, 'amt_annuity', 'amt_down_payment', 'cur_pre_amt_annuity_down_payment')
    # 贷款信用额度 / 过去的首付
    df = curPreCol(df, df2, 'amt_credit', 'amt_down_payment', 'cur_pre_amt_credit_down_payment')
    # 用户收入 / 过去的首付
    df = curPreCol(df, df2, 'amt_income_total', 'amt_down_payment', 'cur_pre_amt_income_down_payment')
    # 贷款物品价格 / 过去的首付
    df = curPreCol(df, df2, 'amt_goods_price', 'amt_down_payment', 'cur_pre_amt_goods_down_payment')

    # 年金贷款 / 过去的物品价格
    df = curPreCol(df, df2, 'amt_annuity', 'amt_goods_price', 'cur_pre_amt_annuity_goods_price')
    # 贷款信用额度 / 过去的物品价格
    df = curPreCol(df, df2, 'amt_credit', 'amt_goods_price', 'cur_pre_amt_credit_goods_price')
    # 用户收入 / 过去的物品价格
    df = curPreCol(df, df2, 'amt_income_total', 'amt_goods_price', 'cur_pre_amt_income_goods_price')
    # 贷款物品价格 / 过去的物品价格
    df = curPreCol(df, df2, 'amt_goods_price', 'amt_goods_price', 'cur_pre_amt_goods_price')

    # ---------------------------------- 最近一期的对比组合特征 ----------------------------------



    feats_not_use = ['code_gender', 'cnt_children', 'name_type_suite', 'name_income_type',
                     'name_education_type', 'name_family_status', 'name_housing_type',
                     'occupation_type', 'region_rating_client', 'name_contract_type'
                     'region_rating_client_w_city', 'weekday_appr_process_start',
                     'hour_appr_process_start', 'organization_type', 'fondkapremont_mode',
                     'housetype_mode', 'wallsmaterial_mode', 'emergencystate_mode',
                     'flag_mobil', 'flag_emp_phone', 'flag_cont_mobile', 'live_city_not_work_city',
                     'flag_document_14', 'flag_document_11', 'cnt_fam_members'
                     'flag_document_16', 'flag_document_18', 'flag_document_9',
                     'flag_document_2', 'flag_document_15', 'reg_city_not_work_city',
                     'flag_document_19', 'flag_document_13', 'flag_document_6', 'flag_document_5',
                     'flag_document_8', 'weekday_appr_process_start', 'hour_appr_process_start',
                     'amt_req_credit_bureau_hour', 'amt_req_credit_bureau_day',
                     'amt_req_credit_bureau_week', 'amt_req_credit_bureau_mon']
    feats_not_use = feats_not_use + notImportantfeat()
    feats_in_use = [col for col in df.columns if col not in feats_not_use]

    return convertType(df[feats_in_use])
    #return df[feats_in_use]

if __name__ == '__main__':
    # 主表，所有应用的统计数据
    application_train = pd.read_csv('raw_data/application_train.csv')
    # 测试集
    application_test = pd.read_csv('raw_data/application_test.csv')
    # 合并
    application_df = pd.concat([application_train, application_test], axis=0)
    application_df.columns = [col.lower() for col in application_df.columns]
    application_df.index = range(len(application_df))

    previous_application_df = pd.read_csv('raw_data/previous_application.csv')
    previous_application_df.columns = [col.lower() for col in previous_application_df.columns]
    # 数据处理及特征工程
    process_application_df = processApplicationData(application_df, previous_application_df)


