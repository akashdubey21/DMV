import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Retail_Sales_Data.csv')

print(df.head())
print(df.info())
print(df.describe())
print(df.columns)

sales_by_region = df.groupby('Store Location')['Sales Revenue (USD)'].sum().reset_index()

plt.figure(figsize=(10, 35))
sns.barplot(x='Sales Revenue (USD)', y='Store Location', data=sales_by_region, palette='viridis')
plt.title('Sales Distribution by Store Location')
plt.xlabel('Total Sales Revenue (USD)')
plt.ylabel('Store Location')
plt.legend(['Sales Revenue'])
plt.show()

sales_by_region_category = df.groupby(['Store Location', 'Product Category'])['Sales Revenue (USD)'].sum().unstack().fillna(0)

sales_by_region_category.plot(kind='bar', stacked=True, figsize=(12, 7), colormap='Set3')
plt.title('Sales Revenue by Store Location and Product Category')
plt.xlabel('Store Location')
plt.ylabel('Total Sales Revenue (USD)')
plt.legend(title='Product Category')
plt.xticks(rotation=45)
plt.show()
