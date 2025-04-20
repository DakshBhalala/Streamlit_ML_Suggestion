import ast
import json
import streamlit as st
import pandas as pd

# --- Custom Styles ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body {
    background-color: #0e1117;
    color: #E0E0E0;
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    color: #00BFFF;
    text-align: center;
    font-weight: 700;
    letter-spacing: 0.7px;
}

h4 {
    color: #AAAAAA;
    text-align: center;
    font-weight: 300;
    font-size: 1.1rem;
    margin-top: -0.5rem;
}

hr {
    border: none;
    border-top: 1px solid #333;
    margin: 2rem auto;
    width: 80%;
}

.centered-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 1rem;
    max-width: 800px;
    margin: auto;
}

.stTextInput, .stSelectbox {
    width: 100% !important;
    max-width: 600px;
    margin: 0 auto;
}

.st-bx {
    width: 100%;
    max-width: 800px;
    background: rgba(255, 255, 255, 0.03);
    border-left: 4px solid #00BFFF;
    border-radius: 18px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 30px rgba(0, 191, 255, 0.08);
    backdrop-filter: blur(4px);
    transition: all 0.3s ease;
}

.st-bx:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(0, 191, 255, 0.2);
}

.emoji {
    font-size: 1.4rem;
    color: #00FFAB;
    font-weight: bold;
}

.tag {
    display: inline-block;
    background-color: #00BFFF;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.75rem;
    margin: 0.25rem 0.3rem 0 0;
}

footer {
    text-align: center;
    color: #777;
    padding: 2.5rem 0 1.2rem;
    font-size: 0.85rem;
    opacity: 0.75;
}

