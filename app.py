

import streamlit as st
import pandas as pd

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Kannada Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------
# 2. MOVIE DATASET
# --------------------------------

movies = [
    {"title": "Kantara", "genres": ["Action", "Drama", "Thriller"], "rating": 8.2, "year": 2022},
    {"title": "KGF Chapter 1", "genres": ["Action", "Crime", "Drama"], "rating": 8.2, "year": 2018},
    {"title": "KGF Chapter 2", "genres": ["Action", "Crime", "Drama"], "rating": 8.3, "year": 2022},
    {"title": "777 Charlie", "genres": ["Adventure", "Comedy", "Drama"], "rating": 8.7, "year": 2022},
    {"title": "Kirik Party", "genres": ["Romance", "Comedy", "Drama"], "rating": 8.0, "year": 2016},
    {"title": "Dia", "genres": ["Romance", "Drama"], "rating": 8.0, "year": 2020},
    {"title": "Mungaru Male", "genres": ["Romance", "Drama"], "rating": 8.3, "year": 2006},
    {"title": "U Turn", "genres": ["Thriller", "Mystery"], "rating": 7.5, "year": 2016},
    {"title": "Lucia", "genres": ["Sci-Fi", "Thriller", "Drama"], "rating": 8.0, "year": 2013},
    {"title": "Avane Srimannarayana", "genres": ["Action", "Adventure", "Comedy"], "rating": 7.8, "year": 2019},
    {"title": "Gaalipata", "genres": ["Romance", "Comedy"], "rating": 7.8, "year": 2008},
    {"title": "Rajakumara", "genres": ["Action", "Drama"], "rating": 7.8, "year": 2017},
    {"title": "Garuda Gamana Vrishabha Vahana", "genres": ["Crime", "Drama", "Thriller"], "rating": 8.2, "year": 2021},
    {"title": "Sapta Sagaradaache Ello", "genres": ["Romance", "Drama"], "rating": 8.2, "year": 2023},
    {"title": "RangiTaranga", "genres": ["Mystery", "Thriller"], "rating": 8.1, "year": 2015}
]

# --------------------------------
# 3. APPLICATION TITLE
# --------------------------------

st.title("🎬 Kannada Movie Recommendation System")

st.write(
    "Discover the best Kannada movies based on your "
    "favourite genres and preferences!"
)

st.divider()

# --------------------------------
# 4. USER PREFERENCES
# --------------------------------

st.subheader("👤 Your Preferences")

name = st.text_input("Enter your name")

all_genres = [
    "Action",
    "Adventure",
    "Romance",
    "Drama",
    "Comedy",
    "Thriller",
    "Crime",
    "Mystery",
    "Sci-Fi"
]

selected_genres = st.multiselect(
    "Select your favourite Kannada movie genres:",
    all_genres
)

min_rating = st.slider(
    "Select minimum movie rating:",
    min_value=5.0,
    max_value=9.0,
    value=7.0,
    step=0.1
)

number = st.slider(
    "How many movies do you want?",
    min_value=1,
    max_value=15,
    value=5
)

# --------------------------------
# 5. RECOMMENDATION ALGORITHM
# --------------------------------

def recommend_movies(preferences, minimum_rating, limit):

    results = []

    if not preferences:
        return results

    user_genres = set(preferences)

    for movie in movies:

        movie_genres = set(movie["genres"])

        # Find common genres
        common = user_genres.intersection(movie_genres)

        # Calculate union
        union = user_genres.union(movie_genres)

        # Calculate Jaccard similarity
        similarity = (len(common) / len(union)) * 100

        # Filter matching movies
        if similarity > 0 and movie["rating"] >= minimum_rating:

            results.append({
                "Movie": movie["title"],
                "Genres": ", ".join(movie["genres"]),
                "Rating": movie["rating"],
                "Year": movie["year"],
                "Similarity Score": round(similarity, 2)
            })

    # Sort by similarity and rating
    results.sort(
        key=lambda x: (
            x["Similarity Score"],
            x["Rating"]
        ),
        reverse=True
    )

    return results[:limit]


# --------------------------------
# 6. GET RECOMMENDATIONS
# --------------------------------

if st.button("✨ Get Kannada Movie Recommendations", type="primary"):

    if not name.strip():

        st.warning("Please enter your name.")

    elif not selected_genres:

        st.warning("Please select at least one genre.")

    else:

        recommendations = recommend_movies(
            selected_genres,
            min_rating,
            number
        )

        st.divider()

        st.subheader(f"Welcome, {name}! 🎉")

        if recommendations:

            st.success(
                f"We found {len(recommendations)} movies for you!"
            )

            # Convert results into DataFrame
            df = pd.DataFrame(recommendations)

            # Display individual movie cards
            st.subheader("🍿 Recommended Kannada Movies")

            for _, movie in df.iterrows():

                with st.container(border=True):

                    st.subheader("🎥 " + movie["Movie"])

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Genre:**", movie["Genres"])
                        st.write("**Release Year:**", int(movie["Year"]))

                    with col2:
                        st.write("**Rating:** ⭐", movie["Rating"])
                        st.write(
                            "**Similarity:**",
                            str(movie["Similarity Score"]) + "%"
                        )

                    st.progress(
                        min(100, int(movie["Similarity Score"])),
                        text="Genre Similarity Score"
                    )

            # Display summary table
            st.divider()

            st.subheader("📊 Recommendation Summary")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No matching movies found. "
                "Try selecting different genres or lowering the rating."
            )

# --------------------------------
# 7. DISPLAY MOVIE COLLECTION
# --------------------------------

st.divider()

with st.expander("🎞️ View All Kannada Movies"):

    movie_df = pd.DataFrame([
        {
            "Movie": movie["title"],
            "Genres": ", ".join(movie["genres"]),
            "Rating": movie["rating"],
            "Year": movie["year"]
        }
        for movie in movies
    ])

    st.dataframe(
        movie_df,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------
# 8. FOOTER
# --------------------------------

st.divider()

st.caption(
    "Kannada Movie Recommendation System | "
    "Python + Streamlit + Pandas | "
    "DecodeLabs AI Project 3"
)
