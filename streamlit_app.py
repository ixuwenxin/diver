import streamlit as st
import pandas as pd

st.title("My first app")
st.sidebar.checkbox("Select")

# 允许用户上传Excel文件
uploaded_file = st.file_uploader("上传Excel文件", type=["xls", "xlsx"])
if uploaded_file is not None:
    # 读取Excel内容
    df = pd.read_excel(uploaded_file)
    st.write("### 文件内容：")
    st.dataframe(df)