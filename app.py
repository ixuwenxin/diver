import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pakages.figure import get_time_series_fig, get_hierarchical_fig


# Initialize the page
st.set_page_config(page_title="Excel Data Viewer", layout="wide")

st.title("Visual Stats")
# 扫描io目录下所有文件夹
io_dir = "io"
folders = [name for name in os.listdir(io_dir) if os.path.isdir(os.path.join(io_dir, name))]
with st.sidebar:
    selected_folder = st.selectbox("选择一个文件夹", folders)
    # 扫描选定目录下所有.xlsx文件 并显示在单选框中
    if selected_folder:
        folder_path = os.path.join(io_dir, selected_folder)
        excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
        selected_file = st.selectbox("选择Excel文件", excel_files)
    

# 读取选定的Excel文件中的Home表
if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        df_home = pd.read_excel(file_path, sheet_name='Home')
   
        #以Home表的Table_id列为工作表名，读取所有工作表；每个工作表从第6行开始读取，Home表中的Index_level存放着该工作表索引列数；分别创建对应个数st.tabs()页面，用来展示各个工作表的数据
        tab_names = ['Home'] + df_home['Table_id'].tolist() + ['Settings']
        index_levels = df_home['Index_level'].tolist()
        st_tabs = st.tabs(tab_names)
        # Home表tab
        with st_tabs[0]:
            df_home = st.data_editor(df_home)
        with st_tabs[-1]:
            st.write("Settings page content goes here.")
            template = st.selectbox("选择Plotly图表模板", ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "presentation", "xgridoff", "ygridoff", "gridon", "none"], index=6)
            width = st.number_input("图表宽度", min_value=400, max_value=1600, value=800, step=100)
            height = st.number_input("图表高度", min_value=300, max_value=1200, value=400, step=100)
        # 其它工作表tab
        for i, (table_id, index_level) in enumerate(zip(df_home['Table_id'], index_levels)):
            try:
                table_name = df_home.loc[df_home['Table_id'] == table_id, 'Table_name'].values[0] if 'Table_name' in df_home.columns else f"{table_id}"
                df_wide = pd.read_excel(file_path, sheet_name=table_id, skiprows=5)
                if index_level > 0:
                    df_wide.set_index(df_wide.columns[:index_level].tolist(), inplace=True)
                with st_tabs[i+1]:
                    st.write(f"数据表 - {table_name}")
                    if st.toggle(f"显示数据", key=f"toggle_{table_id}"):
                        st.dataframe(df_wide)
                    #Home表中的Data_type列表示对应工作表数据的类型，PA代表是宽面板数据，即每列代表一个时间截面上的数据；Column_axis_name代表列轴名称，转成日期时间类型；Value_name代表数值含义；请先将宽数据转换成长数据,另存为df_long
                    if 'Data_type' in df_home.columns and df_home.loc[df_home['Table_id'] == table_id, 'Data_type'].values[0] == 'PA':
                        column_axis_name = df_home.loc[df_home['Table_id'] == table_id, 'Column_axis_name'].values[0]
                        value_name = df_home.loc[df_home['Table_id'] == table_id, 'Value_name'].values[0]
                        df_long = df_wide.reset_index().melt(id_vars=df_wide.index.names, var_name=column_axis_name, value_name=value_name).set_index(df_wide.index.names)
                    # 根据Home表中从Line列开始到最后一列的配置，生成相应类型的plotly图表    
                    plot_types = df_home.columns[ df_home.columns.get_loc('Line'): ].tolist()

                    for plot_type in plot_types:    
                        if plot_type in ['Line', 'Area', 'Bar'] and df_home.loc[df_home['Table_id'] == table_id, plot_type].values[0] == 1:
                            con= st.expander(f"{plot_type} Plot", expanded=True)
                            # 给出选项，让用户选择针对哪列索引,对数据进行groupby操作，得到新的数据；x=column_axis_name，y=value_name,color=选择的索引列
                            index_options = df_long.index.names
                            selected_index = con.selectbox(f"选择索引列", index_options, index=0,key=f"{table_id}_index_{plot_type}")
                            if selected_index:
                                # 根据用户选择的索引,对数据进行groupby操作
                                df_filtered = df_long.groupby([selected_index, column_axis_name])[value_name].sum().reset_index()
                            else:
                                df_filtered = df_long.reset_index()

                            #如果column_axis_name.lower()的值为year（代表年份）/month(代表月份)/date(代表日期)，尝试分别将其转换为日期时间类型
                            try:
                                if column_axis_name.lower() == 'year':
                                    df_filtered[column_axis_name] = pd.to_datetime(df_filtered[column_axis_name], format='%Y')
                                elif column_axis_name.lower() == 'month':
                                    df_filtered[column_axis_name] = pd.to_datetime(df_filtered[column_axis_name], format='%Y-%m')
                                elif column_axis_name.lower() == 'date':
                                    df_filtered[column_axis_name] = pd.to_datetime(df_filtered[column_axis_name], format='%Y-%m-%d')
                            except Exception as e:
                                st.warning(f"无法将列轴 {column_axis_name} 转换为日期时间类型: {e}")
                            # 针对df_filtered时间序列图
                            if column_axis_name in df_filtered.columns and value_name in df_filtered.columns:
                                fig = get_time_series_fig(plot_type.lower(), df_filtered, x=column_axis_name, y=value_name, color=selected_index, title=f"{table_id} {table_name}")
                                con.plotly_chart(fig, use_container_width=False)
                            else:
                                con.warning(f"工作表 {table_id} 中缺少 column_axis_name 列或 '{value_name}' 列，无法生成时间序列图。")
                        # 添加代码以支持treemap, sunburst图表类型
                        elif plot_type in ['Treemap', 'Sunburst'] and df_home.loc[df_home['Table_id'] == table_id, plot_type].values[0] == 1:
                                con= st.expander(f"{plot_type} Plot", expanded=True)
                                # 让用户必须选择df_wide中的一列数据作为数值列
                                value_name = df_home.loc[df_home['Table_id'] == table_id, 'Value_name'].values[0]
                                selected_column = con.selectbox(f"选择一列", df_wide.columns, index=0, key=f"{table_id}_column_{plot_type}")
                                # 假设df_wide的索引列是层级关系，可以用来做treemap的path
                                selected_levels = df_wide.index.names
                                try:
                                    fig = get_hierarchical_fig(plot_type.lower(), df_wide.reset_index(), path=selected_levels, values=selected_column, title=f"{table_id} {table_name}", template=template, width=width, height=height) 
                                    con.plotly_chart(fig, use_container_width=False)

                                except Exception as e:
                                    st.error(f"无法生成层级图: {e}")

                                
                                   
            except Exception as e:
                st.error(f"无法读取工作表 {table_id}: {e}")