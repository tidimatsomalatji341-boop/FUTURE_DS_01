import matplotlib
matplotlib.use('Agg')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("Superstore.csv",encoding='ISO-8859-1' )


category_data = df.groupby('Category')[['Sales', 'Profit']].sum()

category_data['Profit Margin %'] = (category_data['Profit']/category_data['Sales']) * 100

category_data = category_data.sort_values(by= 'Profit Margin %', ascending=False)

sub_category_losses = df.groupby(['Category', 'Sub-Category'])[['Sales', 'Profit']].sum().sort_values(by= 'Profit', ascending=True).reset_index() 

sub_category_losses['Profit_to_Sales_Ratio'] = sub_category_losses['Profit'] / sub_category_losses['Sales']
sub_category_losses['Margin %'] = (sub_category_losses['Profit_to_Sales_Ratio'] * 100).round(2).astype(str) + '%'


discount_impact = df.groupby('Sub-Category').agg(
    Profit = ('Profit', 'sum'), 
    Sales = ('Sales', 'sum'), 
    Avg_Discount = ('Discount', 'mean')
).reset_index()

discount_impact['Profit_Margin %'] = (discount_impact['Profit'] / discount_impact['Sales'] * 100).round(2)

discount_impact = discount_impact.sort_values(by = 'Avg_Discount', ascending=False)

print("The total Sub-Category Losses")
print(sub_category_losses)

print('\n')

print("Sub-Category Discount Impact Analysis")
print(discount_impact)

print("\n")

print("The Regional Profit Filter")
regional_table_loss = df[df['Sub-Category'] == 'Tables'].groupby('Region')['Profit'].sum()
print(regional_table_loss)

east_table = df[(df['Region'] == 'East') & (df['Sub-Category'] == 'Tables')]

city_losses = east_table.groupby('City')['Profit'].sum()

worst_cities = city_losses.sort_values(ascending=True)

print("\n")
print("The Worst Cities in the East Region")
print(worst_cities)


category_profit = df.groupby('Category')['Profit'].sum().reset_index()

sns.barplot(x = 'Category', y = 'Profit', data=category_profit)
plt.title('Total Profit by Category')

plt.savefig('my_chart.png')
print("Chart saved as my_chart.png!")

plt.clf()

sns.set_theme(style='whitegrid')

plt.figure(figsize=(10,6))
sns.scatterplot(x='Discount', y='Profit', data = df, hue='Category', alpha = 0.5)

sns.regplot(x='Discount', y='Profit', data=df, scatter=False, color='black')

plt.title("How Discount Kill Profitability")
plt.savefig('discount_scatter.png')


regional_data = df.groupby(['Region', 'Category'])['Profit'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='Region', y='Profit', hue = 'Category', data=regional_data)

plt.axhline(0, color = 'black', linestyle = '--', linewidth = 1)

plt.title('Profitability by Region & Category')
plt.savefig('regional_final_report.png')
print('Final regional report saved!')

#top_losses = df.sort_values(by = 'Profit', ascending = False)
#print("Shape (rows, colums):", df.shape)
#print("\nColumn names:", df.columns.tolist())
#print("\nData types:\n", df.dtypes)
#print("\nBasic stats:\n", df.describe())