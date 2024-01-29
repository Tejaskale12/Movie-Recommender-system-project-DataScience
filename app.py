import pickle

import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Image URL
image_url = 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1925&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

# Fetch the image from the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open the image using PIL
    img = Image.open(BytesIO(response.content))

    # Resize the image
    img = img.resize((900, 400))

    # Display the image
    container = st.container()
    with container:
        st.image(img, use_column_width=True)
else:
    st.error(f"Failed to fetch image from URL. Status code: {response.status_code}")


def recommend(movie):
    movie_index = list(movies_list_py['movie_name']).index(movie)
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies_list_py.iloc[i[0]].movie_name)
    return recommended_movies


similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list_py = pickle.load(open('movies.pkl', 'rb'))
duplicate_list_py = pickle.load(open('duplicate.pkl', 'rb'))
movie_list_py = pd.DataFrame(movies_list_py)  # Assuming 'movies_list_py' is a DataFrame

st.title('CENTRAL:red[CINEMA] :clapper:')

option = st.selectbox('SELECT THE MOVIE', list(movies_list_py['movie_name']))

if st.button('Recommend'):
    recommendation = recommend(option)

    for i in recommendation:
        with st.expander(i):
            # Use the correct column name for description
            st.write("Movie Description:")
            st.write(duplicate_list_py[duplicate_list_py['movie_name'] == i]['description'].iloc[0])
            st.write("Movie Genre:")
            st.write(duplicate_list_py[duplicate_list_py['movie_name'] == i]['genre'].iloc[0])
            st.write("Year of Release:")
            st.write(duplicate_list_py[duplicate_list_py['movie_name'] == i]['year'].iloc[0])
