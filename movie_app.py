import streamlit as st;
import pandas as pd;
import pickle
import requests


def fetch_poster(id):
    res = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=46d48c3f66538a122b4c523287daf3fb&language=en-US'.format(id));
    data = res.json()
    return "https://image.tmdb.org/t/p/w185"+data['poster_path']


st.title("Movie Recommendation System")


movies_list = pickle.load(open('movies_dict.pkl','rb'));
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity5.pkl','rb'));
def recommend(movie):
    rec_movies_list = []
    rec_movies_poster = []
    movie_index = movies[movies['title'] == movie ].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x : x[1])[1:6]

    for i in movies_list : 
        rec_movies_list.append(movies.iloc[i[0]].title)
        rec_movies_poster.append(fetch_poster(movies.iloc[i[0]].id))
    return rec_movies_list,rec_movies_poster;


def get_that_movie(movie):
    movie_index = movies[movies['title'] == movie ].index[0]
    movie_id = movies.iloc[movie_index].id
    movie_poster = fetch_poster(movie_id)
    print("movie id : ",movie_id)
    print("movie poster : ",movie_poster)

    return movie_id , movie_poster


selected_movie = st.selectbox(
    "Enter your favourite movie .",
    movies['title'],
    placeholder="enter a movie",
)

if st.button("Recommed"):
    name , poster = recommend(selected_movie);
    mname , mposter = get_that_movie(selected_movie)

    st.markdown(
    f"""
    <div style="display: flex; justify-content: center;margin-bottom:30px ; border-radius:50px">
        <img src="{mposter}" width="300">
    </div>
    """,
    unsafe_allow_html=True
    )


    st.markdown(f"""<div class='small-header' style="margin-bottom:3px">Other recommended movies</div>""", unsafe_allow_html=True)
    col1, col2, col3 , col4 , col5 = st.columns(5)

    with col1:
        st.image(poster[0])
        st.markdown(f"<div class='small-header'>{name[0]}</div>", unsafe_allow_html=True)

    with col2:
        st.image(poster[1])
        st.markdown(f"<div class='small-header'>{name[1]}</div>", unsafe_allow_html=True)

    with col3:
        st.image(poster[2])
        st.markdown(f"<div class='small-header'>{name[2]}</div>", unsafe_allow_html=True)
    
    with col4:
        st.image(poster[3])
        st.markdown(f"<div class='small-header'>{name[3]}</div>", unsafe_allow_html=True)
    
    with col5:
        st.image(poster[4])
        st.markdown(f"<div class='small-header'>{name[4]}</div>", unsafe_allow_html=True)