import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity= pickle.load(open('similarity.pkl', 'rb'))

def fetch(movie_id):
    response =requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b259f758e1519709839e1374e4814cc4'.format(movie_id))
    data=response.json()

    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances= similarity[movie_index]
    recommended_movies=[]
    recommended_posters=[]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch(movie_id))
    return recommended_movies, recommended_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a Movie',
    movies['title'].values
)

if st.button('Recommend'):
    name, poster= recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])