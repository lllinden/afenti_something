import pandas as pd
from matplotlib import pyplot as plt


    
def day_interval():
    df = pd.read_csv('./afenti_pay_2.csv',sep='\t', header=None,
        names= ['pay_status', 'pay_amount', 'pay_method', 'product_service_type', 'total_price', 'school_id',
        'user_id', 'service_start_datetime', 'service_end_datetime', 'clazz_id', 'region_code'])
    df_paid = df[df['pay_status']=='Paid']

    df_grouped = df_paid.groupby('user_id').head(2).sort('service_start_datetime')#.reset_index()
    df_grouped['start'] = pd.to_datetime(df_grouped['service_start_datetime'],format='%Y-%m-%d')
    df_grouped['end'] = pd.to_datetime(df_grouped['service_end_datetime'],format='%Y-%m-%d')

    pay_days =  df_grouped.groupby('user_id').apply(lambda x: (x.iloc[0,-1]-x.iloc[0,-2]).days)
    repay_days = df_grouped.groupby('user_id').apply(lambda x: (x.iloc[1,-2]-x.iloc[0,-2]).days)

    pay_repay = pd.DataFrame(data=dict(pay_days=pay_days, repay_days=repay_days), index=pay_days.index)
    pay_repay.to_csv('pay_repay.csv')


def pay_repay_plot():
    df = pd.read_csv('./pay_repay.csv')
    df.set_index('user_id',inplace=True)
    df =df.sort('pay_days')
    df10 = df[df['pay_days']==10]
    print df.pay_days.unique()
    f, axarr = plt.subplots(2, 2)



if __name__ == '__main__':
    # day_interval()
    pay_repay_plot()

