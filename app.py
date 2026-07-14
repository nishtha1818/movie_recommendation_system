import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

print("All libraries installed successfully!")

import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title("🎬 AI Movie Recommendation System")
st.markdown("### Discover movies you'll love using AI!")
st.write("Select a movie below and get 5 similar movie recommendations with their posters.")

st.sidebar.title("About Project")
st.sidebar.write("""
This project uses a Content-Based Movie Recommendation System.
It recommends movies based on similarity between movie features.
Developed using:
- Python
- Pandas
- Streamlit
- Machine Learning
- TMDB API
""")

selected_movie = st.selectbox(
    "Select a Movie",
    movies['title'].values
)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=355127a57e0e760eeac0fd555b5e7625&language=en-US"

        response = requests.get(url, timeout=10)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception:
        return "https://via.placeholder.com/500x750?text=Connection+Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(movies.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters
if st.button("Recommend"):
    st.success("Here are your top 5 movie recommendations!")
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommended_movie_posters[0])
        st.write(recommended_movie_names[0])

    with col2:
        st.image(recommended_movie_posters[1])
        st.write(recommended_movie_names[1])

    with col3:
        st.image(recommended_movie_posters[2])
        st.write(recommended_movie_names[2])

    with col4:
        st.image(recommended_movie_posters[3])
        st.write(recommended_movie_names[3])

    with col5:
        st.image(recommended_movie_posters[4])
        st.write(recommended_movie_names[4])

st.markdown("---")
st.markdown(
    "<center>Developed by <b>Nishtha</b> | B.Tech AI&ML</center>", unsafe_allow_html=True
)


