import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import matplotlib.ticker as ticker

# ----------------------------
# 0. Load and clean data
# ----------------------------
df = pd.read_csv("NetFlix.csv")  # Load data

# Define required columns and remove rows with missing values
required_columns = ['type', 'country', 'date_added', 'release_year', 'rating', 'duration', 'genres']
df = df.dropna(subset=[col for col in required_columns if col in df.columns])

# ----------------------------
# 1. Professional Histogram
# ----------------------------
movies = df[df['type'] == 'Movie'].copy()
movies['duration'] = movies['duration'].astype(str)
movies['duration_minutes'] = movies['duration'].str.extract(r'(\d+)').astype(float)

# Plot histogram with KDE (Kernel Density Estimate)
plt.figure(figsize=(12, 6))
sns.histplot(
    data=movies,
    x='duration_minutes',
    bins=25,
    kde=True,
    color='#E50914', 
    edgecolor='black',
    linewidth=0.5
)

# Customize plot appearance
plt.title("Distribution de la durée des films sur Netflix", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Durée (en minutes)", fontsize=13)
plt.ylabel("Nombre de films", fontsize=13)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Adjust x-axis ticks and remove top/right borders
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(20))
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Show the plot
plt.tight_layout()
plt.show()

# ----------------------------
# 2. Professional Sunburst Chart with Percentages
# ----------------------------
df['genres'] = df['genres'].astype(str).str.split(', ')
df_exploded = df.explode('genres')

# Create the sunburst chart
fig = px.sunburst(
    df_exploded,
    path=['type', 'genres'],
    color='type',
    color_discrete_map={
        'Movie': '#E50914', 
        'TV Show': '#221f1f' 
    },
    title="Répartition des contenus Netflix par type et genre",
    width=750,
    height=750,
)

# Customize chart with percentage labels and hover text
fig.update_traces(
    insidetextorientation='radial',
    hovertemplate='<b>%{label}</b><br>Nombre: %{value}<br>Pourcentage: %{percent}<extra></extra>',
    textinfo="label+percent entry",  
    textfont_size=12,  
)

# Improve layout aesthetics and add title formatting
fig.update_layout(
    title_font_size=20,
    title_font_family="Arial",
    margin=dict(t=60, l=0, r=0, b=0),
    uniformtext=dict(minsize=10, mode='hide'),
    paper_bgcolor="white",
    font=dict(color="black"),
    title_x=0.5, 
    title_y=0.97,  
)

# Show the sunburst chart
fig.show()
