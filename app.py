import streamlit as st
import pandas as pd
import plotly.express as px

st.title("My first app")
st.sidebar.checkbox("Select")

df = pd.DataFrame({
    "x": [1, 2, 3, 4, 5],
    "y": [10, 20, 30, 40, 50]
})

fig = px.line(df, x="x", y="y", title="Sample Plot")
st.plotly_chart(fig)
