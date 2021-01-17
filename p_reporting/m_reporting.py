def report_csv(clean_df,country='all'):
    if country=='all':
        clean_df.to_csv('data/results.csv')
    else:
        country=format_choice.capitalize()
        if country in clean.df['Country'].values():
            clean_df[clean.df['Country']==country].to_csv(f'data/{country} results.csv')
        else:
            raise ValueError("Input is not in database")
    return