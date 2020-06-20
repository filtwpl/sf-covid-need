import pandas as pd
from sodapy import Socrata as sc
import streamlit as st
client = sc("data.sfgov.org", None)
results = client.get("tpyr-dvnc")
df = pd.DataFrame.from_records(results)
df = df.drop(['last_updated_at', 'multipolygon', 'deaths'], axis=1)
df = df.drop(df[df.area_type == 'Census Tract'].index)
df = df.drop(df[df.area_type == 'ZCTA'].index)
df = df.drop('area_type', axis=1)
df = df.rename(columns={'acs_population': 'population', 'count': 'cases'})
df.rate = pd.to_numeric(df.rate)
df.cases = pd.to_numeric(df.cases)
df.population = pd.to_numeric(df.population)
df = df.fillna(value = {'cases': 0})
df['rate'] = df.cases/df.population*100
df = df.sort_values('rate', ascending=False)
#print(df['id'].values[0] + ", " + df['id'].values[1] + ", " + df['id'].values[2])

st.title("MFACA Recommended Mask Drive Sites")
st.write(df['id'].values[0] + ", " + df['id'].values[1] + ", " + df['id'].values[2])
st.dataframe(df)
