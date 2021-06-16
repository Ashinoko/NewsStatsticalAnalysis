from scraper import Scraper
from processor import Processor
from generate_wordclouds import Clouds
from generate_graphs import Graphs

import streamlit as st

st.set_page_config(layout="wide")

st.title("Welcome to the news statistical analysis machine!")

st.text("This a tool brings new insight about news you've already read!")

scrape_button = st.button("Update DataBase")

if scrape_button:
    with st.spinner('Updating database...'):
        my_scraper = Scraper()
        my_scraper.update_data()
        my_processor = Processor()
        my_processor.process_store_csv()

col1, col2 = st.beta_columns([1, 10])

with col1:
    word_cloud = st.radio("WordCloud", [2019, 2020, 2021])

with col2:
    wordcloud_button = st.button("Generate WordCloud")

if wordcloud_button:
    my_cloud = Clouds()
    my_bar = st.progress(0)
    graphs = my_cloud.make_clouds(word_cloud, my_bar)
    st.pyplot(graphs)

text = st.text_input("Enter keywords separated by space")

if text:
    my_graph = Graphs()
    figures = my_graph.draw_graphs(text.lower().split())
    for fig in figures:
        st.pyplot(fig)
    st.balloons()

# while True:
#     user_input = str(input("Please input 'g' for the graphs or 'c' for word clouds, 'u'for scraper and database updates, 'q' to quit the program\n")).lower()

#     if user_input == 'q':
#         print('Quiting the program')
#         break

#     elif user_input =='u':

#         my_scraper = Scraper()
#         my_scraper.update_data()

#         my_processor = Processor()
#         my_processor.process_store_csv()

#     elif user_input == 'g':
#         my_graph = Graphs()
#         my_graph.draw_years_graphs()

#     elif user_input =='c':
#         my_cloud = Clouds()

#         my_cloud.make_years_clouds()
