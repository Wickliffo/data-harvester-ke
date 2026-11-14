import streamlit as st
import pandas as pd
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
properties_path = os.path.join(current_dir, '../../properties.json')
ecommerce_path = os.path.join(current_dir, '../../ecommerce.json')
reddit_path = os.path.join(current_dir, '../../reddit_interests.json')

@st.cache_data
def load_properties():
    with open(properties_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['price_numeric'] = (
        df['price']
        .str.replace('KSh', '', regex=False)
        .str.replace(' ', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(int)
    )
    df['category'] = 'Property'
    df['location'] = df['location'].fillna('')
    df['address'] = df['address'].fillna('')
    df['description'] = df['description'].fillna('')
    df['url'] = df['url'].fillna('')
    return df

@st.cache_data
def load_ecommerce():
    with open(ecommerce_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['price_numeric'] = (
        df['price']
        .str.replace('KSh', '', regex=False)
        .str.replace(' ', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(int)
    )
    df['category'] = 'E-commerce'
    df['location'] = ''
    df['address'] = ''
    df['description'] = ''
    df['url'] = df['url'].fillna('')
    return df

@st.cache_data
def load_reddit():
    with open(reddit_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    # Safely find a voting/score column if 'upvotes' doesn't exist
    vote_col = None
    for col in ['upvotes', 'score', 'votes', 'likes']:
        if col in df.columns:
            vote_col = col
            break
            
    if vote_col:
        df['tweet_count_numeric'] = df[vote_col].apply(lambda x: int(x) if pd.notnull(x) and str(x).isdigit() else 0)
        df['upvotes'] = df[vote_col] # normalize column name for display
    else:
        df['tweet_count_numeric'] = 0
        df['upvotes'] = 0

    df['category'] = 'Social Media'
    df['location'] = ''
    df['address'] = ''
    df['description'] = ''
    df['price'] = ''
    df['price_numeric'] = 0
    df['url'] = df['url'].fillna('') if 'url' in df.columns else ''
    return df

def make_clickable(url, category):
    if url:
        if not url.startswith('http'):
            if category == 'E-commerce':
                url = 'https://www.jumia.co.ke' + url
            elif category == 'Property':
                url = 'https://www.property24.co.ke' + url
        return f'[Link]({url})'
    else:
        return ''

def create_download_link(df, filename):
    return st.download_button(
        label=f"Download {filename} as CSV",
        data=df.to_csv(index=False),
        file_name=filename,
        mime='text/csv'
    )

st.title("Kenyan Market Data Explorer")

properties_df = load_properties()
ecommerce_df = load_ecommerce()
reddit_df = load_reddit()

# Determine price range to set slider with all prices considered
all_prices = pd.concat([
    properties_df['price_numeric'],
    ecommerce_df['price_numeric']
], ignore_index=True)
min_price = int(all_prices.min())
max_price = int(all_prices.max())

category_filter = st.sidebar.multiselect(
    "Filter by Category", options=['Property', 'E-commerce', 'Social Media'], default=['Property']
)

min_slider, max_slider = st.sidebar.slider(
    "Price Range (KSh) (applies to Property & E-commerce)",
    min_price,
    max_price,
    (min_price, max_price)
)

def filter_dataframe(df, min_p, max_p):
    if 'price_numeric' in df.columns and df['price_numeric'].sum() > 0:
        return df[(df['price_numeric'] >= min_p) & (df['price_numeric'] <= max_p)]
    else:
        return df

if len(category_filter) == 1:
    category = category_filter[0]

    if category == 'Property':
        df = filter_dataframe(properties_df, min_slider, max_slider)
        df_display = df.copy()
        df_display['URL'] = df.apply(lambda row: make_clickable(row['url'], 'Property'), axis=1)
        st.subheader("Properties")
        st.dataframe(df_display[['title', 'price', 'location', 'address', 'description', 'URL']])
        create_download_link(df_display, "properties.csv")

    elif category == 'E-commerce':
        df = filter_dataframe(ecommerce_df, min_slider, max_slider)
        df_display = df.copy()
        df_display['URL'] = df.apply(lambda row: make_clickable(row['url'], 'E-commerce'), axis=1)
        st.subheader("E-commerce Products")
        st.dataframe(df_display[['title', 'price', 'URL']])
        create_download_link(df_display, "ecommerce.csv")

    else:  # Social Media
        df = reddit_df.copy()
        df_display = df.copy()
        df_display['URL'] = df_display['url'].apply(lambda x: make_clickable(x, 'Social Media') if x else '')
        st.subheader("Social Media Interests")
        cols_to_show = [c for c in ['title', 'upvotes', 'URL'] if c in df_display.columns]
        st.dataframe(df_display[cols_to_show])
        create_download_link(df_display, "social_media_interests.csv")

else:
    if 'Property' in category_filter:
        df_prop = filter_dataframe(properties_df, min_slider, max_slider)
        df_prop_display = df_prop.copy()
        df_prop_display['URL'] = df_prop.apply(lambda row: make_clickable(row['url'], 'Property'), axis=1)
        st.subheader("Properties")
        st.dataframe(df_prop_display[['title', 'price', 'location', 'address', 'description', 'URL']])
        create_download_link(df_prop_display, "properties.csv")

    if 'E-commerce' in category_filter:
        st.write("---")
        df_ecomm = filter_dataframe(ecommerce_df, min_slider, max_slider)
        df_ecomm_display = df_ecomm.copy()
        df_ecomm_display['URL'] = df_ecomm.apply(lambda row: make_clickable(row['url'], 'E-commerce'), axis=1)
        st.subheader("E-commerce Products")
        st.dataframe(df_ecomm_display[['title', 'price', 'URL']])
        create_download_link(df_ecomm_display, "ecommerce.csv")

    if 'Social Media' in category_filter:
        st.write("---")
        df_sm = reddit_df.copy()
        df_sm_display = df_sm.copy()
        df_sm_display['URL'] = df_sm_display['url'].apply(lambda x: make_clickable(x, 'Social Media') if x else '')
        st.subheader("Social Media Interests")
        cols_to_show = [c for c in ['title', 'upvotes', 'URL'] if c in df_sm_display.columns]
        st.dataframe(df_sm_display[cols_to_show])
        create_download_link(df_sm_display, "social_media_interests.csv")