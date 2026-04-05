from __future__ import annotations

import streamlit as st

from movie_recommender import build_recommender, resolve_dataset_path

st.set_page_config(
    page_title="Movie Matchmaker",
    page_icon="🎬",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Fraunces:opsz,wght@9..144,700&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 12% 18%, rgba(255, 206, 122, 0.30), transparent 28%),
            radial-gradient(circle at 88% 82%, rgba(100, 190, 255, 0.22), transparent 30%),
            linear-gradient(160deg, #0f172a 0%, #1e293b 55%, #111827 100%);
        color: #f8fafc;
        font-family: "Space Grotesk", sans-serif;
    }

    h1, h2, h3 {
        font-family: "Fraunces", serif !important;
        letter-spacing: 0.2px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie Matchmaker")
st.caption("Type a movie title and get close-content recommendations using TF-IDF + cosine similarity.")

@st.cache_resource(show_spinner=False)
def load_recommender():
    dataset_path = resolve_dataset_path()
    return build_recommender(dataset_path)


try:
    with st.spinner("Building recommendation engine..."):
        recommender = load_recommender()
except Exception as exc:
    st.error(f"Could not initialize the recommendation engine: {exc}")
    st.stop()

movie_input = st.text_input("Movie name", placeholder="Example: Avatar")
top_n = st.slider("How many recommendations?", min_value=5, max_value=20, value=10, step=1)
recommend_clicked = st.button("Recommend Movies", use_container_width=True)

if recommend_clicked:
    try:
        matched_title, recommendations = recommender.recommend_movies(movie_input, top_n=top_n)
        st.success(f"Closest match found: **{matched_title}**")

        if not recommendations:
            st.warning("No recommendations could be generated for this movie.")
        else:
            st.subheader("🍿 Recommended Movies")
            for idx, item in enumerate(recommendations, start=1):
                st.write(f"{idx}. **{item['title']}**  | similarity: `{item['score']:.4f}`")
    except ValueError as exc:
        st.warning(str(exc))
    except Exception as exc:  # pragma: no cover
        st.error(f"Unexpected error: {exc}")
