import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample demographics data
data = {
    'Age': ['23 - 27', '28 - 32', '23 - 27', '23 - 27', '23 - 27', '28 - 32', '23 - 27', '18 - 22', '18 - 22', '18 - 22'],
    'Gender': ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male', 'Male'],
    'Experience with collaborative tools': ['Some', 'Some', 'None', 'Some', 'Some', 'None', 'Extensive', 'None', 'Some', 'Some'],
    'Background': ['Graduate Student', 'Graduate Student', 'Graduate Student', 'Graduate Student', 'Graduate Student', 'Graduate Student', 'Undergraduate Student', 'Undergraduate Student', 'Undergraduate Student', 'Undergraduate Student']
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate counts for each demographic category
age_counts = df['Age'].value_counts()
gender_counts = df['Gender'].value_counts()
experience_counts = df['Experience with collaborative tools'].value_counts()
background_counts = df['Background'].value_counts()

# Set up the matplotlib figure and axes
fig, ax = plt.subplots(figsize=(12, 8))

# Plotting the grouped bar chart
age_counts.plot(kind='bar', color='skyblue', position=0, width=0.2, label='Age', ax=ax)
gender_counts.plot(kind='bar', color='salmon', position=1, width=0.2, label='Gender', ax=ax)
experience_counts.plot(kind='bar', color='lightgreen', position=2, width=0.2, label='Experience', ax=ax)
background_counts.plot(kind='bar', color='orange', position=3, width=0.2, label='Background', ax=ax)

# Adding labels and title
ax.set_xlabel('Categories')
ax.set_ylabel('Count')
ax.set_title('Demographic Distribution')
ax.legend()

# Show the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
