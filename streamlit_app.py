import pandas as pd
import plotly.express as px
import streamlit as st
from tmdb import TMDb3, TMDb4

st.set_page_config(page_title="ezapi-tmdb-demo", page_icon=":movie_camera:")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg",
        use_column_width=True,
    )
st.title("ezapi-tmdb-demo")
st.caption("A streamlit app to demo ezapi-tmdb")

tmdb3 = TMDb3(st.secrets["api_key"])

st.subheader("Popular Movies")
resp = tmdb3.get_popular_movies(region="US")
st.json(resp, expanded=False)


df = pd.DataFrame(resp["results"])
st.dataframe(df[["title", "release_date", "vote_average"]])


st.subheader("Movies I have watched")

tmdb = TMDb4(st.secrets["access_token"])


@st.cache
def setup():
    request_token = tmdb.create_request_token().get("request_token")

    return request_token


request_token = setup()

st.markdown(
    f"[Approve Access](https://www.themoviedb.org/auth/access?request_token={request_token})"
)

approved = st.checkbox("I have approved it in a new browser window.")

if approved:
    try:
        resp = tmdb.create_access_token(request_token)
        user_access_token = resp.get("access_token")
    except:
        st.error("Access is not granted")
        st.stop()

    list_id = st.number_input("List ID", value=14151)

    @st.cache
    def get_movies(list_id):
        resp = tmdb.get_list(list_id)

        total_results = resp["total_results"]
        average_rating = resp["average_rating"]
        revenue = resp["revenue"]
        runtime = resp["runtime"]
        total_pages = resp["total_pages"]

        df = pd.DataFrame(resp["results"])
        for i in range(2, total_pages + 1):
            resp = tmdb.get_list(list_id, page=i)
            df = pd.concat([df, pd.DataFrame(resp["results"])], ignore_index=True)

        df["release_date"] = pd.to_datetime(df["release_date"])
        df["release_year"] = df["release_date"].dt.year

        return df, total_results, average_rating, revenue, runtime

    df, total_results, average_rating, revenue, runtime = get_movies(list_id)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Items", total_results)
    col2.metric("Average Rating", f"{average_rating:.1f}")
    if revenue > 1_000_000_000:
        revenue = (revenue / 1_000_000_000, "B")
    elif revenue > 1_000_000:
        revenue = (revenue / 1_000_000, "M")
    elif revenue > 1_000:
        revenue = (revenue / 1_000, "K")
    else:
        revenue = revenue, ""
    col3.metric("Total Revenue", f"{revenue[0]:.2f}{revenue[1]}")
    col4.metric("Total Runtime", f"{runtime/60:.0f} Hrs")

    fig = px.histogram(
        df,
        x="original_language",
        color="original_language",
        labels={"original_language": "Original Language"},
    )
    fig

    fig = px.histogram(
        df,
        x="release_year",
        color="release_year",
        labels={"release_year": "Release Year"},
    )
    fig

    fig = px.box(
        df,
        y="vote_average",
        labels={"vote_average": "Vote Average"},
    )
    fig
