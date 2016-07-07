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
    df_usage = df_paid.groupby('user_id',sort=False).apply(lambda x:x.start.nsmallest(2))

    df_pay_1 = df_pay.reset_index()
    # print df_grouped.head(10)
    print df_pay.head()
    def eee(x):
        print x
    usage = df_pay.apply(lambda x: eee(x))
    # repay = df_grouped.apply(lambda x: (x.iloc[0,-1]-x.iloc[1,-1]))
    # print usage.head()
    # print repay.head()
    # pay_repay = pd.DataFrame(data=dict(usage=usage, repay=repay), index=usage.index)
    # pay_repay.to_csv('pay_repay.csv')

def pay_repay_plot():
    df = pd.read_csv('./pay_repay.csv')
    df.set_index('user_id',inplace=True)
    # df =df.sort('usage')
    
    df10 = df[df['usage']==10]
    df15 = df[df['usage']==15]
    df30 = df[df['usage']==30]
    df90 = df[df['usage']==90]
    df180 = df[df['usage']==180]
    df365 = df[df['usage']==365]


    print df10.repay.min()
    # counts, bins = np.histogram(df10.repay.values,bins=48,range=[0,240])
    # result = pd.Series(counts, index=bins[:-1])
    # print df10.repay.value_counts(bins=48)
    fig1 = df10.repay.hist(bins=48)
    fig1.set_xlim([-10,250])
    plt.show()

if __name__ == '__main__':
    day_interval()
    # pay_repay_plot()

