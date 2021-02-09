import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from datetime import datetime
from intro import process


def generate_rules(df):
    df['cat_suicides_num'] = pd.cut(df['num_of_suicides'], bins=6)
    df['cat_suicides/100k'] = pd.cut(df['suicides/100k'], bins=6)
    df['cat_population'] = pd.cut(df['population'], bins=6)
    df['cat_gdp_for_year'] = pd.cut(df['gdp_for_year'], bins=6)
    df['cat_gdp_per_capita'] = pd.cut(df['gdp_per_capita'], bins=6)

    df.drop(['num_of_suicides', 'population', 'suicides/100k', 'gdp_for_year', 'gdp_per_capita'], axis=1, inplace=True)

    # for i in df['continent'].unique():
    #     df_continent = df.loc[df.continent == i]
    #     df_continent = df_continent.drop(['continent'], axis=1)

    # print('start: ', datetime.now().time())
    trans = []
    for y in range(0, df.shape[0]):
        trans.append([str(df.values[y, j]) for j in range(0, df.shape[1])])

    # print('just transformed the dataset into array: ', datetime.now().time())

    te = TransactionEncoder()
    data = te.fit_transform(trans)
    data = pd.DataFrame(data, columns=te.columns_)
    print(data)

    frequent_items = apriori(data, min_support=0.5, use_colnames=True)
    print(frequent_items)

    rules = association_rules(frequent_items, metric="confidence", min_threshold=0.5)
    print(rules)

    # print('finished mining: ', datetime.now().time())
    rules.to_csv('generated_rules.csv')


if __name__ == '__main__':
    suicides = process()
    generate_rules(suicides)