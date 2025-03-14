import streamlit as st
import pandas as pd
from collections import defaultdict

st.title("📚 Read & Sip Book and Movie Club")
st.markdown(
    """
    <style>
    /* Change background color of the whole app */
    body {
        background-color: #507bc7;  /* Blue background */
    }

    /* Change background color and text color of text input */
    .stTextInput input {
        background-color: pink;
        font-size: 18px;
        color: red;
    }

    /* Optional: Change the background of the sidebar */
    .css-1d391kg {
        background-color: #507bc7;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar for navigation
page = st.sidebar.radio("Go to", ["Submit Book Suggestions", "Submit Movie Suggestions", "Vote on Books", "Vote on Movies", "View Results"])

# Store book suggestions
if "books" not in st.session_state:
    st.session_state.books = []

if "movies" not in st.session_state:
    st.session_state.movies = []

# Page 1: Book Suggestions
if page == "Submit Book Suggestions":
    st.header("📖 Suggest a Book")
    with st.form(key="book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            if title and author:
                st.session_state.books.append(f"{title} by {author}")
                st.success("Book submitted!")
            else:
                st.error("Please enter both title and author.")
# Page 2: Movie Suggestions
elif page == "Submit Movie Suggestions":
    st.header("Suggest a Movie")
    title = st.text_input("Movie Title")
    if st.button("Submit"):
        if title:
            st.session_state.movies.append(title)
            st.success("Movie submitted!")
        else:
            st.error("Please enter a movie title.")
# Page 3: Ranked Choice Voting
elif page == "Vote on Books":
    st.header("Rank Your Favorite Books")
    if not st.session_state.books:
        st.warning("No books submitted yet.")
    else:
        ranked_votes = []
        options = st.session_state.books.copy()
        rank_1 = st.selectbox("1st Choice", options, key="rank1")
        options.remove(rank_1)
        rank_2 = st.selectbox("2nd Choice", options, key="rank2")
        options.remove(rank_2)
        rank_3 = st.selectbox("3rd Choice", options, key="rank3")
        rank_4 = st.selectbox("4th Choice", options, key="rank4")
        rank_5 = st.selectbox("5th Choice", options, key="rank5")
        
        if st.button("Submit Vote"):
            ranked_votes.append([rank_1, rank_2, rank_3, rank_4, rank_5])
            if "bookvotes" not in st.session_state:
                st.session_state.bookvotes = []
            st.session_state.bookvotes.append([rank_1, rank_2, rank_3, rank_4, rank_5])
            st.success("Vote submitted!")
# Page 4: Ranked Choice Voting
elif page == "Vote on Movies":
    st.header("Rank Your Favorite Movies")
    if not st.session_state.movies:
        st.warning("No movies submitted yet.")
    else:
        ranked_votes = []
        options = st.session_state.movies.copy()
        rank_1 = st.selectbox("1st Choice", options, key="rank1")
        options.remove(rank_1)
        rank_2 = st.selectbox("2nd Choice", options, key="rank2")
        options.remove(rank_2)
        rank_3 = st.selectbox("3rd Choice", options, key="rank3")
        rank_4 = st.selectbox("4th Choice", options, key="rank4")
        rank_5 = st.selectbox("5th Choice", options, key="rank5")
        
        if st.button("Submit Vote"):
            ranked_votes.append([rank_1, rank_2, rank_3, rank_4, rank_5])
            if "movievotes" not in st.session_state:
                st.session_state.movievotes = []
            st.session_state.movievotes.append([rank_1, rank_2, rank_3, rank_4, rank_5])
            st.success("Vote submitted!")
# Page 5: View Results
elif page == "View Results":
    st.header("Results")
    if "bookvotes" not in st.session_state or not st.session_state.bookvotes:
        st.warning("No book votes submitted yet.")
    else:
        # Weighted ranking system: 1st choice = 5 points, 2nd choice = 4 points, 3rd choice = 3 points, etc.
        weights = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1}
        scores = defaultdict(int)
        for vote in st.session_state.bookvotes:
            for rank, book in enumerate(vote):
                scores[book] += weights.get(rank, 0)
        
        # Convert results to a DataFrame
        results_df = pd.DataFrame(scores.items(), columns=["Book", "Score"])
        results_df = results_df.sort_values(by="Score", ascending=False)
        
        st.table(results_df)
        
        # Announce the winner
        winner = results_df.iloc[0, 0]
        st.success(f"🏆 The winning book is: ***{winner}***!")
    if "movievotes" not in st.session_state or not st.session_state.movievotes:
            st.warning("No movie votes submitted yet.")
    else:
        # Weighted ranking system: 1st choice = 5 points, 2nd choice = 4 points, 3rd choice = 3 points, etc.
        weights = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1}
        scores = defaultdict(int)
        for vote in st.session_state.movievotes:
            for rank, movie in enumerate(vote):
                scores[movie] += weights.get(rank, 0)
        
        # Convert results to a DataFrame
        results_df = pd.DataFrame(scores.items(), columns=["Movie", "Score"])
        results_df = results_df.sort_values(by="Score", ascending=False)
        
        st.table(results_df)
        
        # Announce the winner
        winner = results_df.iloc[0, 0]
        st.success(f"🏆 The winning movie is: ***{winner}***!")