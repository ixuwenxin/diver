import streamlit as st
import pandas as pd

st.title("My first app")
st.sidebar.checkbox("Select")

# 允许用户上传CSV文件
uploaded_file = st.file_uploader("上传CSV文件", type=["csv"])
if uploaded_file is not None:
	# 读取CSV内容
	df = pd.read_csv(uploaded_file)
	st.write("### 文件内容：")
	st.dataframe(df)