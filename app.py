import pickle
import requests
import streamlit as st

# Function to fetch movie poster given a movie ID
def fetch_poster(movie_id):
    # Construct the API URL using the movie ID
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    # Make a GET request to the API and get the JSON response
    data = requests.get(url).json()
    # Extract the poster path from the JSON response
    poster_path = data['poster_path']
    # Construct the full poster URL using the poster path
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to recommend movies given a movie title
def recommend(movie):
    # Get the index of the movie from the movies DataFrame
    index = movies[movies['title'] == movie].index[0]
    # Get the similarity scores of all movies with the selected movie and sort them in descending order
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    # Initialize empty lists to store recommended movie names and posters
    recommended_movie_names = []
    recommended_movie_posters = []
    # Loop through the similarity scores and get the movie ID, poster URL and name of the top 6 similar movies
    for i in distances[0:6]:
        # Get the movie ID of the similar movie
        movie_id = movies.iloc[i[0]].movie_id
        # Fetch the poster URL of the similar movie using the fetch_poster function
        recommended_movie_posters.append(fetch_poster(movie_id))
        # Get the name of the similar movie
        recommended_movie_names.append(movies.iloc[i[0]].title)
    # Return the recommended movie names and posters as a tuple
    return recommended_movie_names, recommended_movie_posters

# Set page title and main title
st.set_page_config(page_title='Movie Recommender System')
st.title('Movie Recommender System')

# Load the movies DataFrame and similarity matrix using pickle
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Get the list of movie titles from the movies DataFrame
movie_list = movies['title'].values

# Create a dropdown menu for selecting a movie from the list
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Create a button to show the recommended movies
if st.button('Show Recommendations'):
    # Call the recommend function to get the recommended movie names and posters
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    # Create 5 columns to display the recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)
    # Display the recommended movies in each column
    with col1:
        st.image(recommended_movie_posters[0], use_column_width=True)
        st.write(recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1], use_column_width=True)
        st.write(recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2], use_column_width=True)
        st.write(recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3], use_column_width=True)
        st.write(recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4], use_column_width=True)
        st.write(recommended_movie_names[4])
