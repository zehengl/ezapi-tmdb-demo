import streamlit as st
from tmdb import TMDb3

st.set_page_config(page_title="ezapi-tmdb-demo", page_icon="random")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg",
        use_column_width=True,
    )
st.title("ezapi-tmdb-demo")
st.caption("A streamlit app to demo ezapi-tmdb")

tmdb = TMDb3(st.secrets["api_key"])
