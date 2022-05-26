import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt

st.title('Statistical analysis of accidents on federal highways in Brazil from 2018 to 2021.')
#st.write('Project made by Nicolas Lohan, student of Statistics Applied to Computing class, in Computer Engeneering course.')

@st.cache
def load_data():
    # import of data
    prf_2018 = pd.read_csv('https://arquivos.prf.gov.br/arquivos/index.php/s/MaC6cieXSFACNWT/download', compression='zip', encoding='latin1', sep=';')
    prf_2019 = pd.read_csv('https://arquivos.prf.gov.br/arquivos/index.php/s/kRBUylqz6DyQznN/download', compression='zip', encoding='latin1', sep=';')
    prf_2020 = pd.read_csv('https://arquivos.prf.gov.br/arquivos/index.php/s/jdDLrQIf33xXSCe/download', compression='zip', encoding='latin1', sep=';')
    prf_2021 = pd.read_csv('https://arquivos.prf.gov.br/arquivos/index.php/s/n1T3lymvIdDOzzb/download', compression='zip', encoding='latin1', sep=';')

    # matching columns types before merging
    prf_2021['latitude'] = prf_2021['latitude'].astype(str)
    prf_2021['longitude'] = prf_2021['longitude'].astype(str)

    # merging dataframes
    acidentes = pd.merge(prf_2018.merge(prf_2019, how="outer"), prf_2020.merge(prf_2021, how="outer"), how="outer")

    #correcting date type
    acidentes['data_inversa'] = acidentes['data_inversa'].str.replace("-", "")
    acidentes['data_inversa'] = pd.to_datetime(acidentes['data_inversa'], format='%Y%m%d')
    acidentes.rename(columns={'data_inversa':'data'}, inplace=True)

    return acidentes

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Imported DataFrames from PRF')
    st.write(data)

county = data.groupby('municipio').agg(n_acidentes = ('municipio', 'count'))
s = data.groupby(['uf', data['data'].dt.to_period('Y')]).agg(n_acidentes=('uf', 'count'))
s.reset_index(inplace=True)
state = pd.DataFrame(s).astype(str)
state.set_index('uf', inplace=True)


county_list = county.index
state_list = data['uf'].unique()

st.write("## Filter for accidents per county in Brazil")
counties = st.multiselect("Choose county", county_list, ['CAMPINA GRANDE'])
if not counties:
    st.error("Please select at least one country.")
else:
    st.write("#### Number of accidents between 2018 - 2021")
    county.loc[counties]


st.write("## Filter for accidents per state in Brazil")
states = st.multiselect("Choose state", state_list)

if states:
    year = st.radio("Choose year", state['data'].unique())
    st.write("#### Number of accidents", state.loc[state['data']==str(year)].loc[states])
else:
    st.error("Please select at least one state")
