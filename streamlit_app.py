#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Scorecared Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
df_reshaped = pd.read_csv('data/scores.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('Selection Scorescard')
    cat_list = list(df_reshaped.category.unique())[::-1]
    
    selected_category = st.selectbox('Select a Category', cat_list)
    df_selected_category = df_reshaped[df_reshaped.category == selected_category]
    df_selected_category_sorted = df_selected_category.sort_values(by="priority", ascending=False)
    st.markdown('list out the subs here.')
    st.markdown(list(df_reshaped.subcategory))
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
#######################
# Plots


#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Gains/Losses')

    st.markdown('#### States Migration')


with col[1]:
    st.markdown('#### Total Population')

    

with col[2]:
    st.markdown('#### Top States')

    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')
