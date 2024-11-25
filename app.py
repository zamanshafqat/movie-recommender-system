import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3e88ccfc733d75a78b489071a613ca85&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movies_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from api
        fetch_poster(movie_id)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Enter Movie",
    movies["title"].values)

if st.button("Recommend"):
    name, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(name[0])
        st.image(posters[0])

    with col2:
        st.header(name[1])
        st.image(posters[1])

    with col3:
        st.header(name[2])
        st.image(posters[2])
    with col4:
        st.header(name[3])
        st.image(posters[3])
    with col5:
        st.header(name[4])
        st.image(posters[4])