import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def day_interval():
    df = pd.read_csv('./afenti_pay_more_than_2.csv',sep='\t', header=None,
        names= ['pay_status', 'pay_amount', 'pay_method', 'product_service_type', 'total_price', 'school_id',
        'user_id', 'activate_datetime', 'service_start_datetime','service_end_datetime', 'clazz_id', 'region_code'])
    df_paid = df[df['pay_status']=='Paid']
    df_paid = df_paid.sort('activate_datetime')

    df_paid['pay'] = pd.to_datetime(df_paid['activate_datetime'],format = "%Y-%m-%d")
    df_paid['start'] = pd.to_datetime(df_paid['service_start_datetime'],format='%Y-%m-%d')
    df_paid['end'] = pd.to_datetime(df_paid['service_end_datetime'],format='%Y-%m-%d')

    df_pay = df_paid.groupby('user_id',sort=False,).apply(lambda x: x.pay.nsmallest(2))
    df_start = df_paid.groupby('user_id',sort=False).apply(lambda x:x.start.nsmallest(1))
    df_end = df_paid.groupby('user_id',sort=False).apply(lambda x:x.end.nsmallest(1))

    df_pay = df_pay.reset_index()
    df_start = df_start.reset_index()
    df_end = df_end.reset_index()

    del df_start['level_1']
    del df_end['level_1']
    del df_pay['level_1']

    df_pay_0 = df_pay.iloc[0::2]    
    df_pay_1 = df_pay.iloc[1::2]
    df_pay_join = pd.merge(df_pay_0,df_pay_1,on='user_id',how='inner')
    df_pay_join['pay_diff'] = (df_pay_join['pay_y'] - df_pay_join['pay_x'])
    df_pay_join['pay'] = df_pay_join['pay_diff'].apply(lambda x :x.days)    

    del df_pay_join['pay_x']
    del df_pay_join['pay_y']

    df_usage_join = pd.merge(df_start,df_end, on='user_id', how ='inner')
    df_usage_join['usage_diff'] = (df_usage_join['end'] - df_usage_join['start'])
    df_usage_join['usage'] = df_usage_join['usage_diff'].apply(lambda x :x.days)    
    df_pay_usage = pd.merge(df_usage_join, df_pay_join, on ='user_id', how  ='inner')
    pay_usage  = df_pay_usage[['usage','pay']]
    print pay_usage.head()
    pay_usage.to_csv('pay_repay_7.7.csv')
def retention():
    df = pd.read_csv('./afenti_pay_more_than_2.csv',sep='\t', header=None,
        names= ['pay_status', 'pay_amount', 'pay_method', 'product_service_type', 'total_price', 'school_id',
        'user_id', 'activate_datetime', 'service_start_datetime','service_end_datetime', 'clazz_id', 'region_code'])
    df = df[['pay_status','pay_amount','user_id','service_start_datetime']]
    df_paid = df[df['pay_status']=='Paid']
    df_paid['start'] = pd.to_datetime(df_paid['service_start_datetime'],format='%Y-%m-%d')

    df_count = df_paid.groupby('user_id')['pay_status'].count()
    
    df_first = df_paid.groupby('user_id').apply(lambda x:x.start.nlargest(1))
    df_first = df_first.reset_index()#.set_index(['user_id','start'])
    df_first['end'] = 999
    del df_first['level_1']

    df_join = pd.merge(df_paid,df_first,on=['start','user_id'], how='left')
    del df_join['service_start_datetime']
    del df_join['pay_status']
    df_join.to_csv('pay_retention.csv',index=False)
def first():
    df = pd.read_csv('./afenti_pay_more_than_2.csv',sep='\t', header=None,
        names= ['pay_status', 'pay_amount', 'pay_method', 'product_service_type', 'total_price', 'school_id',
        'user_id', 'activate_datetime', 'service_start_datetime','service_end_datetime', 'clazz_id', 'region_code'])
    df = df[['pay_status','pay_amount','user_id','service_start_datetime']]
    df_paid = df[df['pay_status']=='Paid']
    df_paid['start'] = pd.to_datetime(df_paid['service_start_datetime'],format='%Y-%m-%d')

    df_count = df_paid.groupby('user_id')['pay_status'].count()
    
    df_first = df_paid.groupby('user_id').apply(lambda x:x.start.nsmallest(1))
    df_first = df_first.reset_index()
    df_first['first'] = 000
    del df_first['level_1']

    df_join = pd.merge(df_paid,df_first,on=['start','user_id'], how='right')
    del df_join['service_start_datetime']
    del df_join['pay_status']
    df_join.to_csv('pay_first.csv',index=False)
def second():
    df = pd.read_csv('./afenti_pay_more_than_2.csv',sep='\t', header=None,
        names= ['pay_status', 'pay_amount', 'pay_method', 'product_service_type', 'total_price', 'school_id',
        'user_id', 'activate_datetime', 'service_start_datetime','service_end_datetime', 'clazz_id', 'region_code'])
    df = df[['pay_status','pay_amount','user_id','service_start_datetime']]
    df_paid = df[df['pay_status']=='Paid']
    df_paid['start'] = pd.to_datetime(df_paid['service_start_datetime'],format='%Y-%m-%d')
    df_paid = df_paid.sort('start')
    df_first = df_paid.groupby('user_id').nth(0)
    print df_first.shape[0]

    print df_first.head()
    df_second = df_paid.groupby('user_id').nth(1)
    print df_second.shape[0]
    print df_second.head()


    df_third = df_paid.groupby('user_id').nth(2)
    print df_third.shape[0]
    print df_third.head()

    # df_join.to_csv('pay_second.csv',index=False)
def pay_repay_plot():
    df = pd.read_csv('./pay_repay_7.7.csv')
    # df.set_index('user_id',inplace=True)
    # df =df.sort('usage')
    
    df10 = df[df['usage']==10]
    df15 = df[df['usage']==15]
    df30 = df[df['usage']==30]
    df90 = df[df['usage']==90]
    df180 = df[df['usage']==180]
    df365 = df[df['usage']==365]


    # print df10.pay.min()
    # counts, bins = np.histogram(df10.repay.values,bins=48,range=[0,240])
    # result = pd.Series(counts, index=bins[:-1])
    # print df10.repay.value_counts(bins=48)
    fig1 = df365.pay.hist(bins=35)
    fig1.set_xlim([-10,140])
    plt.show()
def retention_cal():
    df = pd.read_csv('pay_retention.csv')
    df10 = df[df['pay_amount']==10]
    df15 = df[df['pay_amount']==15]
    df30 = df[df['pay_amount']==29]
    df90 = df[df['pay_amount']==80]
    df180 = df[df['pay_amount']==158]
    df365 = df[df['pay_amount']==300]

    print 1- df10.end.count()/float(df10.shape[0])
    print 1- df15.end.count()/float(df15.shape[0])
    print 1- df30.end.count()/float(df30.shape[0])
    print 1- df90.end.count()/float(df90.shape[0])
    print 1- df180.end.count()/float(df180.shape[0])
    print 1- df365.end.count()/float(df365.shape[0])
def first_cal():
    df = pd.read_csv('pay_first.csv')
    print df.shape[0]
    print df.pay_amount.value_counts()


if __name__ == '__main__':
    # day_interval()
    # pay_repay_plot()
    # retention()
    # retention_cal()
    # first()
    # first_cal()
    second()