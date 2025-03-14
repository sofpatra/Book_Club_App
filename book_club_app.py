import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from collections import defaultdict


# Load credentials from Streamlit secrets
credentials_info = json.loads(st.secrets["GOOGLE_SHEET_CREDENTIALS"])

# Google Sheets authentication
# Google Sheets authentication
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    client = gspread.authorize(creds)
    return client

# Load the Google Sheet
client = connect_to_gsheet()

# Open the spreadsheet by name
spreadsheet = client.open("BookClub")

# Access 'Books' sheet
books_sheet = spreadsheet.worksheet("Books")
# Access 'Movies' sheet
movies_sheet = spreadsheet.worksheet("Movies")

bookvotes_sheet = spreadsheet.worksheet("BookVotes")
movievotes_sheet = spreadsheet.worksheet("MovieVotes")

st.title("📚 Read & Sip Book and Movie Club")
st.markdown(
    """
    <style>
    .stSelectbox > div > div > div {
        background-color: #ffcccc;  /* Light red background */
        color: black;  /* Text color */
    }
        .main {
        background-color: #5dade2;  /* Same or different color */
    }
    /* Change background color and text color of text input */
    .stTextInput input {
        background-color: pink;
        font-size: 18px;
        color: red;
    }
    .stdataframe {
        background-color: lightpink;  /* Background color */
        color: black;  /* Text color */
    }


    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar for navigation
page = st.sidebar.radio("Go to", ["Submit Book Suggestions", "Submit Movie Suggestions", "Vote on Books", "Vote on Movies", "View Results"])

# Page 1: Book Suggestions
if page == "Submit Book Suggestions":
    st.header("📖 Suggest a Book")
    with st.form(key="book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            if title and author:
                # Append to Google Sheet (Books)
                books_sheet.append_row([title, author])
                st.success("Book submitted!")
            else:
                st.error("Please enter both title and author.")
# Page 2: Movie Suggestions
elif page == "Submit Movie Suggestions":
    st.header("Suggest a Movie")
    title = st.text_input("Movie Title")
    if st.button("Submit"):
        if title:
            #Append to Google Sheet (Movies)
            movies_sheet.append_row([title])
            st.success("Movie submitted!")
        else:
            st.error("Please enter a movie title.")
# Page 3: Ranked Choice Voting
elif page == "Vote on Books":
    st.header("Rank Your Favorite Books")
    books = books_sheet.get_all_records()
    if not books:
        st.warning("No books submitted yet.")
    else:
        ranked_votes = []
        options = [book["Book Title"] for book in books] # Assuming the column name is "Book Title"
        rank_1 = st.selectbox("1st Choice", options, key="rank1")
        options.remove(rank_1)
        rank_2 = st.selectbox("2nd Choice", options, key="rank2")

        rank_3 = st.selectbox("3rd Choice", options, key="rank3")

        rank_4 = st.selectbox("4th Choice", options, key="rank4")

        rank_5 = st.selectbox("5th Choice", options, key="rank5")
        
        if st.button("Submit Vote"):
            ranked_votes = [rank_1, rank_2, rank_3, rank_4, rank_5]
            if "bookvotes" not in st.session_state:
                st.session_state.bookvotes = []
            st.session_state.bookvotes.append(ranked_votes)
            #Save to Google Sheet
            bookvotes_sheet.append_row([rank_1, rank_2, rank_3, rank_4, rank_5])
            st.success("Vote submitted!")

# Page 4: Ranked Choice Voting
elif page == "Vote on Movies":
    st.header("Rank Your Favorite Movies")
    movies = movies_sheet.get_all_records()
    if not movies:
        st.warning("No movies submitted yet.")
    else:
        ranked_votes = []
        options = [movie["Movie Title"] for movie in movies] # Assuming the column name is "Movie Title"
        rank_1 = st.selectbox("1st Choice", options, key="rank1")
        options.remove(rank_1)
        rank_2 = st.selectbox("2nd Choice", options, key="rank2")

        rank_3 = st.selectbox("3rd Choice", options, key="rank3")

        rank_4 = st.selectbox("4th Choice", options, key="rank4")

        rank_5 = st.selectbox("5th Choice", options, key="rank5")
        
        if st.button("Submit Vote"):
            movievotes_sheet.append_row([rank_1, rank_2, rank_3, rank_4, rank_5])
            st.success("Vote submitted!")
# Page 5: View Results
elif page == "View Results":
    st.header("Results")
    books = books_sheet.get_all_records()
    book_votes = bookvotes_sheet.get_all_records()

    if not book_votes:
        st.warning("No book votes submitted yet.")
    else:
        # Weighted ranking system: 1st choice = 5 points, 2nd choice = 4 points, 3rd choice = 3 points, etc.
        weights = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1}
        scores = defaultdict(int)
        for vote in book_votes:
            for rank, book in enumerate(vote.values()):
                if book != "NA" and book:
                    scores[book] += weights.get(rank, 0)
        
        # Convert results to a DataFrame
        results_df = pd.DataFrame(scores.items(), columns=["Book", "Score"])
        results_df = results_df.sort_values(by="Score", ascending=False)
        
        st.table(results_df)
        
        # Announce the winner
        winner = results_df.iloc[0, 0]
        st.success(f"🏆 The winning book is: ***{winner}***!")

    # Movie results
    movies = movies_sheet.get_all_records()
    movie_votes = movievotes_sheet.get_all_records()
    if not movie_votes:
        st.warning("No movie votes submitted yet.")
    else:
        # Weighted ranking system: 1st choice = 5 points, 2nd choice = 4 points, 3rd choice = 3 points, etc.
        weights = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1}
        scores = defaultdict(int)
        for vote in movie_votes:
            for rank, movie in enumerate(vote.values()):
                if movie != "NA" and movie:
                    scores[movie] += weights.get(rank, 0)
        
        # Convert results to a DataFrame
        results_df = pd.DataFrame(scores.items(), columns=["Movie", "Score"])
        results_df = results_df.sort_values(by="Score", ascending=False)
        
        st.table(results_df)
        
        # Announce the winner
        winner = results_df.iloc[0, 0]
        st.success(f"🏆 The winning movie is: ***{winner}***!")
