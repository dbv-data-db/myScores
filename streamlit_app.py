#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import math
import numpy as np

#######################
# Page configuration
st.set_page_config(
    page_title="Scorecard Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
df_reshaped = pd.read_csv('data/scores.csv')
scoredata = pd.read_csv('data/scores.csv')
weightdata = pd.read_csv('data/weight.csv')
categorydata = pd.read_csv('data/scorecard_categories.csv')
hots = [[.1, .3, .5, .7, .9],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1]]

#######################
# Sidebar
with st.sidebar:
    st.title('Selection Scorecard')
    cat_list = list(df_reshaped.category.unique())[::-1]
    
    selected_category = st.selectbox('Select a Category', cat_list)
    df_selected_category = df_reshaped[df_reshaped.category == selected_category]
    df_selected_category_sorted = df_selected_category.sort_values(by="priority", ascending=False)
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    st.title('About')
    st.write('''
        Data Analysis completed by Virtusa.
        ''')
#######################
# Plots
# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Priority", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap
# Piechart
def make_pie(input_color_theme):
    pie = px.pie(scoredata, values='priority', names='category', title='Feature Prioritization')
    return pie

# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

#######################
# Dashboard Main Panel
st.title('Analysis of Multi-Channel Marketing Hub Capabilities')
col = st.columns((3, 3, .5), gap='medium')
with col[0]:
    st.markdown('#### Adobe')
    indexCount = 0
    for index, row in scoredata.iterrows():
        if row['adobeScore']==4:
            indexCount = indexCount + 1
        if row['adobeScore']==5:
            indexCount = indexCount + 1
    feature_complete = math.trunc(indexCount/scoredata['adobeScore'].count()*100)
    ease_implementation = indexCount
    donut_chart_greater = make_donut(feature_complete, 'Feature Complete', 'blue')
    donut_chart_less = make_donut(ease_implementation, 'Ease of Implementation', 'orange')
    st.write('Feature Completeness')
    st.altair_chart(donut_chart_greater) 
    st.markdown('Average')
    st.write(scoredata['adobeScore'].mean())    
with col[1]:
    st.markdown('#### Salesforce')
    indexCount = 0
    for index, row in scoredata.iterrows():
        if row['salesforceScore']==4:
            indexCount = indexCount + 1
        if row['salesforceScore']==5:
            indexCount = indexCount + 1
    feature_complete = math.trunc(indexCount/scoredata['salesforceScore'].count()*100)    
    ease_implementation = 40
    donut_chart_greater = make_donut(feature_complete, 'Feature Complete', 'blue')
    donut_chart_less = make_donut(ease_implementation, 'Ease of Implementation', 'orange')
    st.write('Feature Complete')
    st.altair_chart(donut_chart_greater)    
    st.markdown('Average')
    st.write(scoredata['salesforceScore'].mean())    
      
    
col = st.columns((.5, 6.5, 1), gap='medium')

with col[1]:
    st.markdown('#### Shared Prioritization Weighting')
    fig = px.pie(weightdata, values='weight', names='category', title=f'Feature Priotization', height=500, width=300)
    st.plotly_chart(fig, use_container_width=True)    
    st.markdown('#### (Weighted) Capability Scoring')

    st.markdown('### (Unweighted) Dimensional Scoring')
    #hardcoding in the summary numbers for now
    data=[[4, 4, 4, 5, 5, 4, 5, 5], [3, 4, 4, 4, 5, 4, 5, 3]]
    fig3 = px.imshow(data,
                labels=dict(x="Vendor", y="Dimension", color="Score"),
                x=['Interoperability', 'Technical', 'Security', 'Scalability', 'Capability','Reliability', 'Usability', 'Maturity'],
                y=['Adobe', 'Salesforce']
               )
    fig3.update_xaxes(side="top")
    st.plotly_chart(fig3, use_container_width=True)            
 

