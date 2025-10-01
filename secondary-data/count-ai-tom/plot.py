import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read the CSV file
df = pd.read_csv('gscholar.csv')

# extract years and counts
years = df['year'].tolist()
counts = df['count'].tolist()

print("Publication counts by year:")
for year, count in zip(years, counts):
    print(f"Year: {year}, Count: {count}")

# abbreviate year labels
year_labels = [f"'{str(y)[-2:]}" for y in years]

# make a pretty plot
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (8, 5)
fig, ax = plt.subplots()
ax.bar(years, counts, color='#bf5700')
ax.set_xticks(years)
ax.set_xticklabels(year_labels, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
sns.despine()
plt.tight_layout()
plt.show()