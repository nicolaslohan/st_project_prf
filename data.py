import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
import streamlit.components.v1 as components
import altair as alt

@st.cache
def load_data():
    # import of data
    prf_2018 = pd.read_csv('https://raw.githubusercontent.com/nicolaslohan/Projeto-PRF-EAC/main/Acidentes/datatran2018.csv', encoding='latin1', sep=';')
    prf_2019 = pd.read_csv('https://raw.githubusercontent.com/nicolaslohan/Projeto-PRF-EAC/main/Acidentes/datatran2019.csv', encoding='latin1', sep=';')
    prf_2020 = pd.read_csv('https://raw.githubusercontent.com/nicolaslohan/Projeto-PRF-EAC/main/Acidentes/datatran2020.csv', encoding='latin1', sep=';')
    prf_2021 = pd.read_csv('https://raw.githubusercontent.com/nicolaslohan/Projeto-PRF-EAC/main/Acidentes/datatran2021.csv', encoding='latin1', sep=';')

    # matching columns types before merging
    prf_2021['latitude'] = prf_2021['latitude'].astype(str)
    prf_2021['longitude'] = prf_2021['longitude'].astype(str)

    #merging data
    acidentes = merge_data(prf_2018, prf_2019, prf_2020, prf_2021)
    return acidentes

def merge_data(df1, df2, df3, df4):
    merged_data = pd.merge(df1.merge(df2, how="outer"), df3.merge(df4, how="outer"), how="outer")
    # change date column type to datetime
    merged_data['data_inversa'] = merged_data['data_inversa'].str.replace("-", "")
    merged_data['data_inversa'] = pd.to_datetime(merged_data['data_inversa'], format='%Y%m%d')
    merged_data.rename(columns={'data_inversa':'data'}, inplace=True)
    return merged_data

def county_filter(data):
    c = data.groupby('municipio').agg(n_acidentes = ('municipio', 'count'))
    county = pd.DataFrame(c).sort_values(ascending=True, by='n_acidentes')
    return county

def state_filter(data):
    s = data.groupby('uf').agg(n_acidentes=('uf', 'count'))
    state = pd.DataFrame(s).sort_values(ascending=True, by='n_acidentes')
    return state

def state_year_filter(data):
    s = data.groupby(['uf', data['data'].dt.to_period('Y')]).agg(n_acidentes=('uf', 'count'))
    s.reset_index(inplace=True)
    state = pd.DataFrame(s).astype(str)
    return state

def ac_per_county(data):

    county = county_filter(data)
    county_list = county.index

    st.write("## Filter for accidents per county in Brazil")
    counties = st.multiselect("Choose county", county_list)
    if not counties:
        st.error("Please select at least one country.")
    else:
        selected = ", ".join([str(x) for x in counties])
        st.write("#### Number of accidents between 2018 - 2021 in ", selected)
        county_df = county.loc[counties]
        st.write(county_df)

def ac_per_state(data):

    state = state_year_filter(data)
    state.set_index('uf', inplace=True)

    state_list = data['uf'].unique()

    st.write("## Filter for accidents per state and year in Brazil")
    states = st.multiselect("Choose state", state_list)

    if states:
        st_string = ", ".join([str(x) for x in states])
        year = st.radio("Choose year", state['data'].unique())
        st.write("#### Number of accidents of ", st_string, "in ", year)
        st.write(state.loc[state['data']==str(year)].loc[states])
    else:
        st.error("Please select at least one state")

def show_about():
    st.write("### Objectives")
    st.write("With Streamlit library, this project has the objective to better display the results of the previous pandas library's *exploratory* project, developed as a partial requirement for the Statistics Applied to Computing discipline. Futhermore, this application aims to be my *first step* towards the Data Science area.")
    st.write(""" 
    - Explore Streamlit library;
    - Clean interface; 
    - Display dynamic options of filtering;""")
    st.write("### Follow me on *GitHub*:")
    components.html("""
    <div class="github-profile-badge" data-user="nicolaslohan"></div>
<script src="https://cdn.jsdelivr.net/gh/Rapsssito/github-profile-badge@latest/src/widget.min.js"></script>""")

def ranking_county(data):
    dc = county_filter(data)
    rank = dc.nlargest(5, "n_acidentes")
    rank.reset_index(inplace=True)
    list = rank.astype(str)
    bar_chart = alt.Chart(list, height=200).mark_bar().encode(y='municipio:O', x='n_acidentes:Q')
    st.altair_chart(bar_chart, use_container_width=True)

def ranking_states(data):
    ds = state_filter(data)
    rank = ds.nlargest(5, "n_acidentes")
    rank.reset_index(inplace=True)
    list = rank.astype(str)
    bar_chart = alt.Chart(list, height=200).mark_bar().encode(y='uf:O', x='n_acidentes:Q')
    st.altair_chart(bar_chart, use_container_width=True)