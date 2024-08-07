import streamlit as st
import pickle
import pandas as pd
import requests


# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


# Function to fetch movie details using OMDB API
def fetch_movie_details(movie_title):
    api_key = 'a114014c'  # Replace with your OMDB API key
    base_url = "http://www.omdbapi.com/"
    params = {
        'apikey': api_key,
        't': movie_title
    }
    response = requests.get(base_url, params=params)
    return response.json()


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('Similarity.pkl', 'rb'))

# Streamlit app
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    cols = st.columns(len(recommendations))

    for i, col in enumerate(cols):
        with col:
            movie_details = fetch_movie_details(recommendations[i])
            poster_url = movie_details.get('Poster', 'Poster not found')
            movie_title = recommendations[i]
            movie_genre = movie_details.get('Genre', 'N/A')
            movie_rating = movie_details.get('imdbRating', 'N/A')
            movie_year = movie_details.get('Year', 'N/A')

            # Align movie details vertically
            st.image(poster_url, use_column_width=True)

            # Adjusting spacing between movie title and "About"
            st.markdown(f"**{movie_title}**", unsafe_allow_html=True)
            st.write("")  # Adding an empty line for spacing

            # Add expander for movie details
            with st.expander("About"):
                st.markdown(f"Genre: {movie_genre}")
                st.markdown(f"Rating: {movie_rating} ⭐")
                st.markdown(f"Year: {movie_year}")

# Custom CSS for better alignment
st.markdown("""
    <style>
        .stImage {
            text-align: center;
        }
        .stMarkdown {
            text-align: center;
            margin-top: 0.5rem; /* Adjust top margin for movie title */
        }
        .css-1v3fvcr {
            overflow-x: scroll;
        }
        .css-1v3fvcr .stExpander {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            margin-top: 0.10rem; /* Adjust top margin for "About" expander */
        }

    </style>
""", unsafe_allow_html=True)
