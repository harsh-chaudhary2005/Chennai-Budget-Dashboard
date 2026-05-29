import pandas as pd
df = pd.read_csv('A_corporation_line_items_714rows.csv')
def reclassify_sector(row):
    if row['expenditure_type'] == 'capital_goods':
        return 'infrastructure'
    else:
        return row['sector']
df['simplified_sector'] = df.apply(reclassify_sector, axis=1)

new_summary = df.groupby('simplified_sector')['amount_crore'].sum().reset_index()
print(new_summary.sort_values(by='amount_crore', ascending=False))