import pandas as pd
import numpy as np
# from matplotlib import pyplot as plt

def day_interval():
    df = pd.read_csv('./afenti_pay_more_than_2.csv',sep='\t', header=None,
        names= ['pay_status', 'pay_amount', 'pay_method', 'product_service_type', 'total_price', 'school_id',
        'user_id', 'activate_datetime', 'service_start_datetime','service_end_datetime', 'clazz_id', 'region_code'])
    df_paid = df[df['pay_status']=='Paid']

    df_grouped = df_paid.groupby('user_id').head(2).sort('activate_datetime')#.reset_index()
    df_grouped['pay'] = pd.to_datetime(df_grouped['activate_datetime'],format = "%Y-%m-%d")
    df_grouped['start'] = pd.to_datetime(df_grouped['service_start_datetime'],format='%Y-%m-%d')
    df_grouped['end'] = pd.to_datetime(df_grouped['service_end_datetime'],format='%Y-%m-%d')

    usage =  df_grouped.groupby('user_id').apply(lambda x: (x.iloc[0,-1]-x.iloc[0,-2]).days)
    print usage.head()
    repay = df_grouped.groupby('user_id').apply(lambda x: (x.iloc[1,-3]-x.iloc[0,-2]).days)
    print repay.head()
    pay_repay = pd.DataFrame(data=dict(usage=usage, repay=repay), index=usage.index)
    pay_repay.to_csv('pay_repay.csv')

def pay_repay_plot():
    df = pd.read_csv('./pay_repay.csv')
    df.set_index('user_id',inplace=True)
    df =df.sort('usage')
    
    df10 = df[df['usage']==10]
    df15 = df[df['usage']==15]
    df30 = df[df['usage']==30]
    df90 = df[df['usage']==90]
    df180 = df[df['usage']==180]
    df365 = df[df['usage']==365]
    counts, bins = np.histogram(df10.repay_days.values,bins=48,range=[0,240])
    result = pd.Series(counts, index=bins[:-1])
    # print result
    # plt.figure()


    print df10.repay_days.value_counts(bins=40)

    plt.show()

if __name__ == '__main__':
    day_interval()
    # pay_repay_plot()