.stButton>button {
    background: linear-gradient(145deg, #1e90ff, #00bfff);
    color: white;
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    font-weight: bold;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(30, 144, 255, 0.3);
    border: none;
    transition: 0.3s ease-in-out;
}

.stButton>button:hover {
    background: linear-gradient(145deg, #00bfff, #1e90ff);
    transform: scale(1.05);
}

/* Fix for details and "Read More" functionality */
details {
    background-color: rgba(255, 255, 255, 0.02);
    padding: 0.6rem 1rem;
    margin-top: 0.8rem;
    border-radius: 10px;
    color: #ccc;
    font-size: 0.95rem;
    overflow-wrap: break-word;
}

details summary {
    cursor: pointer;
    font-weight: bold;
    color: #00BFFF;
    outline: none;
    margin-bottom: 0.4rem;
}

details[open] summary {
    margin-bottom: 0.5rem;
}

details p {
    margin: 0;
    line-height: 1.5;
}

details {
    max-height: 250px;
    overflow-y: auto;
}

details {
    transition: all 0.3s ease-in-out;
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Title ---
st.markdown("<h1>🎯 Content-Based Recommendation System</h1>", unsafe_allow_html=True)
st.markdown(
    "<h4>Find Movies, Music, Anime & Games tailored to your taste!</h4><hr>",
    unsafe_allow_html=True,
)


# --- Load Data ---
@st.cache_data
def load_data(name):
    return pd.read_csv(f"data/{name}.csv")


@st.cache_data
def load_similarities(name):
    with open(f"data/top_{name}_similarities.json", "r") as f:
        return json.load(f)


# --- Utilities ---
def display_tags(tag_str):
    tags = tag_str.split(",") if isinstance(tag_str, str) else []
    return " ".join([f"<span class='tag'>{t.strip()}</span>" for t in tags])


def get_recommendations(title, df, sim_dict, col_mapping):
    if title not in sim_dict:
        return []
    indices = sim_dict[title]
    recs = []
    for i in indices:
        item = {}
        for key, value in col_mapping.items():
            item[key] = df.iloc[i].get(value, "N/A")
        recs.append(item)
    return recs


# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["🎬 Movies", "🎵 Music", "📺 Anime", "🎮 Games"])

# --- Movies Tab ---
with tab1:
    movie_df = load_data("movies")
    movie_sim = load_similarities("movie")
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    movie_title = st.text_input("Enter a Movie Title", key="movie")
    st.markdown("</div>", unsafe_allow_html=True)
    if movie_title:
        with st.spinner("Finding similar movies..."):
            results = get_recommendations(
                movie_title, movie_df, movie_sim, {"title": "title", "genres": "genres"}
            )
        if results:
            st.success("Recommended Movies:")
            for rec in results:
                st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class='st-bx'>
                        <h3 class='emoji'>🎥 {rec["title"]}</h3>
                        <p><strong>Genres:</strong><br> {display_tags(rec["genres"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No recommendations found for that title.")

# --- Music Tab ---
with tab2:
    music_df = load_data("music")
    music_sim = load_similarities("music")
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    music_title = st.text_input("Enter a Song Title", key="music")
    st.markdown("</div>", unsafe_allow_html=True)
    if music_title:
        with st.spinner("Finding similar tracks..."):
            results = []
            if music_title in music_sim:
                for i in music_sim[music_title]:
                    raw_artists = music_df.iloc[i]["artists"]
                    try:
                        artists = ", ".join(ast.literal_eval(raw_artists))
                    except:
                        artists = str(raw_artists)
                    results.append(
                        {
                            "name": music_df.iloc[i]["name"],
                            "artist": artists,
                            "mood": music_df.iloc[i]["Mood"],
                            "release": music_df.iloc[i]["release_date"],
                        }
                    )
        if results:
            st.success(f"Similar Tracks to '{music_title}':")
            for rec in results:
                st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class='st-bx'>
                        <h3 class='emoji'>🎧 {rec["name"]}</h3>
                        <p><strong>Artist:</strong> {rec["artist"]}<br>
                        <strong>Mood:</strong><br> {display_tags(rec["mood"])}<br>
                        <strong>Release Date:</strong> {rec["release"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No recommendations found.")

# --- Anime Tab ---
with tab3:
    anime_df = load_data("anime")
    anime_sim = load_similarities("anime")
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    anime_title = st.text_input("Enter an Anime Title", key="anime")
    st.markdown("</div>", unsafe_allow_html=True)
    if anime_title:
        with st.spinner("Searching for anime..."):
            results = get_recommendations(
                anime_title,
                anime_df,
                anime_sim,
                {
                    "name": "name",
                    "genre": "genre",
                    "episodes": "episodes",
                    "rating": "rating",
                    "type": "type",
                },
            )
        if results:
            st.success("Recommended Anime:")
            for rec in results:
                st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class='st-bx'>
                        <h3 class='emoji'>📺 {rec["name"]}</h3>
                        <p><strong>Genre:</strong><br> {display_tags(rec["genre"])}<br>
                        <strong>Episodes:</strong> {rec["episodes"]}<br>
                        <strong>Rating:</strong> {rec["rating"]}<br>
                        <strong>Type:</strong> {rec["type"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No similar anime found.")

# --- Games Tab ---
with tab4:
    game_df = load_data("games")
    game_sim = load_similarities("game")
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    game_title = st.text_input("Enter a Game Title", key="game")
    st.markdown("</div>", unsafe_allow_html=True)
    if game_title:
        with st.spinner("Fetching game recommendations..."):
            results = get_recommendations(
                game_title,
                game_df,
                game_sim,
                {
                    "name": "Name",
                    "genres": "Genres",
                    "release_date": "Release date",
                    "description": "About the game",
                },
            )
        if results:
            st.success("Games you might enjoy:")
            for rec in results:
                st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class='st-bx'>
                        <h3 class='emoji'>🕹️ {rec["name"]}</h3>
                        <p><strong>Genres:</strong><br> {display_tags(rec["genres"])}<br>
                        <strong>Release Date:</strong> {rec["release_date"]}<br>
                        <strong>Description:</strong></p>
                        <details>
                            <summary>Read more</summary>
                            <p>{rec["description"] or "No description available"}</p>
                        </details>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No game recommendations found.")

# --- Footer ---
st.markdown(
    """
<footer>
    🔮 Made with <span style="color:#FF69B4;">❤️</span> using Streamlit
</footer>
""",
    unsafe_allow_html=True,
)
