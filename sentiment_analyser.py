import pandas as pd

movies_df = pd.read_csv("movies (1).csv")
user_fav_df = pd.read_csv("user_fav.csv")

fav_movies_melted = user_fav_df.melt(id_vars=['username'], 
                                     value_vars=['favmovie1', 'favmovie2', 'favmovie3'],
                                     var_name='fav_order', value_name='movie_id')

merged_df = fav_movies_melted.merge(movies_df, on='movie_id', how='left')

top_genres = merged_df.groupby(['username', 'genre']).size().reset_index(name='count')
top_genres = top_genres.sort_values(['username', 'count'], ascending=[True, False])
top_genre_df = top_genres.drop_duplicates('username')

recommendations = []

for _, row in top_genre_df.iterrows():
    user = row['username']
    genre = row['genre']
    liked_ids = user_fav_df[user_fav_df['username'] == user].iloc[0, 1:].values.tolist()
    recommended = movies_df[(movies_df['genre'] == genre) & (~movies_df['movie_id'].isin(liked_ids))]
    recommended_titles = recommended['name'].tolist()[:5]
    recommendations.append({
        'username': user,
        'top_genre': genre,
        'recommended_movies': recommended_titles
    })

recommendation_df = pd.DataFrame(recommendations)
print(recommendation_df)
