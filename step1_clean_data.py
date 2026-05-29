import pandas as pd


df = pd.read_csv('A_corporation_line_items_714rows.csv')


def reclassify_sector(row):
    if row['expenditure_type'] == 'capital_goods':
        return 'infrastructure'
    else:
        return row['sector']

df['simplified_sector'] = df.apply(reclassify_sector, axis=1)


df.to_csv('A_corporation_line_items_reclassified.csv', index=False)
print("Success: A_corporation_line_items_reclassified.csv has been created!")