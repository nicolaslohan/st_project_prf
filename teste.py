import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
import data as d

st.title('Statistical analysis of accidents on federal highways in Brazil from 2018 to 2021.')

data_load_state = st.text('Loading data...')
data = d.load_data()
data_load_state.text("Done!")

if st.checkbox('Show raw data'):
    st.subheader('Imported DataFrame from PRF')
    st.write(data)

list_options = ('About this project', '1. Accidents per county', '2. Accidents per state', '3. Accidents per county ranking', '4. Accidents per state ranking')

option = st.selectbox('Select the data you want to visualize...', list_options)

if option == 'About this project':
    d.show_about()
elif option == '1. Accidents per county':
    d.ac_per_county(data)
elif option == '2. Accidents per state':
    d.ac_per_state(data)
elif option == '3. Accidents per county ranking':
    d.ranking_county(data)
elif option == '4. Accidents per state ranking':
    d.ranking_states(data)
