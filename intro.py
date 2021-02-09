import pandas as pd

pd.options.display.float_format = "{:.2f}".format


def read_file():
    master = pd.read_csv('data/master.csv')
    return master


def data_cleaning(master):
    master.rename(columns={
        'suicides_no': 'num_of_suicides',
        'suicides/100k pop': 'suicides/100k',
        'country-year': 'countryYear',
        'HDI for year': 'HDIforYear',
        ' gdp_for_year ($) ': 'gdp_for_year',
        'gdp_per_capita ($)': 'gdp_per_capita',
    }, inplace=True)

    master.drop_duplicates(inplace=True)
    # print(master.isna().sum())
    master.dropna(axis=1, inplace=True)

    # drop useless column - composite key
    master.drop(['countryYear'], axis=1, inplace=True)

    # apply function to age values
    master['age'] = master['age'].apply(lambda x: clear_years(x))

    # make new column in df based on continent
    master['continent'] = master.apply(country_to_continent, axis=1)

    master['gdp_for_year'] = master.gdp_for_year.astype(str)
    master['gdp_for_year'] = master['gdp_for_year'].apply(lambda x: convert_to_float(x))


def clear_years(age):
    return age.split(' ')[0]


def country_to_continent(df):
    africa = ["Cabo Verde", "Mauritius", "Seychelles", "South Africa"]
    asia = ["Armenia", "Azerbaijan", "Bahrain", "Israel", "Japan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Macau",
            "Maldives", "Mongolia", "Oman", "Philippines", "Qatar", "Republic of Korea", "Singapore", "Sri Lanka",
            "Thailand", "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan"]
    australia = ["Australia", "Fiji", "Kiribati", "New Zealand"]
    europe = ["Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
              "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Georgia", "Hungary",
              "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Montenegro", "Netherlands",
              "Norway", "Poland", "Portugal", "Romania", "Russian Federation", "San Marino", "Serbia", "Slovakia",
              "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"]
    north_america = ["Antigua and Barbuda", "Aruba", "Bahamas", "Belize", "Barbados", "Canada", "Costa Rica",
                     "Cuba", "Dominica", "El Salvador", "Grenada", "Guatemala", "Jamaica", "Mexico", "Nicaragua",
                     "Panama", "Puerto Rico", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and Grenadines",
                     "United States"]
    south_america = ["Argentina", "Brazil", "Chile", "Colombia", "Ecuador",
                     "Guyana", "Paraguay", "Suriname", "Trinidad and Tobago", "Uruguay"]

    if df['country'] in africa:
        continent = 'Africa'
    elif df['country'] in asia:
        continent = 'Asia'
    elif df['country'] in australia:
        continent = 'Australia'
    elif df['country'] in europe:
        continent = 'Europe'
    elif df['country'] in north_america:
        continent = 'North America'
    elif df['country'] in south_america:
        continent = 'South America'
    else:
        continent = None
    return continent


def convert_to_float(x):
    x = x.split(',')
    number = ''
    for i in x:
        number += i
    return float(number)


def process():
    df = read_file()
    data_cleaning(df)

    # save modifications in csv file
    # df.to_csv('suicides.csv', index=False)

    return df
