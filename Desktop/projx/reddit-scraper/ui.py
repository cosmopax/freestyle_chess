import streamlit as st
import pandas as pd
from cosmoscrape import get_reddit_instance, scrape_data

st.set_page_config(page_title="Cosmoscrape", page_icon="🚀", layout="centered")

st.title("🚀 Cosmoscrape")
st.markdown("A web UI for scraping data from any public subreddit.")

try:
    reddit = get_reddit_instance()
    st.sidebar.success("Connected to Reddit API.")
except Exception as e:
    st.sidebar.error(f"Failed to connect to Reddit API. Check `config.ini`.\n\n{e}")
    st.stop()

# --- UI Inputs ---
st.sidebar.header("Scrape Settings")
subreddit_name = st.sidebar.text_input("Subreddit Name (e.g., 'futurology')", "futurology")
post_limit = st.sidebar.slider("Number of Posts to Scrape", 10, 1000, 50)
listing_type = st.sidebar.selectbox("Listing Type", ["Hot", "New", "Top"])

timeframe = None
if listing_type == "Top":
    timeframe = st.sidebar.selectbox(
        "Timeframe for Top Posts",
        ["All", "Year", "Month", "Day"],
        format_func=lambda x: x.capitalize()
    ).lower()

# --- Scraping Execution ---
if st.sidebar.button("Start Scraping"):
    if not subreddit_name:
        st.error("Please enter a subreddit name.")
    else:
        with st.spinner(f"Scraping {post_limit} '{listing_type}' posts from r/{subreddit_name}..."):
            try:
                posts_df, comments_df = scrape_data(
                    reddit,
                    subreddit_name,
                    post_limit,
                    listing_type.lower(),
                    timeframe
                )
                st.success("Scraping Complete!")

                st.header("Results")
                st.write(f"Found {len(posts_df)} posts and {len(comments_df)} comments.")
                
                # Display dataframes and download buttons
                st.subheader("Posts Data")
                st.dataframe(posts_df)
                st.download_button(
                    label="Download Posts CSV",
                    data=posts_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
                    file_name=f"{subreddit_name}_posts.csv",
                    mime='text/csv',
                )

                st.subheader("Comments Data")
                st.dataframe(comments_df)
                st.download_button(
                    label="Download Comments CSV",
                    data=comments_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
                    file_name=f"{subreddit_name}_comments.csv",
                    mime='text/csv',
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

else:
    st.info("Adjust the settings in the sidebar and click 'Start Scraping' to begin.")
