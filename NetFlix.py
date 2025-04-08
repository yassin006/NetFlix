import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# 1. Charger les données
df = pd.read_csv("C:/Users/MSI/zz/NetFlix.csv/NetFlix.csv")

# 2. Vérifier les colonnes disponibles
print("Aperçu des données :")
print(df.head())
print("\nColonnes :", df.columns)

# 3. Nettoyage de base
required_columns = ['type', 'country', 'date_added', 'release_year', 'rating', 'duration', 'genres']
df = df.dropna(subset=[col for col in required_columns if col in df.columns])

# 4. Répartition des types
plt.figure(figsize=(6, 4))
sns.countplot(x='type', data=df, hue='type', palette='Set2', legend=False)
plt.title("Répartition des types (Movie vs TV Show)")
plt.xlabel("Type")
plt.ylabel("Nombre")
plt.tight_layout()
plt.show()

# 5. Top 10 des pays
top_countries = df['country'].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, dodge=False, palette='Set3', legend=False)
plt.title("Top 10 des pays avec le plus de titres sur Netflix")
plt.xlabel("Nombre de titres")
plt.ylabel("Pays")
plt.tight_layout()
plt.show()

# 6. Nombre de sorties par année
plt.figure(figsize=(10, 5))
sns.histplot(df['release_year'], bins=30, kde=False, color='skyblue')
plt.title("Nombre de titres sortis par année")
plt.xlabel("Année de sortie")
plt.ylabel("Nombre de titres")
plt.tight_layout()
plt.show()

# 7. Répartition des notes (ratings)
plt.figure(figsize=(8, 4))
sns.countplot(y='rating', data=df, order=df['rating'].value_counts().index, hue='rating', palette='cool', legend=False)
plt.title("Répartition des classifications (ratings)")
plt.xlabel("Nombre")
plt.ylabel("Classification")
plt.tight_layout()
plt.show()

# 8. Durée moyenne des films (minutes)
movies = df[df['type'] == 'Movie'].copy()
movies['duration'] = movies['duration'].astype(str)
movies['duration_minutes'] = movies['duration'].str.extract(r'(\d+)').astype(float)

plt.figure(figsize=(8, 4))
sns.histplot(movies['duration_minutes'], bins=30, kde=True, color='salmon')
plt.title("Durée des films sur Netflix")
plt.xlabel("Durée (minutes)")
plt.ylabel("Nombre de films")
plt.tight_layout()
plt.show()

# 9. Graphe en arborescence Type → Genre
df['genres'] = df['genres'].astype(str).str.split(', ')
df_exploded = df.explode('genres')

fig = px.sunburst(
    df_exploded,
    path=['type', 'genres'],
    color='type',
    color_discrete_map={'Movie': 'lightblue', 'TV Show': 'lightgreen'},
    title="Arborescence des contenus Netflix : Type → Genre"
)
fig.show()

# 10. Prep diagramme Type → Genre
genre_flow = df_exploded.groupby(['type', 'genres']).size().reset_index(name='count')
node_labels = ['Movie', 'TV Show'] + list(genre_flow['genres'].unique())
node_ids = {label: idx for idx, label in enumerate(node_labels)}
links = []
for _, row in genre_flow.iterrows():
    type_idx = node_ids[row['type']]
    genre_idx = node_ids[row['genres']]
    links.append({'source': type_idx, 'target': genre_idx, 'value': row['count']})

fig_flow = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=node_labels,
        color=["lightblue", "lightgreen"] + ['#FFA07A' for _ in range(len(node_labels) - 2)]
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links],
        color='rgba(255, 99, 132, 0.6)'
    )
))

fig_flow.update_layout(title="Diagramme: Type → Genre")
fig_flow.show()
