def report_csv(clean_df,country='all'):
    if country=='all':
        clean_df.to_csv('data/results.csv', index=False)
        print('All countries reported. File created: data/results.csv')
    else:
        country=country.capitalize()
        if country in list(clean_df['Country'].values):
            clean_df[clean_df['Country']==country].to_csv(f'data/{country}_results.csv', index=False)
            print(f'File created: data/{country}_results.csv')
        else:
            raise ValueError(f"Input Country is not in database \n"
                             f" List of countries included in database: \n"
                             f"{clean_df['Country'].unique()}")
    return

def report_csv_bonus(result,bonus):
    result.to_csv(f'data/bonus{bonus}.csv')
    print(f'File created: data/bonus{bonus}.csv')