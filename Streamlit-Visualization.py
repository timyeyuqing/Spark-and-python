import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import os
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import interp2d
from st_aggrid import AgGrid
    from st_aggrid.shared import GridUpdateMode
    from st_aggrid.grid_options_builder import GridOptionsBuilder
    #from istreamlit.index_monitor_page import IndexMonitorPage

xxxxxx
from plotly.subplots import make_subplots
csv_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
current_path = os.path.dirname(__file__)
from matplotlib.font_manager import FontProperties
#from istreamlit.index_monitor_page import IndexMonitorPage
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.set_option('deprecation.showPyplotGlobalUse', False)
chart_visual = st.sidebar.selectbox(' xxxxxx
',
                                    (' xxxxxx
if chart_visual == ' xxxxxx
':
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    the_day_before = today + datetime.timedelta(days=-2)
)
    #all_options = st.sidebar.checkbox("全选")
    #if all_options: phase = [xxxxxx]
    @st.cache(allow_output_mutation=True, ttl=1 * 60 * 60)
    def load_data():
     sql1="""
     xxxxxx
    """
     pd1=olap_query(sql1)
     return pd1
    pd1 = load_data()
    # xxxxxx
xxxxxx =f"{pd1[xxxxxx].values[0]:.2%}"
    easy_abroad_rate_yesterday_difference = f"{pd1['easy_abroad_rate'].values[0] - pd1['easy_abroad_rate'].values[1]:.2%}"
    easy_abroad_rate_yesterday = f"{abs(pd1['easy_abroad_rate'].values[0] - pd1['easy_abroad_rate'].values[1]) :.2%}"
    if pd1['easy_abroad_rate'].values[0] - pd1['easy_abroad_rate'].values[1] >=0:
        easy_abroad_rate_difference = '🔺' + str(easy_abroad_rate_yesterday)
    else:
        easy_abroad_rate_difference = '🔻'+ str(easy_abroad_rate_yesterday)
    # xxxxxx
    load_mode_rate = f"{pd1['load_mode_rate'].values[0]:.2%}"
    load_mode_rate_yesterday_difference = f"{pd1['load_mode_rate'].values[0] - pd1['load_mode_rate'].values[1] :.2%}"
    load_mode_rate_yesterday = f"{abs(pd1['load_mode_rate'].values[0] - pd1['load_mode_rate'].values[1]) :.2%}"
    if pd1['load_mode_rate'].values[0] - pd1['load_mode_rate'].values[1] >=0:
        load_mode_rate_difference = '🔺'+str(load_mode_rate_yesterday)
    else:
        load_mode_rate_difference = '🔻'+str(load_mode_rate_yesterday)
    # xxxxxx
    lifting_mode_rate  = f"{pd1['lifting_mode_rate'].values[0]:.2%}"
    lifting_mode_rate_yesterday_difference = f"{pd1['lifting_mode_rate'].values[0] - pd1['lifting_mode_rate'].values[1] :.2%}"
    lifting_mode_rate_yesterday = f"{abs(pd1['lifting_mode_rate'].values[0] - pd1['lifting_mode_rate'].values[1]) :.2%}"
    if pd1['lifting_mode_rate'].values[0] - pd1['lifting_mode_rate'].values[1] >=0:
         lifting_mode_rate_difference = '🔺'+str(lifting_mode_rate_yesterday)
    else:
         lifting_mode_rate_difference = '🔻'+str(lifting_mode_rate_yesterday)





    st.subheader(' xxxxxx ',anchor= xxxxxx)
    col1, col2, col3, col4 = st.columns((1,1,1,1.6))
    with col1:
        vin2 = st.text_input('请选择vin')
    with col2:
        start_date_2 = st.date_input('开始日期 （含当日）', yesterday_10,key = 6)
    with col3:
        end_date_2 = st.date_input('结束日期（含当日）', today, key = 6)
    with col4:
    with col1:

    #front
    x_cur = [xxxxxx]
    y_vel xxxxxx]
    #Front Dampr Force
    z = np.array([(xxxxxx)])
    #Rear Dampr Force
    z_rear = np.array([(xxxxxx)]    f_rear = interp2d(x_cur,y_vel,z_rear,kind = 'linear',fill_value=None)
    def load_data():
        data = pd.read_csv(f'{csv_path}/cur_vel.csv')
        return data
    data2 = load_data()




    data3 = pd.DataFrame (ff_FL, columns = ['N'])
    data5 = pd.DataFrame (ff_FR, columns = ['N'])
    data7 = pd.DataFrame (ff_RL, columns = ['N'])
    data9 = pd.DataFrame (ff_RR, columns = ['N'])
    data4 = pd.concat([data2[' xxxxxx], data3['N'], data2[xxxxxx FL_A']], axis=1, keys=['m_ xxxxxx, 'DampForce','m_ xxxxxx])
    data6 = pd.concat([data2['m_ xxxxxx s'], data5['N'], data2['m_ xxxxxx _FR_A']], axis=1, keys=['m_ xxxxxx, 'DampForce','m_ xxxxxx])
    data8 = pd.concat([data2['m_ xxxxxx mps'], data7['N'], data2['m_ xxxxxx _A']], axis=1, keys=['m_DmpCtl_i_suspVel_RL_mps', 'DampForce','m_ xxxxxx _A'])
    data10 = pd.concat([data2['m_ xxxxxx mps'], data9['N'], data2['m_ xxxxxx _A']], axis=1, keys=['m_ xxxxxx mps', 'DampForce','m xxxxxx _A'])




    df2 = pd.DataFrame(dict(
            x = xxxxxx            ))
    df3 = pd.DataFrame(dict(
            xxxxxx xxxxxx xxxxxx xxxxxx xxxxxx xxxxxx    if all_vin:
        if loc == 'FL':
            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(y=df2.y1, x=df2.x,
                                     mode = 'lines',
                                     name= 'ZF Front soft', line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig5.add_trace(go.Scatter(y=df2.y2, x=df2.x,
                                     mode = 'lines',
                                     name= 'ZF Front hard',line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig5.add_trace(go.Scatter(y=df3.y1, x=df3.x,
                                     mode = 'lines',
                                     name= 'TN Front soft',line_shape = 'linear',
                                     line=dict(color='firebrick',width=2)))
            fig5.add_trace(go.Scatter(y=df3.y2, x=df3.x,
                                     mode = 'lines',
                                     name= 'TN Front hard',line_shape = 'linear',
                                     line=dict(color='firebrick',width=2)))
            fig5.add_trace(go.Scatter(x=data4.m_DmpCtl_i_suspVel_FL_mps,y=data4.DampForce,
                                    mode = 'markers',
                                    marker=dict(
                                        size=3,
                                        color=data4.m_DmpCtl_damprCur_FL_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig5.update_yaxes(title_text = "<b>(N)<b>", title_standoff=5,side = "left")
            fig5.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                      yanchor="top",
                                      y=0.99,
                                      xanchor="right",
                                      x=0.99
                                  ),
                               margin=dict(l=0, r=200,b=40,t=20),
                                             )
            fig5.show()
            st.plotly_chart(fig5,height=600,width=900,use_container_width=True)
        if loc == 'FR':
            fig6 = go.Figure()
            fig6.add_trace(go.Scatter(y=df2.y1, x=df2.x,
                                     mode = 'lines',
                                     name= 'Front soft', line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig6.add_trace(go.Scatter(y=df2.y2, x=df2.x,
                                     mode = 'lines',
                                     name= 'Front hard',line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig6.add_trace(go.Scatter(y=df3.y1, x=df3.x,
                                     mode = 'lines',
                                     name= 'TN Front soft',line_shape = 'linear',
                                     line=dict(color='firebrick',width=2)))
            fig6.add_trace(go.Scatter(y=df3.y2, x=df2.x,
                                     mode = 'lines',
                                     name= 'TN Front hard',line_shape = 'linear',
                                     line=dict(color='firebrick',width=2)))
            fig6.add_trace(go.Scatter(x=data6.m_DmpCtl_i_suspVel_FR_mps,y=data6.DampForce,
                                    mode = 'markers',
                                    name = '',
                                    marker=dict(
                                        size=3,
                                        color=data6.m_DmpCtl_damprCur_FR_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig6.update_yaxes(title_text = "<b>(N)<b>", title_standoff=5)
            fig6.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                      yanchor="top",
                                      y=0.99,
                                      xanchor="right",
                                      x=0.99
                                  ),
                               margin=dict(l=0, r=200,b=40,t=20),
                                             )
            fig6.show()
            st.plotly_chart(fig6,height=600,width=900,use_container_width=True)
        if loc == 'RL':
            fig7 = go.Figure()
            fig7.add_trace(go.Scatter(y=df2.y3, x=df2.x,
                                     mode = 'lines',
                                     name= 'ZF Rear soft', line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig7.add_trace(go.Scatter(y=df2.y4, x=df2.x,
                                     mode = 'lines',
                                     name= 'ZF Rear hard',line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig7.add_trace(go.Scatter(y=df3.y3, x=df3.x,
                                    mode = 'lines',
                                    name= 'TN Rear soft',line_shape = 'linear',
                                    line=dict(color='firebrick',width=2)))
            fig7.add_trace(go.Scatter(y=df3.y4, x=df3.x,
                                    mode = 'lines',
                                    name= 'TN Rear hard',line_shape = 'linear',
                                    line=dict(color='firebrick',width=2)))
            fig7.add_trace(go.Scatter(x=data8.m_DmpCtl_i_suspVel_RL_mps,y=data8.DampForce,
                                    mode = 'markers',
                                    marker=dict(
                                        size=3,
                                        color=data8.m_DmpCtl_damprCur_RL_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig7.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                      yanchor="top",
                                      y=0.99,
                                      xanchor="right",
                                      x=0.99
                                  ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b> xxxxxx (m/s)<b>"
                                             )
            fig7.show()
            st.plotly_chart(fig7,height=600,width=900,use_container_width=True)
        if loc == 'RR':
            fig8 = go.Figure()
            fig8.add_trace(go.Scatter(y=df2.y3, x=df2.x,
                                     mode = 'lines',
                                     name= 'Rear soft', line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig8.add_trace(go.Scatter(y=df2.y4, x=df2.x,
                                     mode = 'lines',
                                     name= 'Rear hard',line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig8.add_trace(go.Scatter(y=df3.y3, x=df3.x,
                                    mode = 'lines',
                                    name= 'TN Rear soft',line_shape = 'linear',
                                    line=dict(color='firebrick',width=2)))
            fig8.add_trace(go.Scatter(y=df3.y4, x=df3.x,
                                    mode = 'lines',
                                    name= 'TN Rear hard',line_shape = 'linear',
                                    line=dict(color='firebrick',width=2)))
            fig8.add_trace(go.Scatter(x=data10.m_DmpCtl_i_suspVel_RR_mps,y=data10.DampForce,
                                    mode = 'markers',
                                    marker=dict(
                                        size=3,
                                        color=data10.m_DmpCtl_damprCur_RR_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig8.update_yaxes(title_text = "<b> xxxxxx (N)<b>", title_standoff=5)
            fig8.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                      yanchor="top",
                                      y=0.99,
                                      xanchor="right",
                                      x=0.99
                                  ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b> xxxxxx (m/s)<b>"
                                             )
            fig8.show()
            st.plotly_chart(fig8,height=600,width=900,use_container_width=True)
    else:
        if loc == 'FL':
            fig9 = go.Figure()
            fig9.add_trace(go.Scatter(y=df2.y1, x=df2.x,
                                     mode = 'lines',
                                     name= 'Front soft', line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig9.add_trace(go.Scatter(y=df2.y2, x=df2.x,
                                     mode = 'lines',
                                     name= 'Front hard',line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig9.add_trace(go.Scatter(x=data4.m_DmpCtl_i_suspVel_FL_mps,y=data4.DampForce,
                                    mode = 'markers',
                                    marker=dict(
                                        size=3,
                                        color=data4.m_DmpCtl_damprCur_FL_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig9.update_yaxes(title_text = "<b> xxxxxx (N)<b>", title_standoff=5)
            fig9.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = False,
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b> xxxxxx (m/s)<b>"
                                             )
            fig9.show()
            st.plotly_chart(fig9,height=600,width=900,use_container_width=True)
        if loc == 'FR':
            fig10 = go.Figure()
            fig10.add_trace(go.Scatter(y=df2.y1, x=df2.x,
                                     mode = 'lines',
                                     name= 'Front soft', line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig10.add_trace(go.Scatter(y=df2.y2, x=df2.x,
                                     mode = 'lines',
                                     name= 'Front hard',line_shape = 'linear',
                                     line=dict(color='royalblue',width=2)))
            fig10.add_trace(go.Scatter(x=data6.m_DmpCtl_i_suspVel_FR_mps,y=data6.DampForce,
                                    mode = 'markers',
                                    marker=dict(
                                        size=3,
                                        color=data6.m_DmpCtl_damprCur_FR_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig10.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = False,
                               margin=dict(l=0, r=200,b=40,t=20),
                                             )
            fig10.show()
            st.plotly_chart(fig10,height=600,width=900,use_container_width=True)
    with st.expander("上图说明："):
        st.write('X xxxxxx **')


    col1, col2, col3 = st.columns(3) 
    with col1:
        st.title("")
    with col1:
        st.title("")
    st.subheader("",anchor=xxxxxxx)
    st.subheader("",anchor= xxxxxxx)
    #ETL
    today = datetime.date.today()
    #ETL
    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def load_data5():
        sql1="""
        xxxxxxx xxxxxxx xxxxxxx    """
        pd1=olap_query(sql1)
        return pd1
    pd1 = load_data5()
    # xxxxxxx cnt distinct vin
    cnt = pd1['cnt'].values[0]
    #ETL
    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def load_data6():
        sql2="""
        xxxxxxx    """
        pd2=olap_query(sql2)
        return pd2
    pd2 = load_data6()
    #ETL
    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def load_data7():
        sql5="""
xxxxxxx xxxxxxx xxxxxxx xxxxxxx    """
        pd5=olap_query(sql5)
        return pd5
    pd5 = load_data7()
    
    # unixtime 转化为 timestamp
    def to_datetime(x):
        return pd.to_datetime(pd.to_datetime(x, utc=True, unit="s").tz_convert('Asia/Shanghai').strftime("%Y-%m-%d %H:%M:%S"))

    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def get_running_cycle(vin, arouse_time, sleep_time):
        sql = f"""
                select vin, UNIX_TIMESTAMP(start_time)-500 as arouse_time, UNIX_TIMESTAMP(end_time)+500 as sleep_time,dt,cast(dt as date) as dt2
                from xxxxxxx xxxxxxx xxxxxxx                where dt >= '{arouse_time}' and dt <= '{sleep_time}'
                and vin = '{vin}'
                order by vin, dt desc
            """
        try:
            df = olap_query(sql)
        except:
            df = pd.DataFrame(columns=["vin", "arouse_time", "sleep_time", "dt"])

        return df

    
    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def get_sig_data(vin, start_date, end_date, sigs):
        sql = f"""
                select vin, sig_name, sig_val, arouse_time, sleep_time, val_start_time, val_end_time, dt
                from xxxxxxx xxxxxxx
                where dt >= '{start_date}' and dt <= '{end_date}'            
                and vin = '{vin}'
                and sig_name in ('{"', '".join(sigs)}')
                order by vin, sig_name, val_start_time
            """
        print(sql)
        try:
            df = olap_query(sql)
        except:
            df = pd.DataFrame(columns=["vin", "sig_name", "sig_val", "arouse_time", "sleep_time", "time_start", "time_end", "val_start_time", "val_end_time", "dt"])
        df["val_start_datetime"] = df["val_start_time"].apply(lambda x: to_datetime(x))
        df["val_end_datetime"] = df["val_end_time"].apply(lambda x: to_datetime(x))

        return df


    # 信号拉平
    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def pivot_sig_data(df, sigs):
        df["collect_time"] = df.apply(lambda x: np.arange(x["val_start_time"], x["val_end_time"]), axis=1)
        new_df = df[["vin", "arouse_time", "sleep_time", "sig_name", "sig_val", "collect_time"]].explode("collect_time")
        pivot_df = pd.pivot_table(new_df, index=["vin", "arouse_time", "sleep_time", "collect_time"], columns="sig_name", values="sig_val", aggfunc="max").reset_index()
        for sig in sigs:
            if sig not in pivot_df.columns:
                pivot_df[sig] = np.NaN
        pivot_df["collect_datetime"] = pivot_df["collect_time"].apply(lambda x: to_datetime(x))
        pivot_df.sort_values(by=["collect_time"], inplace=True)
        return pivot_df

    #加入plotly工具包
    @st.cache(allow_output_mutation=True, ttl=0.5 * 60 * 60)
    def plot_pivot_sigs(pivot_df, sigs, fault_time, end_time):
        fig = go.Figure()
        cols = pivot_df.columns
        if fault_time:
            fig.add_vrect(x0=fault_time, x1=fault_time,
                          annotation_text=" xxxxxxx ", annotation_position="top left",
                          fillcolor="purple", line_width=2, line_dash="dash", line_color="purple",)
        if fault_time and end_time:
            fig.add_vrect(x0=fault_time, x1=end_time,
                          fillcolor="purple", opacity=0.25, line_width=0)
        for sig in sigs:
            if sig in cols:
                fig.add_trace(
                    go.Scatter(
                        x=pivot_df["collect_datetime"],
                        y=pivot_df[sig],
                        name=sig,
                        mode="markers+lines",
                        marker=dict(size=2),
                        showlegend=True
                    )
                )
        fig.update_layout(yaxis_range=[min(sigs),max(sigs)],
            height=300,
            margin=dict(t=10, b=0, l=0, r=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.0,
                xanchor="left",
                x=0.01
            )
        )
        return fig


    sigs = ["xxxxxxx ", " xxxxxxx ", " xxxxxxx ", " xxxxxxx "]




    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3) 
    with col1:
            choice = st.radio(" ",("日","周","月"),key = 1)
    if choice == "日":   
        #日期选择
        yesterday = today + datetime.timedelta(days=-1)
        yesterday_10 = today + datetime.timedelta(days=-11)
        col1, col2 = st.columns(2)
        with col1:
            start_date_1 = st.date_input('开始日期 （含当日）', yesterday_10,key=17)
        with col2:
            end_date_1 = st.date_input('结束日期（含当日）', today,key=18)
        if start_date_1 > end_date_1:
            st.error('Error: 开始日期必须在结束日期之前')
        pd3 = pd1.loc[(pd1['dt2'] >= start_date_1)  & (pd1['dt2']<= end_date_1)]

        fig1 = go.Figure()
        # set up plotly figure
        fig1.add_trace(go.Scatter(x=pd3['dt'], y=pd3['cnt'],
                                 mode = 'lines',
                                 name= ' xxxxxxx ', line_shape = 'linear',
                                 line=dict(color='mediumvioletred',width=2)))
        fig1.update_layout(
                           height=400,width=900,
                           showlegend = True,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>", legend=dict(
                                                      yanchor="top",
                                                      y=0.99,
                                                      xanchor="left",
                                                      x=0.01
                                                  )
                                         )

        fig1.show()
        st.plotly_chart(fig1,height=600,width=900,use_container_width=True)

        pd6 = pd5.loc[(pd5['dt'] >= start_date_1) & (pd5['dt'] <= end_date_1)]

        gd = GridOptionsBuilder.from_dataframe(pd6)   
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(groupable=True, editable=True) 

        gd.configure_selection(selection_mode="single", use_checkbox=True)
        gridOptions = gd.build()    
        grid_data = AgGrid(pd6, 
                  gridOptions=gridOptions, 
                  enable_enterprise_modules=True, 
                  allow_unsafe_jscode=True, 
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                theme = 'light'
                  )

        selected_rows = grid_data["selected_rows"]
        selected_rows = pd.DataFrame(selected_rows)

        if len(selected_rows) != 0:
            st.subheader("xxxxxxx ")
            vin=selected_rows["vin"].values[0]
            dt=selected_rows["dt"].values[0]
            pd7 = pd2.loc[(pd2['dt'] == dt) & (pd2['vin'] == vin)]


            pd7.drop('dt2',axis=1,inplace=True)

            gd = GridOptionsBuilder.from_dataframe(pd7)   
            gd.configure_pagination(enabled=True)
            gd.configure_default_column(groupable=True, editable=True) 

            gd.configure_selection(selection_mode="single", use_checkbox=True)
            gridOptions = gd.build()    
            grid_data = AgGrid(pd7, 
                      gridOptions=gridOptions, 
                      enable_enterprise_modules=True, 
                      allow_unsafe_jscode=True, 
                      update_mode=GridUpdateMode.SELECTION_CHANGED,
                    theme = 'light'
                      )
            selected_rows = grid_data["selected_rows"]
            selected_rows = pd.DataFrame(selected_rows)
            if len(selected_rows) != 0:
                vin_detailed=selected_rows["vin"].values[0]
                dt_detailed=selected_rows["dt"].values[0] 
                down_t =selected_rows["down_t"].values[0] 
                start_time = selected_rows["start_time"].values[0]
                start_time_epouch=int(pd.Timestamp(start_time).timestamp())-8*60*60
                end_time_epouch=int(pd.Timestamp(start_time).timestamp()) +down_t -8*60*60
                sig_df = get_sig_data(vin_detailed, dt_detailed, dt_detailed, sigs)
                running_cycle = get_running_cycle(vin_detailed, dt_detailed, dt_detailed).drop_duplicates(subset=['vin', 'dt','arouse_time'], keep='last')
                fault_running_cycle = running_cycle.loc[
                    (running_cycle["arouse_time"]-3 <= start_time_epouch) & (running_cycle["sleep_time"]+3 >= end_time_epouch )]
                fault_start_time = fault_running_cycle.iloc[0]["arouse_time"] if len(fault_running_cycle) > 0 else None
                end_time = to_datetime(end_time_epouch)
                pivot_df = pivot_sig_data(sig_df.loc[sig_df["val_start_time"] < start_time_epouch + 3600], sigs)
                pivot_df = pivot_df.loc[
                    (pivot_df["collect_time"] >= start_time_epouch-100) & (pivot_df["collect_time"] <=end_time_epouch + 100 )]

                st.plotly_chart(
                    plot_pivot_sigs(pivot_df, ["xxxxxxx ", " xxxxxxx "," xxxxxxx "," xxxxxxx "], start_time, end_time),
                use_container_width=True)












    if choice == "周":
        #日期选择
        yesterday = today + datetime.timedelta(days=-1)
        yesterday_10 = today + datetime.timedelta(days=-111)
        col1, col2 = st.columns(2)
        with col1:
            start_date_1 = st.date_input('开始日期 （含当日）', yesterday_10, key=13)
        with col2:
            end_date_1 = st.date_input('结束日期（含当日）', today, key=14)
        if start_date_1 > end_date_1:
            st.error('Error: 开始日期必须在结束日期之前')
        pd3 = pd1.loc[(pd1['dt2'] >= start_date_1)  & (pd1['dt2']<= end_date_1)].groupby('week_id').sum().reset_index()
        fig1 = go.Figure()
        # set up plotly figure
        fig1.add_trace(go.Scatter(x=pd3['week_id'], y=pd3['cnt'],
                                 mode = 'lines',
                                 name= ' xxxxxxx ', line_shape = 'linear',
                                 line=dict(color='mediumvioletred',width=2)))
        fig1.update_layout(
                           height=400,width=900,
                           showlegend = True,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>Week ID<b>", legend=dict(
                                                      yanchor="top",
                                                      y=0.99,
                                                      xanchor="left",
                                                      x=0.01
                                                  )
                                         )

        fig1.show()
        st.plotly_chart(fig1,height=600,width=900,use_container_width=True)

        st.subheader("xxxxxxx ")
        pd6 = pd5.loc[(pd5['dt'] >= start_date_1) & (pd5['dt'] <= end_date_1)]
        gd = GridOptionsBuilder.from_dataframe(pd6)   
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(groupable=True, editable=True) 

        gd.configure_selection(selection_mode="single", use_checkbox=True)
        gridOptions = gd.build()    
        grid_data = AgGrid(pd6, 
                  gridOptions=gridOptions, 
                  enable_enterprise_modules=True, 
                  allow_unsafe_jscode=True, 
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                theme = 'light'
                  )

        selected_rows = grid_data["selected_rows"]
        selected_rows = pd.DataFrame(selected_rows)

        if len(selected_rows) != 0:
            vin=selected_rows["vin"].values[0]
            dt=selected_rows["dt"].values[0]
            pd7 = pd2.loc[(pd2['dt'] == dt) & (pd2['vin'] == vin)]
            pd7.drop('dt2',axis=1,inplace=True)
            gd = GridOptionsBuilder.from_dataframe(pd7)   
            gd.configure_pagination(enabled=True)
            gd.configure_default_column(groupable=True, editable=True) 

            gd.configure_selection(selection_mode="single", use_checkbox=True)
            gridOptions = gd.build()    
            grid_data = AgGrid(pd7, 
                      gridOptions=gridOptions, 
                      enable_enterprise_modules=True, 
                      allow_unsafe_jscode=True, 
                      update_mode=GridUpdateMode.SELECTION_CHANGED,
                    theme = 'light'
                      )
            selected_rows = grid_data["selected_rows"]
            selected_rows = pd.DataFrame(selected_rows)
            if len(selected_rows) != 0:
                vin_detailed=selected_rows["vin"].values[0]
                dt_detailed=selected_rows["dt"].values[0] 
                down_t =selected_rows["down_t"].values[0] 
                start_time = selected_rows["start_time"].values[0]
                start_time_epouch=int(pd.Timestamp(start_time).timestamp())-8*60*60
                end_time_epouch=int(pd.Timestamp(start_time).timestamp()) +down_t -8*60*60
                sig_df = get_sig_data(vin_detailed, dt_detailed, dt_detailed, sigs)
                running_cycle = get_running_cycle(vin_detailed, dt_detailed, dt_detailed).drop_duplicates(subset=['vin', 'dt','arouse_time'], keep='last')
                fault_running_cycle = running_cycle.loc[
                    (running_cycle["arouse_time"]-3 <= start_time_epouch) & (running_cycle["sleep_time"]+3 >= end_time_epouch )]
                fault_start_time = fault_running_cycle.iloc[0]["arouse_time"] if len(fault_running_cycle) > 0 else None
                end_time = to_datetime(end_time_epouch)
                pivot_df = pivot_sig_data(sig_df.loc[sig_df["val_start_time"] < start_time_epouch + 3600], sigs)
                pivot_df = pivot_df.loc[
                    (pivot_df["collect_time"] >= start_time_epouch-100) & (pivot_df["collect_time"] <=end_time_epouch + 100 )]

                st.plotly_chart(
                    plot_pivot_sigs(pivot_df, ["xxxxxxx ", " xxxxxxx "," xxxxxxx "," xxxxxxx "], start_time, end_time),
                use_container_width=True)


    if choice == "月":
        #日期选择
        yesterday = today + datetime.timedelta(days=-1)
        yesterday_10 = today + datetime.timedelta(days=-366)
        col1, col2 = st.columns(2)
        with col1:
            start_date_1 = st.date_input('开始日期 （含当日）', yesterday_10,key=15)
        with col2:
            end_date_1 = st.date_input('结束日期（含当日）', today,key=16)
        if start_date_1 > end_date_1:
            st.error('Error: 开始日期必须在结束日期之前')
        pd3 = pd1.loc[(pd1['dt2'] >= start_date_1)  & (pd1['dt2']<= end_date_1)].groupby('month_short_desc').sum().reset_index()
        fig1 = go.Figure()
        # set up plotly figure
        fig1.add_trace(go.Scatter(x=pd3['month_short_desc'], y=pd3['cnt'],
                                 mode = 'lines',
                                 name= '', line_shape = 'linear',
                                 line=dict(color='mediumvioletred',width=2)))
        fig1.update_layout(
                           height=400,width=900,
                           showlegend = True,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>月份<b>", legend=dict(
                                                      yanchor="top",
                                                      y=0.99,
                                                      xanchor="left",
                                                      x=0.01
                                                  )
                                         )

        fig1.show()
        st.plotly_chart(fig1,height=600,width=900,use_container_width=True)

        st.subheader("")
        pd6 = pd5.loc[(pd5['dt'] >= start_date_1) & (pd5['dt'] <= end_date_1)]

        gd = GridOptionsBuilder.from_dataframe(pd6)   
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(groupable=True, editable=True) 

        gd.configure_selection(selection_mode="single", use_checkbox=True)
        gridOptions = gd.build()    
        grid_data = AgGrid(pd6, 
                  gridOptions=gridOptions, 
                  enable_enterprise_modules=True, 
                  allow_unsafe_jscode=True, 
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                theme = 'light'
                  )

        selected_rows = grid_data["selected_rows"]
        selected_rows = pd.DataFrame(selected_rows)

        if len(selected_rows) != 0:
            st.subheader("")
            vin=selected_rows["vin"].values[0]
            dt=selected_rows["dt"].values[0]
            pd7 = pd2.loc[(pd2['dt'] == dt) & (pd2['vin'] == vin)]
            pd7.drop('dt2',axis=1,inplace=True)
            gd = GridOptionsBuilder.from_dataframe(pd7)   
            gd.configure_pagination(enabled=True)
            gd.configure_default_column(groupable=True, editable=True) 

            gd.configure_selection(selection_mode="single", use_checkbox=True)
            gridOptions = gd.build()    
            grid_data = AgGrid(pd7, 
                      gridOptions=gridOptions, 
                      enable_enterprise_modules=True, 
                      allow_unsafe_jscode=True, 
                      update_mode=GridUpdateMode.SELECTION_CHANGED,
                    theme = 'light'
                      )
            selected_rows = grid_data["selected_rows"]
            selected_rows = pd.DataFrame(selected_rows)
            if len(selected_rows) != 0:
                vin_detailed=selected_rows["vin"].values[0]
                dt_detailed=selected_rows["dt"].values[0] 
                down_t =selected_rows["down_t"].values[0] 
                start_time = selected_rows["start_time"].values[0]
                start_time_epouch=int(pd.Timestamp(start_time).timestamp())-8*60*60
                end_time_epouch=int(pd.Timestamp(start_time).timestamp()) +down_t -8*60*60
                sig_df = get_sig_data(vin_detailed, dt_detailed, dt_detailed, sigs)
                running_cycle = get_running_cycle(vin_detailed, dt_detailed, dt_detailed).drop_duplicates(subset=['vin', 'dt','arouse_time'], keep='last')
                fault_running_cycle = running_cycle.loc[
                    (running_cycle["arouse_time"]-3 <= start_time_epouch) & (running_cycle["sleep_time"]+3 >= end_time_epouch )]
                fault_start_time = fault_running_cycle.iloc[0]["arouse_time"] if len(fault_running_cycle) > 0 else None
                end_time = to_datetime(end_time_epouch)
                pivot_df = pivot_sig_data(sig_df.loc[sig_df["val_start_time"] < start_time_epouch + 3600], sigs)
                pivot_df = pivot_df.loc[
                    (pivot_df["collect_time"] >= start_time_epouch-100) & (pivot_df["collect_time"] <=end_time_epouch + 100 )]

                st.plotly_chart(
                    plot_pivot_sigs(pivot_df, ["xxxxxxx ", " xxxxxxx "," xxxxxxx "," xxxxxxx "], start_time, end_time),
                use_container_width=True)
            
    st.subheader('',anchor= xxxxxxx)
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    date = st.date_input('日期', yesterday,key=21)
    #ETL
    @st.cache(allow_output_mutation=True, ttl=1 * 60 * 60)
    def load_data8():
        sql1="""
        xxxxxxx    """%(date)
        pd1=olap_query(sql1)
        return pd1
    pd1 = load_data8()
    # xxxxxxx    total_vin = pd1['vin'].count()
    total_times = pd1['times'].sum()
    st.subheader("`%s` xxxxxxx "%(date,total_vin,total_times))
    with st.expander("xxxxxxx："):
        st.info("xxxxxxx
    @st.cache(allow_output_mutation=True, ttl=1 * 60 * 60)
    def convert_df(pd1):
       return pd1.to_csv().encode('utf-8')


    csv = convert_df(pd1)

    st.download_button(
       " xxxxxxx "%(date),
       csv,
       "file.csv",
       "text/csv",
       key='download-csv'
    )
    #ETL
    @st.cache(allow_output_mutation=True, ttl=1 * 60 * 60)
    def load_data9():
        sql2="""
        xxxxxxx    """%(date)
        pd2=olap_query(sql2)
        return pd2
    pd2 = load_data9()
    gd = GridOptionsBuilder.from_dataframe(pd1)   
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(groupable=True, editable=True) 

    gd.configure_selection(selection_mode="single", use_checkbox=True)
    gridOptions = gd.build()    
    grid_data = AgGrid(pd1, 
              gridOptions=gridOptions, 
              enable_enterprise_modules=True, 
              allow_unsafe_jscode=True, 
              update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme = 'light'
              )
    selected_rows = grid_data["selected_rows"]
    selected_rows = pd.DataFrame(selected_rows)
    @st.cache(allow_output_mutation=True, ttl=1 * 60 * 60)
    def convert_df(pd2):
       return pd2.to_csv().encode('utf-8')


    csv2 = convert_df(pd2)

    st.download_button(
       " xxxxxxx "%(date),
       csv2,
       "file.csv",
       "text/csv",
       key='download-csv'
    )
    if len(selected_rows) != 0:
        vin_detailed=selected_rows["vin"].values[0]
        pd3 = pd2.loc[(pd2['vin'] == vin_detailed)]
        gd = GridOptionsBuilder.from_dataframe(pd3)   
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(groupable=True, editable=True) 

        gd.configure_selection(selection_mode="single", use_checkbox=True)
        gridOptions = gd.build()    
        grid_data = AgGrid(pd3, 
                  gridOptions=gridOptions, 
                  enable_enterprise_modules=True, 
                  allow_unsafe_jscode=True, 
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                theme = 'light'
                  )
        selected_rows = grid_data["selected_rows"]
        selected_rows = pd.DataFrame(selected_rows)
        
