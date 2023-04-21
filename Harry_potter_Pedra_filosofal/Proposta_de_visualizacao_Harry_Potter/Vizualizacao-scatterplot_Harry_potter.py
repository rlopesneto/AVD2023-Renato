import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data from your CSV
data = '''
28323   -60.5   4829
20918   -67.0   3658
23949   -85.0   4209
21936   -78.0   3855
41738   -65.0   7107
38303   -57.5   6688
27461   -38.0   4662
19219   -47.0   3300
30873   -90.5   5366
27169   -49.5   4686
20842   -27.5   3606
33041   -55.0   5772
19718   -22.5   3412
21366   -49.0   3737
31097   -106.0  5328
38878   -91.0   6739
33245   -46.5   5766
'''

# Convert data to a pandas DataFrame
data = [row.split() for row in data.strip().split('\n')]
df = pd.DataFrame(data, columns=['Chapter', 'Sentiment', 'WordCount'])

# Convert columns to appropriate data types
df['Chapter'] = df['Chapter'].astype(int)
df['Sentiment'] = df['Sentiment'].astype(float)
df['WordCount'] = df['WordCount'].astype(int)

# Scatterplot with line connecting points
sns.set(style='whitegrid')
plt.figure(figsize=(12, 6))

# Use 'Chapter' as the x-axis, 'Sentiment' as the y-axis, and 'WordCount' to scale the point size
scatter = sns.scatterplot(x='Chapter', y='Sentiment', size='WordCount', data=df, legend=False, alpha=0.7)
sns.lineplot(x='Chapter', y='Sentiment', data=df, alpha=0.6)

# Add labels for each point
for index, row in df.iterrows():
    scatter.text(row['Chapter'] + 1000, row['Sentiment'], f"{index+1}", fontsize=10)

# Customize the plot
plt.title('Sentiment and Word Count by Chapter')
plt.xlabel('Chapter Word Count')
plt.ylabel('Chapter Sentiment')
plt.tight_layout()

# Display the plot
plt.show()
