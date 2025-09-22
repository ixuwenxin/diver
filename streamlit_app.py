import streamlit as st
import pandas as pd

st.title("My first app")
st.sidebar.checkbox("Select")

# 允许用户上传Excel文件
uploaded_file = st.file_uploader("上传Excel文件", type=["xls", "xlsx"])
if uploaded_file is not None:
    # 读取所有工作表
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    tabs = st.tabs(sheet_names)
    for i, sheet in enumerate(sheet_names):
        with tabs[i]:
            df = pd.read_excel(xls, sheet_name=sheet)
            st.write(f"### 工作表：{sheet}")
            st.dataframe(df)