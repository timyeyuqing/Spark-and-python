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
import numpy as np
from ilad_pyspark import olap_query,olap_ods_query,olap_query_ontest
from plotly.subplots import make_subplots
csv_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
current_path = os.path.dirname(__file__)
from matplotlib.font_manager import FontProperties
#from istreamlit.index_monitor_page import IndexMonitorPage
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.set_option('deprecation.showPyplotGlobalUse', False)
chart_visual = st.sidebar.selectbox('性能监控',
                                    ('电磁阀耐久', '电磁阀性能','xxx'))
if chart_visual == '电磁阀耐久':
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    the_day_before = today + datetime.timedelta(days=-2)
    #phase = st.sidebar.multiselect("请选择试验车阶段（多选）", ['PPV3','EP2','EP','PPV2','PPV1','PP1','PPV3','PRE-PPV','EP1','骡车','PPV','MULE','PP2'])
    #all_options = st.sidebar.checkbox("全选")
    #if all_options: phase = ['PPV3','EP2','EP','PPV2','PPV1','PP1','PPV3','PRE-PPV','EP1','骡车','PPV','MULE','PP2']
    #悬架数据
    @st.cache
    def load_data():
     sql1="""
     select arouse_veh_cnt, easy_aboard_cnt,load_mode_cnt,lifting_mode_cnt,disable_height_cnt,
     round(damping_mode_durs_comfort,0) as damping_mode_durs_comfort,
     round(damping_mode_dis_comfort,0) as damping_mode_dis_comfort,
     round(height_level_durs_low,0) as height_level_durs_low,
     round(height_level_dis_low,0) as height_level_dis_low,
     round(damping_mode_durs_comfort_sport,0) as damping_mode_durs_comfort_sport,
     round(damping_mode_dis_comfort_sport,0) as damping_mode_dis_comfort_sport,
     round(height_level_durs_low_normal,0) as height_level_durs_low_normal,
     round(height_level_dis_low_normal,0) as height_level_dis_low_normal,
     round(damping_mode_durs_comfort_normal,0) as damping_mode_durs_comfort_normal,
     round(damping_mode_dis_comfort_normal,0) as damping_mode_dis_comfort_normal,
     round(height_level_durs_low_high,0) as height_level_durs_low_high,
     round(height_level_dis_low_high,0) as height_level_dis_low_high,
     cast(easy_aboard_cnt/arouse_veh_cnt as decimal(10,4)) as easy_abroad_rate,
     cast(load_mode_cnt/arouse_veh_cnt as decimal(10,4)) as load_mode_rate,
     cast(lifting_mode_cnt/arouse_veh_cnt as decimal(10,4)) as lifting_mode_rate,
     dt,
     cast(dt as date) as dt2
     from ilad_dm.dm_vehicle_asu_stat_di
     order by dt DESC
    """
     pd1=olap_query(sql1)
     return pd1
    pd1 = load_data()
    #便捷上下车日活率
    easy_abroad_rate =f"{pd1['easy_abroad_rate'].values[0]:.2%}"
    easy_abroad_rate_yesterday_difference = f"{pd1['easy_abroad_rate'].values[0] - pd1['easy_abroad_rate'].values[1]:.2%}"
    easy_abroad_rate_yesterday = f"{abs(pd1['easy_abroad_rate'].values[0] - pd1['easy_abroad_rate'].values[1]) :.2%}"
    if pd1['easy_abroad_rate'].values[0] - pd1['easy_abroad_rate'].values[1] >=0:
        easy_abroad_rate_difference = '🔺' + str(easy_abroad_rate_yesterday)
    else:
        easy_abroad_rate_difference = '🔻'+ str(easy_abroad_rate_yesterday)
    #装载模式
    load_mode_rate = f"{pd1['load_mode_rate'].values[0]:.2%}"
    load_mode_rate_yesterday_difference = f"{pd1['load_mode_rate'].values[0] - pd1['load_mode_rate'].values[1] :.2%}"
    load_mode_rate_yesterday = f"{abs(pd1['load_mode_rate'].values[0] - pd1['load_mode_rate'].values[1]) :.2%}"
    if pd1['load_mode_rate'].values[0] - pd1['load_mode_rate'].values[1] >=0:
        load_mode_rate_difference = '🔺'+str(load_mode_rate_yesterday)
    else:
        load_mode_rate_difference = '🔻'+str(load_mode_rate_yesterday)
    #举升模式
    lifting_mode_rate  = f"{pd1['lifting_mode_rate'].values[0]:.2%}"
    lifting_mode_rate_yesterday_difference = f"{pd1['lifting_mode_rate'].values[0] - pd1['lifting_mode_rate'].values[1] :.2%}"
    lifting_mode_rate_yesterday = f"{abs(pd1['lifting_mode_rate'].values[0] - pd1['lifting_mode_rate'].values[1]) :.2%}"
    if pd1['lifting_mode_rate'].values[0] - pd1['lifting_mode_rate'].values[1] >=0:
         lifting_mode_rate_difference = '🔺'+str(lifting_mode_rate_yesterday)
    else:
         lifting_mode_rate_difference = '🔻'+str(lifting_mode_rate_yesterday)


    st.sidebar.markdown("""
         ## 目录
          &emsp;[1.功能监控](#X01_air_suspension_main_menu)\n
         &emsp; &emsp;[1.1便捷上下车功能](#X01_xuanjiadianzitiaojie_bianjieshangxiache_easy_abroad_rate)\n
         &emsp; &emsp;[1.2装载模式功能](#X01_xuanjiadianzitiaojie_zhuangzaimoshi_load_mode_rate)\n                     
         &emsp; &emsp;[1.3举升模式功能](#X01_xuanjiadianzitiaojie_jushengmoshi_lifting_mode_rate)\n
         &emsp; &emsp;[1.4阻尼模式功能](#X01_air_suspension_damp_mode_damp_mode_rate)\n
         &emsp; &emsp;[1.5不同悬架高度等级](#X01_air_suspension_damp_mode_odometer_duration)\n
          &emsp;[2.性能监控](#X01_air_suspension_main_damper)\n
         &emsp; &emsp;[2.1减震器](#X01_air_suspension_main_damper_distribution)\n
         &emsp;&emsp; &emsp;[2.1.1工程性能](#X01_air_suspension_)\n
         &emsp;&emsp; &emsp;[2.1.2耐久性能](#X01_air_suspension_)\n
         &emsp; &emsp;[2.2压缩机](#X01_air_suspension_compressor_rate)\n
         &emsp;&emsp; &emsp;[2.2.1工程性能](#X01_air_suspension_)\n
         &emsp;&emsp; &emsp;[2.2.2耐久性能](#X01_air_suspension_)\n
         &emsp; &emsp;[2.3电磁阀](#X01_xuanjiadianzitiaojie_yucepaiqidiancifashiyongcishu_predicted_exaust_valve_cnt)\n
         &emsp;&emsp; &emsp;[2.3.1工程性能](#X01_air_suspension_)\n
         &emsp;&emsp; &emsp;[2.3.2耐久性能](#X01_air_suspension_)\n
         &emsp; &emsp;[2.4空气弹簧](#X01_air_suspension_)\n
         &emsp;&emsp; &emsp;[2.4.1工程性能](#X01_air_suspension_)\n
         &emsp;&emsp; &emsp;[2.4.2耐久性能](#X01_air_suspension_)\n
          &emsp;[3.质量监控](#X01_air_suspension_quality_monitor)\n
         &emsp; &emsp;[3.1DTC](#X01_air_suspension_DTC)\n
         &emsp; &emsp;[3.2售后工单](#X01_air_suspension_work_order)\n
 """) #目录
    st.title('空气悬架监控仪')
    st.header('指标监控大屏',anchor = 'X01_air_suspension_main_menu')
    col1, col2, col3 = st.columns(3)  #监控大屏
    with col1:
        st.metric("便捷上下车日活率",easy_abroad_rate,easy_abroad_rate_yesterday_difference,delta_color = "inverse")
    with col2:
        st.metric("装载模式日活率",load_mode_rate,load_mode_rate_yesterday_difference,delta_color = "inverse")
    with col3:
        st.metric("举升模式日活率",lifting_mode_rate,lifting_mode_rate_yesterday_difference,delta_color = "inverse")
    with col1:
        st.title("  ")
    st.header("功能指标监控")
    st.subheader("便捷上下车功能",anchor='X01_xuanjiadianzitiaojie_bianjieshangxiache_easy_abroad_rate')
    new_title = '<p style="font-family:sans-serif; color:Black; font-size: 24px;">便捷上下车日活率</p>'
    new_title2 = '<p style="font-family:sans-serif; color:Black; font-size: 14px;">定义:当日便捷上下车模式实际激活车辆数/当日激活车辆数</p>'
    col1, col2, col3  = st.columns((1,3.6,1))
    with col1:
        st.info(' &emsp;&emsp;&emsp;&emsp;**`%s`** &emsp;&emsp;&emsp;&emsp;`%s`'%(easy_abroad_rate,easy_abroad_rate_difference))
    with col2:
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(new_title2, unsafe_allow_html=True)
    yesterday_10 = today + datetime.timedelta(days=-11)
    col1, col2 = st.columns(2)
    with col1:
        start_date_1 = st.date_input('开始日期 （含当日）', yesterday_10)
    with col2:
        end_date_1 = st.date_input('结束日期（含当日）', yesterday)
    if start_date_1 > end_date_1:
        st.error('Error: 开始日期必须在结束日期之前')
    #日期嵌入df
    pd2 = pd1.loc[(pd1['dt2'] >= start_date_1)  & (pd1['dt2']<= end_date_1)]
    pd2['easy_abroad_rate_percent'] = (pd2['easy_abroad_rate']*100).astype(str) + '%'
    #平均日活
    avg_DAU = pd2['easy_abroad_rate'].sum()/pd2['dt'].count()
    avg_DAU_rounded = f"{avg_DAU:.2%}"
    #便捷上下车日活率图
    fig11 = go.Figure()
    fig11 = make_subplots(specs=[[{"secondary_y": True}]])
    # set up plotly figure
    fig11.add_trace(go.Scatter(x=pd2['dt'], y=pd2['easy_aboard_cnt'],
                             mode = 'lines',
                             name= '当日便捷上下车模式实际激活车辆数', line_shape = 'linear',
                             line=dict(color='mediumvioletred',width=2)),secondary_y=True,)
    fig11.add_trace(go.Bar(y=pd2.easy_abroad_rate, x=pd2.dt, text=pd2['easy_abroad_rate_percent'],
                           textposition='outside', name='便捷上下车日活率',
                     marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6),secondary_y=False,
              )
    fig11.add_hline(y= avg_DAU, line_width=3, line_dash="dash", line_color="green", annotation_text="平均日活率:%s"%(avg_DAU_rounded))
    fig11.update_layout(
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
    fig11.update_yaxes(title_text="<b>便捷上下车日活率</b>", secondary_y=False)
    fig11.update_yaxes(title_text="<b>当日便捷上下车模式实际激活车辆数</b>", secondary_y=True)
    fig11.layout.yaxis.tickformat = ',.0%'
    fig11.show()
    st.plotly_chart(fig11,height=600,width=900,use_container_width=True)

    #ETL
    @st.cache
    def load_data():
     sql2="""
     select *, cast(dt as date) as dt2 from
        (select sig_name,times_per_100km, count(*) as times_per_100km_cnt, dt  from
        ilad_dw.dwd_vehicle_signal_x01_bc_f_moving_cycle_di 
        group by dt,sig_name,times_per_100km) a
        order by dt
    """
     pd7=olap_query(sql2)
     return pd7
    pd7 = load_data()

    st.subheader("便捷上下车用户使用频率")
    col1,col2,col3 = st.columns((1,3.6,1))
    with col1:
        start_date_6 = st.date_input('日期', yesterday,key = 12)
    with col2:
        choose =  st.slider('请选择每百公里便捷上下车模式的打开次数区间',
     0, 100, (0,5))


    pd8 = pd7.loc[(pd7['dt2'] == start_date_6) & (pd7['sig_name'] == "SusActuEasyEntMdSts") & (pd7['times_per_100km'] >= choose[0]) & (pd7['times_per_100km'] <= choose[1])]
    SusActuEasyEntMdSts_times = pd8['times_per_100km_cnt'].sum()
    SusActuEasyEntMdSts_total =pd7.loc[(pd7['dt2'] == start_date_6) & (pd7['sig_name'] == "SusActuEasyEntMdSts")]
    SusActuEasyEntMdSts_ratio = f"{ SusActuEasyEntMdSts_times/SusActuEasyEntMdSts_total['times_per_100km_cnt'].sum() :.2%}"
    st.success('在`%s`中，打开`%s`次至`%s`次便捷上下车模式的车数量为`%s`辆，占所有车的`%s`。'%(start_date_6,choose[0],choose[1],SusActuEasyEntMdSts_times,SusActuEasyEntMdSts_ratio))


    #装载模式功能
    st.subheader('装载模式',anchor = 'X01_xuanjiadianzitiaojie_zhuangzaimoshi_load_mode_rate')
    new_title = '<p style="font-family:sans-serif; color:Black; font-size: 24px;">装载模式日活率</p>'
    new_title2 = '<p style="font-family:sans-serif; color:Black; font-size: 14px;">定义:装载模式实际激活车辆数/当日激活车辆数</p>'
    col1, col2, col3  = st.columns((1,3.6,1))
    with col1:
        st.info(' &emsp;&emsp;&emsp;&emsp;**`%s`** &emsp;&emsp;&emsp;&emsp;`%s`'%(load_mode_rate,load_mode_rate_difference))
    with col2:
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(new_title2, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_date_2 = st.date_input('开始日期 （含当日）', yesterday_10,key = 10)
    with col2:
        end_date_2 = st.date_input('结束日期（含当日）', yesterday, key = 10)
    if start_date_2 > end_date_2:
        st.error('Error: 开始日期必须在结束日期之前')
    #日期嵌入df
    pd3 = pd1.loc[(pd1['dt2'] >= start_date_2)  & (pd1['dt2']<= end_date_2)]
    pd3['load_mode_rate_percent'] = (pd3['load_mode_rate']*100).astype(str) + '%'
    #平均日活
    avg_DAU_2 = pd3['load_mode_rate'].sum()/pd3['dt'].count()
    avg_DAU_rounded_2 = f"{avg_DAU_2:.2%}"
    #装载模式日活率图
    fig12 = go.Figure()
    fig12 = make_subplots(specs=[[{"secondary_y": True}]])
    # set up plotly figure
    fig12.add_trace(go.Scatter(x=pd3['dt'], y=pd3['load_mode_cnt'],
                             mode = 'lines',
                             name= '装载模式实际激活车辆数', line_shape = 'linear',
                             line=dict(color='mediumvioletred',width=2)),secondary_y=True,)
    fig12.add_trace(go.Bar(y=pd3.load_mode_rate, x=pd3.dt, text=pd3['load_mode_rate_percent'],
                           textposition='outside', name='装载模式日活率',
                     marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6),secondary_y=False,
              )
    fig12.add_hline(y= avg_DAU_2, line_width=3, line_dash="dash", line_color="green", annotation_text="平均日活率:%s"%(avg_DAU_rounded_2))
    fig12.update_layout(
                       height=400,width=900,
                       showlegend = True,
                       margin=dict(l=0, r=200,b=40,t=20),
                       xaxis_title="<b>日期<b>",
                       legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              )

                                     )
    fig12.update_yaxes(title_text="<b>装载模式日活率</b>", secondary_y=False)
    fig12.update_yaxes(title_text="<b>装载模式实际激活车辆数</b>", secondary_y=True)
    fig12.layout.yaxis.tickformat = ',.0%'
    fig12.show()
    st.plotly_chart(fig12,height=600,width=900,use_container_width=True)

    #装载模式用户使用频率
    st.subheader("装载模式用户使用频率")
    col1,col2,col3 = st.columns((1,3.6,1))
    with col1:
        start_date_7 = st.date_input('日期', yesterday,key = 13)
    with col2:
        choose_2 =  st.slider('请选择每百公里装载模式的打开次数区间',
     0, 100, (0,5))


    pd9 = pd7.loc[(pd7['dt2'] == start_date_7) & (pd7['sig_name'] == "SusActuLdngMdSts") & (pd7['times_per_100km'] >= choose_2[0]) & (pd7['times_per_100km'] <= choose_2[1])]
    SusActuLdngMdSts_times_2 = pd9['times_per_100km_cnt'].sum()
    SusActuLdngMdSts_total_2 =pd7.loc[(pd7['dt2'] == start_date_7) & (pd7['sig_name'] == "SusActuLdngMdSts")]
    SusActuLdngMdSts_ratio_2 = f"{ SusActuLdngMdSts_times_2/SusActuLdngMdSts_total_2['times_per_100km_cnt'].sum() :.2%}"
    st.success('在`%s`中，打开`%s`次至`%s`次装载模式的车数量为`%s`辆，占所有车的`%s`。'%(start_date_7,choose_2[0],choose_2[1],SusActuLdngMdSts_times_2,SusActuLdngMdSts_ratio_2))




    #举升模式日活率
    st.subheader('举升模式',anchor = 'X01_xuanjiadianzitiaojie_jushengmoshi_lifting_mode_rate')
    new_title = '<p style="font-family:sans-serif; color:Black; font-size: 24px;">举升模式日活率</p>'
    new_title2 = '<p style="font-family:sans-serif; color:Black; font-size: 14px;">定义:举升模式实际激活车辆数/当日激活车辆数</p>'
    col1, col2, col3  = st.columns((1,3.6,1))
    with col1:
        st.info(' &emsp;&emsp;&emsp;&emsp;**`%s`** &emsp;&emsp;&emsp;&emsp;`%s`'%(lifting_mode_rate,lifting_mode_rate_difference))
    with col2:
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(new_title2, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_date_3 = st.date_input('开始日期 （含当日）', yesterday_10,key = 11)
    with col2:
        end_date_3 = st.date_input('结束日期（含当日）', yesterday, key = 11)
    if start_date_3 > end_date_3:
        st.error('Error: 开始日期必须在结束日期之前')
    #日期嵌入df
    pd4 = pd1.loc[(pd1['dt2'] >= start_date_3)  & (pd1['dt2']<= end_date_3)]
    pd4['lifting_mode_rate_percent'] = (pd4['lifting_mode_rate']*100).astype(str) + '%'
    #平均日活
    avg_DAU_3 = pd4['lifting_mode_rate'].sum()/pd4['dt'].count()
    avg_DAU_rounded_3 = f"{avg_DAU_3:.2%}"
    #举升模式日活率图
    fig13 = go.Figure()
    fig13 = make_subplots(specs=[[{"secondary_y": True}]])
    # set up plotly figure
    fig13.add_trace(go.Scatter(x=pd4['dt'], y=pd4['lifting_mode_cnt'],
                             mode = 'lines',
                             name= '举升模式实际激活车辆数', line_shape = 'linear',
                             line=dict(color='mediumvioletred',width=2)),secondary_y=True,)
    fig13.add_trace(go.Bar(y=pd4.lifting_mode_rate, x=pd4.dt, text=pd4['lifting_mode_rate_percent'],
                           textposition='outside', name='举升模式日活率',
                     marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6),secondary_y=False,
              )
    fig13.add_hline(y= avg_DAU_3, line_width=3, line_dash="dash", line_color="green", annotation_text="平均日活率:%s"%(avg_DAU_rounded_3))
    fig13.update_layout(
                       height=400,width=900,
                       showlegend = True,
                       margin=dict(l=0, r=200,b=40,t=20),
                       xaxis_title="<b>日期<b>",legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              )
                                     )
    fig13.update_yaxes(title_text="<b>举升模式日活率</b>", secondary_y=False)
    fig13.update_yaxes(title_text="<b>举升模式实际激活车辆数</b>", secondary_y=True)
    fig13.layout.yaxis.tickformat = ',.0%'
    fig13.show()
    st.plotly_chart(fig13,height=600,width=900,use_container_width=True)


    #举升模式用户使用频率
    st.subheader("举升模式用户使用频率")
    col1,col2,col3 = st.columns((1,3.6,1))
    with col1:
        start_date_8 = st.date_input('日期', yesterday,key = 14)
    with col2:
        choose_3 =  st.slider('请选择每百公里装载模式的打开次数区间',
     0, 100, (0,5),key = 1)


    pd10 = pd7.loc[(pd7['dt2'] == start_date_8) & (pd7['sig_name'] == "SusHoistMdSts") & (pd7['times_per_100km'] >= choose_3[0]) & (pd7['times_per_100km'] <= choose_3[1])]
    SusHoistMdSts = pd10['times_per_100km_cnt'].sum()
    SusHoistMdSts_total = pd7.loc[(pd7['dt2'] == start_date_8) & (pd7['sig_name'] == "SusHoistMdSts")]
    SusHoistMdSts_ratio = f"{ SusHoistMdSts/SusHoistMdSts_total['times_per_100km_cnt'].sum() :.2%}"
    st.success('在`%s`中，打开`%s`次至`%s`次举升模式的车数量为`%s`辆，占所有车的`%s`。'%(start_date_8,choose_3[0],choose_3[1],SusHoistMdSts,SusHoistMdSts_ratio))



    #阻尼模式功能
    st.subheader('不同阻尼模式里程与时长',anchor='X01_air_suspension_damp_mode_damp_mode_rate')
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date_4 = st.date_input('开始日期 （含当日）', yesterday_10,key = 1)
    with col2:
        end_date_4 = st.date_input('结束日期（含当日）', today, key = 1)
    with col3:
        damping = st.radio(" ",("不同阻尼模式里程","不同阻尼模式时长"),key = 7)
    if start_date_4 > end_date_4:
        st.error('Error: 开始日期必须在结束日期之前')
     #日期嵌入df
    pd5 = pd1.loc[(pd1['dt2'] >= start_date_4)  & (pd1['dt2']<= end_date_4)]
    if damping == "不同阻尼模式里程" :

        #平均里程
        #阻尼模式里程图

        fig14 = go.Figure()
        fig14.add_trace(go.Bar(
            y=pd5['damping_mode_dis_comfort'],
            x=pd5.dt,
            name='<b>舒适<b>模式里程(公里)',
            orientation='v',text= pd5['damping_mode_dis_comfort'],
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=1.5)
            )
        ))
        fig14.add_trace(go.Bar(
            y=pd5['damping_mode_dis_comfort_sport'],
            x=pd5.dt,
            name='<b>运动<b>模式里程(公里)',
            orientation='v',text = pd5['damping_mode_dis_comfort_sport'],
            marker=dict(
                color='rgba(0, 171, 117, 0.5)',
                line=dict(color='rgba(224, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig14.add_trace(go.Bar(
            y=pd5['damping_mode_dis_comfort_normal'],
            x=pd5.dt,
            name='<b>普通<b>模式里程(公里)',
            orientation='v',text= pd5['damping_mode_dis_comfort_normal'],
            marker=dict(
                color='rgba(58, 71, 80, 0.6)',
                line=dict(color='rgba(0, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig14.update_yaxes(title_text = "<b>里程(公里)<b>", title_standoff=5)
        fig14.update_xaxes(title_text = "<b>日期<b>", title_standoff=5)
        fig14.update_layout(barmode='stack',showlegend = True,
                            margin=dict(l=0, r=200,b=40,t=20),legend=dict(
                                   yanchor="top",
                                   y=0.99,
                                   xanchor="left",
                                   x=0.01
                               ))
        fig14.show()
        st.plotly_chart(fig14,height=600,width=900,use_container_width=True)



    if damping == "不同阻尼模式时长" :
        #平均时长
        #平均里程
        #阻尼模式里程图

        fig14 = go.Figure()
        fig14.add_trace(go.Bar(
            y=pd5['damping_mode_durs_comfort'],
            x=pd5.dt,
            name='<b>舒适<b>模式时长(秒)',
            orientation='v',text= pd5['damping_mode_durs_comfort'],
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=1.5)
            )
        ))
        fig14.add_trace(go.Bar(
            y=pd5['damping_mode_durs_comfort_sport'],
            x=pd5.dt,
            name='<b>运动<b>模式时长(秒)',
            orientation='v',text = pd5['damping_mode_durs_comfort_sport'],
            marker=dict(
                color='rgba(0, 171, 117, 0.5)',
                line=dict(color='rgba(224, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig14.add_trace(go.Bar(
            y=pd5['damping_mode_durs_comfort_normal'],
            x=pd5.dt,
            name='<b>普通<b>模式时长(秒)',
            orientation='v',text= pd5['damping_mode_durs_comfort_normal'],
            marker=dict(
                color='rgba(58, 71, 80, 0.6)',
                line=dict(color='rgba(0, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig14.update_yaxes(title_text = "<b>时长(秒)<b>", title_standoff=5)
        fig14.update_xaxes(title_text = "<b>日期<b>", title_standoff=5)
        fig14.update_layout(barmode='stack',showlegend = True,
                            margin=dict(l=0, r=200,b=40,t=20),legend=dict(
                                   yanchor="top",
                                   y=0.99,
                                   xanchor="left",
                                   x=0.01
                               ))
        fig14.show()
        st.plotly_chart(fig14,height=600,width=900,use_container_width=True)









    #不同悬架高度等级
    st.subheader('不同悬架高度里程与时长',anchor='X01_air_suspension_damp_mode_odometer_duration')
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date_5 = st.date_input('开始日期 （含当日）', yesterday_10,key = 5)
    with col2:
        end_date_5 = st.date_input('结束日期（含当日）', today, key = 5)
    with col3:
        height = st.radio(" ",("不同悬架高度里程","不同悬架高度时长"),key = 5)
    if start_date_5 > end_date_5:
        st.error('Error: 开始日期必须在结束日期之前')
    #日期嵌入df
    pd6 = pd1.loc[(pd1['dt2'] >= start_date_4)  & (pd1['dt2']<= end_date_4)]
    if height == "不同悬架高度里程" :

        #平均里程
        #阻尼模式里程图

        fig15 = go.Figure()
        fig15.add_trace(go.Bar(
            y=pd6['height_level_dis_low'],
            x=pd6.dt,
            name='<b>低<b>悬架高度总里程（公里）',
            orientation='v',text= pd6['height_level_dis_low'],
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=1.5)
            )
        ))
        fig15.add_trace(go.Bar(
            y=pd6['height_level_dis_low_normal'],
            x=pd6.dt,
            name='<b>中<b>悬架高度总里程(公里)',
            orientation='v',text = pd6['height_level_dis_low_normal'],
            marker=dict(
                color='rgba(0, 171, 117, 0.5)',
                line=dict(color='rgba(224, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig15.add_trace(go.Bar(
            y=pd6['height_level_dis_low_high'],
            x=pd6.dt,
            name='<b>高<b>悬架高度总里程（公里）',
            orientation='v',text= pd6['height_level_dis_low_high'],
            marker=dict(
                color='rgba(58, 71, 80, 0.6)',
                line=dict(color='rgba(0, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig15.update_yaxes(title_text = "<b>里程(公里)<b>", title_standoff=5)
        fig15.update_xaxes(title_text = "<b>日期<b>", title_standoff=5)
        fig15.update_layout(barmode='stack',showlegend = True,
                            margin=dict(l=0, r=200,b=40,t=20),legend=dict(
                                   yanchor="top",
                                   y=0.99,
                                   xanchor="left",
                                   x=0.01
                               ))
        fig15.show()
        st.plotly_chart(fig15,height=600,width=900,use_container_width=True)

    if height == "不同悬架高度时长" :
        #平均时长
        #阻尼模式里程图

        fig15 = go.Figure()
        fig15.add_trace(go.Bar(
            y=pd6['height_level_durs_low'],
            x=pd6.dt,
            name='<b>低<b>悬架高度总时长（秒）',
            orientation='v',text= pd6['height_level_durs_low'],
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                line=dict(color='rgba(246, 78, 139, 1.0)', width=1.5)
            )
        ))
        fig15.add_trace(go.Bar(
            y=pd6['height_level_durs_low_normal'],
            x=pd6.dt,
            name='<b>中<b>悬架高度总时长(秒)',
            orientation='v',text = pd6['height_level_durs_low_normal'],
            marker=dict(
                color='rgba(0, 171, 117, 0.5)',
                line=dict(color='rgba(224, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig15.add_trace(go.Bar(
            y=pd6['height_level_durs_low_high'],
            x=pd6.dt,
            name='<b>高<b>悬架高度总时长（秒）',
            orientation='v',text= pd6['height_level_durs_low_high'],
            marker=dict(
                color='rgba(58, 71, 80, 0.6)',
                line=dict(color='rgba(0, 100, 255, 0.5)', width=1.5)
            )
        ))
        fig15.update_yaxes(title_text = "<b>时长(秒)<b>", title_standoff=5)
        fig15.update_xaxes(title_text = "<b>日期<b>", title_standoff=5)

        fig15.update_layout(barmode='stack',showlegend = True,
                            margin=dict(l=0, r=200,b=40,t=20), legend=dict(
                                   yanchor="top",
                                   y=0.99,
                                   xanchor="left",
                                   x=0.01
                               ))
        fig15.show()
        st.plotly_chart(fig15,height=600,width=900,use_container_width=True)









    #减震器单车分析
    st.subheader('减震器监控',anchor='X01_air_suspension_main_damper_distribution')
    col1, col2, col3, col4 = st.columns((1,1,1,1.6))
    with col1:
        vin2 = st.text_input('请选择vin')
    with col2:
        start_date_2 = st.date_input('开始日期 （含当日）', yesterday_10,key = 6)
    with col3:
        end_date_2 = st.date_input('结束日期（含当日）', today, key = 6)
    with col4:
        loc=st.radio("请选择减震器位置：",("FL","FR","RL","RR"),key = 6)
    with col1:
        all_vin = st.checkbox('全辆车' , value = True)
        # 电流，速度 map出阻尼力
    #x为电流 y为速度 z为阻尼力
    #front
    x_cur = [0,0.2,0.4,0.6,0.8,1,1.2,1.4,1.6]
    y_vel=[-1.571, -1.048,-0.524,-0.393, -0.262, -0.131, -0.052,-0.026,0,
                                                  0.026,0.052, 0.131, 0.262, 0.393, 0.524,1.048, 1.571]
    #Front Dampr Force
    z = np.array([(1520,1545,1615,1780,2020,2395,2825,3255,3650),
                  (1000,1020,1070,1200,1455	,1770,2200,2590	,3025),
                  (500,520,535,615,845,1155	,1580,1990,2395),
                  (380,390,405,465,685,1000,1415,1815,2210),
                  (240,250,265,315,520,850,1260,1655,2055),
                  (145,155,170,185,375,705,1060	,1285,1495),
                  (90,95,105,115,260,415,500,530,565),
                  (85,90,95,100,155,215,225,235,245),
                  (0,0.00001,0.00002,0.00003,0.00004,0.00005,0.00006,0.00007,0.00008),
                  (-90,-100,-105,-130,-325,	-460,-480,-500,	-540),
                  (-135	,-140,-145,-190,-560,-1005,	-1325,-1450,-1490),
                  (-300,-305,-330,-415,-865	,-1575,-2470,-3350,-3960),
                  (-675,-690,-730,-885,-1395,-2070,-2990,-3830,-4470),
                  (-960	,-980,-1060,-1290,-1820,-2495,-3465,-4190,-4795),
                  (-1240,-1265,-1375,-1670,-2215,-2930,-3825,-4495,-5115),
                  (-2255,-2315,-2535,-2950,-3555,-4150,-4815,-5390,-6050),
                  (-3300,-3375,-3625,-4020,-4575,-5145,	-5785,-6330,-7005)])
    #Rear Dampr Force
    z_rear = np.array([(1335,1360,1440,1615	,1905,2270,2675,3100,3590),
                       (990,1020,1070,1225,1465,1855,2280,2690,3100),
                       (500,520,540,635,880,1220,1655,2060,2515),
                       (380,395,410,480,725,1060,1500,1895,2345),
                       (250,260,270,320,560,900,1330,1745,2175),
                       (155,165,175,190,420,745,1050,1270,1530),
                       (95,100,110,120,270,405,480,505,545),
                       (85,90,95,100,155,190,200,210,225),
                       (0,0.00001,0.00002,0.00003,0.00004,0.00005,0.00006,0.00007,0.00008),
                       (-90,-95,-100,-125,-425,-645,-665,-690,-730),
                       (-135,-140,-145,-185,-695,-1235,	-1610,-1970,-2140),
                       (-290,-295,-320,	-445,-975,-1720,-2695,-3585,-4035),
                       (-630,-645,-705,-915,-1470,	-2225,-3205,-3985,-4600),
                       (-900,-925,-1020,-1300,-1855,-2645,-3610,-4280,	-4895),
                       (-1150,-1180,-1310,	-1645,-2240,-3055,-3905,-4545,-5165),
                       (-1960,-2030,-2270,	-2710,-3350,-4125,-4750,-5395,-6065),
                       (-2975,-3060,-3300,	-3790,-4370,-4935,-5525,-6200,	-6885)])
    f = interp2d(x_cur,y_vel,z,kind = 'linear',fill_value=None)
    f_rear = interp2d(x_cur,y_vel,z_rear,kind = 'linear',fill_value=None)
    @st.cache
    def load_data():
        data = pd.read_csv(f'{csv_path}/cur_vel.csv')
        return data
    data2 = load_data()
    #左前减震器数据
    ff_FL=[f(x,y)[0] for x,y in zip(data2.m_DmpCtl_damprCur_FL_A,data2.m_DmpCtl_i_suspVel_FL_mps)]
    #右前减震器数据
    ff_FR=[f(x,y)[0] for x,y in zip(data2.m_DmpCtl_damprCur_FR_A,data2.m_DmpCtl_i_suspVel_FR_mps)]
    #左后减震器数据
    ff_RL=[f_rear(x,y)[0] for x,y in zip(data2.m_DmpCtl_damprCur_RL_A,data2.m_DmpCtl_i_suspVel_RL_mps)]
    #右后减震器数据
    ff_RR=[f_rear(x,y)[0] for x,y in zip(data2.m_DmpCtl_damprCur_RR_A,data2.m_DmpCtl_i_suspVel_RR_mps)]



    data3 = pd.DataFrame (ff_FL, columns = ['N'])
    data5 = pd.DataFrame (ff_FR, columns = ['N'])
    data7 = pd.DataFrame (ff_RL, columns = ['N'])
    data9 = pd.DataFrame (ff_RR, columns = ['N'])
    #新df，x1为速度,x2为阻尼力，x3为电流
    data4 = pd.concat([data2['m_DmpCtl_i_suspVel_FL_mps'], data3['N'], data2['m_DmpCtl_damprCur_FL_A']], axis=1, keys=['m_DmpCtl_i_suspVel_FL_mps', 'DampForce','m_DmpCtl_damprCur_FL_A'])
    data6 = pd.concat([data2['m_DmpCtl_i_suspVel_FR_mps'], data5['N'], data2['m_DmpCtl_damprCur_FR_A']], axis=1, keys=['m_DmpCtl_i_suspVel_FR_mps', 'DampForce','m_DmpCtl_damprCur_FR_A'])
    data8 = pd.concat([data2['m_DmpCtl_i_suspVel_RL_mps'], data7['N'], data2['m_DmpCtl_damprCur_RL_A']], axis=1, keys=['m_DmpCtl_i_suspVel_RL_mps', 'DampForce','m_DmpCtl_damprCur_RL_A'])
    data10 = pd.concat([data2['m_DmpCtl_i_suspVel_RR_mps'], data9['N'], data2['m_DmpCtl_damprCur_RR_A']], axis=1, keys=['m_DmpCtl_i_suspVel_RR_mps', 'DampForce','m_DmpCtl_damprCur_RR_A'])




        #ZF 电流与阻尼力
    df2 = pd.DataFrame(dict(
            x = [-1.571,-1.048,-0.524,-0.393,-0.262,-0.131,-0.052,-0.026,0,0.026,
                 0.052,0.131,0.262,0.393,0.524,1.048,1.571],
     #ZF 电流与阻尼力  #front soft
            y1 = [1520,1000,500,380,240,145,90,85,0,-90,-135,-300,-675,-960,
                  -1240,-2255,-3300],
       #front hard
            y2 = [3650,3025,2395,2210,2055,1495,565,245,0.00008,-540,-1490,-3960,
                  -4470,-4795,-5115,-6050,-7005],
       #rear soft
            y3 = [1335,990,500,380,250,155,95,85,0,-90,-135,-290,-630,-900,-1150,
                  -1960,-2975],
       #rear hard
            y4 = [3590,3100,2515,2345,2175,1530,545,225,0.00008,-730,-2140,-4035,
                  -4600, -4895, -5165, -6065, -6885]
            ))
    #TN 电流与阻尼力
    df3 = pd.DataFrame(dict(
            x = [-1.047,-0.524,-0.393,-0.262,-0.131,-0.052,0,
                 0.052,0.131,0.262,0.393,0.524,1.047],
     #TN 电流与阻尼力  #front soft
            y1 = [1146,573,442,319,202,130,0,-145,-252,-446,-644,-838,-1799],
       #front hard
            y2 = [3596,2871,2502,2047,1200,327,0,-871,-2772,-3173,-3497,-3756,
                  -4602],
       #rear soft
            y3 = [1131,555,430,315,207,136,0,-148,-247,-413,-604,-771,-1679],
       #rear hard
            y4 = [3718,2961,2451,2053,1348,360,0,-929,-2658,-3032,-3338,-3615,
                -4463]
            ))
    if all_vin:
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
                                    name = '全辆车',
                                    marker=dict(
                                        size=3,
                                        color=data4.m_DmpCtl_damprCur_FL_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig5.update_yaxes(title_text = "<b>阻尼力(N)<b>", title_standoff=5,side = "left")
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
                               xaxis_title="<b>减震器速度(m/s)<b>"
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
                                    name = '全辆车',
                                    marker=dict(
                                        size=3,
                                        color=data6.m_DmpCtl_damprCur_FR_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig6.update_yaxes(title_text = "<b>阻尼力(N)<b>", title_standoff=5)
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
                               xaxis_title="<b>减震器速度(m/s)<b>"
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
                                    name = '全辆车',
                                    marker=dict(
                                        size=3,
                                        color=data8.m_DmpCtl_damprCur_RL_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig7.update_yaxes(title_text = "<b>阻尼力(N)<b>", title_standoff=5)
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
                               xaxis_title="<b>减震器速度(m/s)<b>"
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
                                    name = '全辆车',
                                    marker=dict(
                                        size=3,
                                        color=data10.m_DmpCtl_damprCur_RR_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig8.update_yaxes(title_text = "<b>阻尼力(N)<b>", title_standoff=5)
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
                               xaxis_title="<b>减震器速度(m/s)<b>"
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
                                    name = '全辆车',
                                    marker=dict(
                                        size=3,
                                        color=data4.m_DmpCtl_damprCur_FL_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig9.update_yaxes(title_text = "<b>阻尼力(N)<b>", title_standoff=5)
            fig9.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = False,
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>减震器速度(m/s)<b>"
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
                                    name = '全辆车',
                                    marker=dict(
                                        size=3,
                                        color=data6.m_DmpCtl_damprCur_FR_A, #set color equal to a variable
                                        colorscale='Viridis', # one of plotly colorscales
                                        showscale=True,reversescale=True
                                        ))
                                    )
            fig10.update_yaxes(title_text = "<b>阻尼力(N)<b>", title_standoff=5)
            fig10.update_layout(xaxis_range=[-1.8,1.8],
                               yaxis_range=[-5000,3000],
                               height=500,width=800,
                               showlegend = False,
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>减震器速度(m/s)<b>"
                                             )
            fig10.show()
            st.plotly_chart(fig10,height=600,width=900,use_container_width=True)
    with st.expander("上图说明："):
        st.write('X轴为减震器速度(m/s)，Y轴为阻尼力（N），而上方的两条线为X01减震器的设计阈值。而上图反映出了每次使用减震器在阈值范围内的分布情况。\n\n **颜色越深电流越大。**')





    #预计16万公里电磁阀打开次数与时长
    #ETL
    @st.cache
    def load_data():
     sql8="""
     select round(predicted_total_susactuvlvblkrlsts,0) as predicted_total_susactuvlvblkrlsts,
        round(predicted_total_susactuvlvblkrrsts,0) as predicted_total_susactuvlvblkrrsts,
        round(predicted_total_susactuvlvblkfrsts,0) as predicted_total_susactuvlvblkfrsts,
        round(predicted_total_susactuvlvblkflsts,0) as predicted_total_susactuvlvblkflsts,
        round(predicted_total_susactucomprelaysts/3600,0) as predicted_total_susactucomprelaysts,
        round(predicted_total_susactuvlvblkexhsts,0) as predicted_total_susactuvlvblkexhsts,
        round(predicted_total_susactuvlvblkrsvrsts,0) as predicted_total_susactuvlvblkrsvrsts,
        cast(dt as date) as dt2, dt
         from ilad_dm.dwd_vehicle_signal_x_asu_arouse_stat_final_di
         order by dt desc
    """
     pd19=olap_query(sql8)
     return pd19
    pd19 = load_data()
    #曲线图数据
    @st.cache
    def load_data():
     sql9="""
     select * from ilad_dm.dwd_vehicle_signal_x_asu_arouse_stat_unpredicted_di
    order by dt asc
    """
     pd22=olap_query(sql9)
     return pd22
    pd22 = load_data()
    #压缩机耐久
    predicted_total_susactucomprelaysts = pd19['predicted_total_susactucomprelaysts'].values[0]
    predicted_total_susactucomprelaysts = int(predicted_total_susactucomprelaysts)
    predicted_total_susactucomprelaysts_difference =  pd19['predicted_total_susactucomprelaysts'].values[0] -  pd19['predicted_total_susactucomprelaysts'].values[1]
    predicted_total_susactucomprelaysts_difference = int(predicted_total_susactucomprelaysts_difference)
    if pd19['predicted_total_susactucomprelaysts'].values[0] - pd19['predicted_total_susactucomprelaysts'].values[1] >=0:
         predicted_total_susactucomprelaysts_difference = '🔺'+str(predicted_total_susactucomprelaysts_difference)
    else:
         predicted_total_susactucomprelaysts_difference = '🔻'+str(predicted_total_susactucomprelaysts_difference)
    #压缩机耐久性能
    st.subheader('压缩机耐久性能',anchor = 'X01_air_suspension_compressor_rate')
    new_title7 = '<p style="font-family:sans-serif; color:Black; font-size: 24px;">预测压缩机工作时长</p>'
    new_title8 = '<p style="font-family:sans-serif; color:Black; font-size: 13.8px;">定义:基于全量车数据预测车辆行驶16万公里时压缩机工作时长</p>'
    col1, col2, col3  = st.columns((1,2.5,1))
    with col1:
        st.info('&emsp;&emsp;&emsp;**`%s`** &emsp;&emsp;&emsp;&emsp;&emsp;`%s`'%(predicted_total_susactucomprelaysts,predicted_total_susactucomprelaysts_difference))
    with col2:
        st.markdown(new_title7, unsafe_allow_html=True)
        st.markdown(new_title8, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        start_date_11 = st.date_input('开始日期 （含当日）', yesterday_10,key = 3)
    with col2:
        end_date_11 = st.date_input('结束日期（含当日）', today, key = 3)
    if start_date_11 > end_date_11:
        st.error('Error: 开始日期必须在结束日期之前')
    #嵌入df
    pd20 = pd19.loc[(pd19['dt2'] >= start_date_11)  & (pd19['dt2']<= end_date_11)]
    #预测压缩机工作时长
    avg_predicted_total_susactucomprelaysts = pd20['predicted_total_susactucomprelaysts'].sum()/pd20['dt'].count()
    avg_predicted_total_susactucomprelaysts_rounded = int(avg_predicted_total_susactucomprelaysts)
    fig11 = go.Figure()
    fig11.add_trace(go.Bar(
        y=pd20['predicted_total_susactucomprelaysts'],
        x=pd20.dt,
        name='<b>压缩机耐久性能<b>',
        orientation='v',text= pd20['predicted_total_susactucomprelaysts'],
        marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
     marker_line_width=1.5, opacity=0.6

    ))
    fig11.add_hline(y= avg_predicted_total_susactucomprelaysts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均压缩机预测工作时长:%s"%(avg_predicted_total_susactucomprelaysts_rounded))
    fig11.update_yaxes(title_text = "<b>16万公里压缩机预测工作时长<b>", title_standoff=5)
    fig11.update_layout(
                       height=500,width=800,
                       showlegend = False,
                       margin=dict(l=0, r=200,b=40,t=20),
                       xaxis_title="<b>日期<b>"
                                     )
    fig11.show()
    st.plotly_chart(fig11,height=600,width=900,use_container_width=True)



    # #random data
    # data8={'total_odometer':[1000,1200,1300,1400],'total_relay_durs':[22,23,25,27],
    #  'total_relay_cnt':[10,11,13,15],
    #  'dt':['2022-06-23','2022-06-24','2022-06-25','2022-06-26']}
    # df3=pd.DataFrame(data8)

    # dt_list= df3['dt'].values.tolist()
    # df3.insert(4,'m',[0]*len(dt_list),True)
    # df3.insert(4,'b',[0]*len(dt_list),True)
    # df3.insert(4,'total_odo_before',[0]*len(dt_list),True)
    # df3.insert(4,'total_dur_before',[0]*len(dt_list),True)
    # for i, l in enumerate(dt_list):
    #     m, b = np.polyfit(df3[df3['dt']==l]['total_odometer'], df3[df3['dt']==l]['total_relay_durs'], 1)

    #     df3.loc[i,'m'] = m
    #     df3.loc[i,'b'] = b
    # mm= df3['m'].values.tolist()
    # bb= df3['b'].values.tolist()
    # for i, l in enumerate(dt_list):
    #     df3.loc[i,'total_odo_before'] = mm[i]
    #     df3.loc[i,'total_dur_before'] = bb[i]

    #排气电磁阀
    predicted_total_susactuvlvblkexhsts = pd19['predicted_total_susactuvlvblkexhsts'].values[0]
    predicted_total_susactuvlvblkexhsts = int(predicted_total_susactuvlvblkexhsts)
    predicted_total_susactuvlvblkexhsts_difference =  pd19['predicted_total_susactuvlvblkexhsts'].values[0] -  pd19['predicted_total_susactuvlvblkexhsts'].values[1]
    predicted_total_susactuvlvblkexhsts_difference = int(predicted_total_susactuvlvblkexhsts_difference)
    if pd19['predicted_total_susactuvlvblkexhsts'].values[0] - pd19['predicted_total_susactuvlvblkexhsts'].values[1] >=0:
         predicted_total_susactuvlvblkexhsts_difference_1 = '🔺'+str(predicted_total_susactuvlvblkexhsts_difference)
    else:
         predicted_total_susactuvlvblkexhsts_difference_1 = '🔻'+str(predicted_total_susactuvlvblkexhsts_difference)

    #预测左前电磁阀打开次数
    predicted_total_susactuvlvblkflsts = pd19['predicted_total_susactuvlvblkflsts'].values[0]
    predicted_total_susactuvlvblkflsts = int(predicted_total_susactuvlvblkflsts)
    predicted_total_susactuvlvblkflsts_difference =  pd19['predicted_total_susactuvlvblkflsts'].values[0] -  pd19['predicted_total_susactuvlvblkflsts'].values[1]
    predicted_total_susactuvlvblkflsts_difference = int(predicted_total_susactuvlvblkflsts_difference)
    #预测右前电磁阀打开次数
    predicted_total_susactuvlvblkfrsts = pd19['predicted_total_susactuvlvblkfrsts'].values[0]
    predicted_total_susactuvlvblkfrsts = int(predicted_total_susactuvlvblkfrsts)
    predicted_total_susactuvlvblkfrsts_difference =  pd19['predicted_total_susactuvlvblkfrsts'].values[0] -  pd19['predicted_total_susactuvlvblkfrsts'].values[1]
    predicted_total_susactuvlvblkfrsts_difference = int(predicted_total_susactuvlvblkfrsts_difference)
    #预测左后电磁阀打开次数
    predicted_total_susactuvlvblkrlsts = pd19['predicted_total_susactuvlvblkrlsts'].values[0]
    predicted_total_susactuvlvblkrlsts = int(predicted_total_susactuvlvblkrlsts)
    predicted_total_susactuvlvblkrlsts_difference =  pd19['predicted_total_susactuvlvblkrlsts'].values[0] -  pd19['predicted_total_susactuvlvblkrlsts'].values[1]
    predicted_total_susactuvlvblkrlsts_difference = int(predicted_total_susactuvlvblkrlsts_difference)
    #预测右后电磁阀打开次数
    predicted_total_susactuvlvblkrrsts = pd19['predicted_total_susactuvlvblkrrsts'].values[0]
    predicted_total_susactuvlvblkrrsts = int(predicted_total_susactuvlvblkrrsts)
    predicted_total_susactuvlvblkrrsts_difference =  pd19['predicted_total_susactuvlvblkrrsts'].values[0] -  pd19['predicted_total_susactuvlvblkrrsts'].values[1]
    predicted_total_susactuvlvblkrrsts_difference = int(predicted_total_susactuvlvblkrrsts_difference)
    #预测储气罐电磁阀打开次数
    predicted_total_susactuvlvblkrsvrsts = pd19['predicted_total_susactuvlvblkrsvrsts'].values[0]
    predicted_total_susactuvlvblkrsvrsts = int(predicted_total_susactuvlvblkrsvrsts)
    predicted_total_susactuvlvblkrsvrsts_difference =  pd19['predicted_total_susactuvlvblkrsvrsts'].values[0] -  pd19['predicted_total_susactuvlvblkrsvrsts'].values[1]
    predicted_total_susactuvlvblkrsvrsts_difference = int(predicted_total_susactuvlvblkrsvrsts_difference)

    st.header('电磁阀指标监控大屏',anchor = '电磁阀')
    col1, col2, col3 = st.columns(3)  #电磁阀耐久性能
    with col1:
        st.metric("预测排气电磁阀打开次数",predicted_total_susactuvlvblkexhsts,predicted_total_susactuvlvblkexhsts_difference,delta_color = "inverse")
    with col2:
        st.metric("预测左前电磁阀打开次数",predicted_total_susactuvlvblkflsts,predicted_total_susactuvlvblkflsts_difference,delta_color = "inverse")
    with col3:
        st.metric("预测右前电磁阀打开次数",predicted_total_susactuvlvblkfrsts,predicted_total_susactuvlvblkfrsts_difference,delta_color = "inverse")
    with col1:
        st.metric("预测储气罐电磁阀打开次数",predicted_total_susactuvlvblkrsvrsts,predicted_total_susactuvlvblkrsvrsts_difference,delta_color = "inverse")
    with col2:
        st.metric("预测左后电磁阀打开次数",predicted_total_susactuvlvblkrlsts,predicted_total_susactuvlvblkrlsts_difference,delta_color = "inverse")
    with col3:
        st.metric("预测右后电磁阀打开次数",predicted_total_susactuvlvblkrrsts,predicted_total_susactuvlvblkrrsts_difference,delta_color = "inverse")
    with col1:
        st.title("  ")
    #电磁阀耐久性能指标监控
    st.subheader("电磁阀耐久性能指标监控",anchor='X01_xuanjiadianzitiaojie_yucepaiqidiancifashiyongcishu_predicted_exaust_valve_cnt')
    col1, col2 = st.columns(2)
    with col1:
        expander2=st.expander("点击展开电磁阀预测原理")
        expander2.write("""
                        根据全辆车过往驾驶与电磁阀使用记录，预测当16万公里时，全辆车的电磁阀平均使用情况。
                        所有电磁阀设计值均为不超过16万公里5万次。
                        """)
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        start_date_12 = st.date_input('开始日期 （含当日）', yesterday_10,key = 4)
    with col2:
        end_date_12 = st.date_input('结束日期（含当日）', today, key = 4)
    with col3:
        open_cnt = st.selectbox('请选择电磁阀', ('左前电磁阀','右前电磁阀','左后电磁阀','右后电磁阀','排气电磁阀','储气罐电磁阀'))
    with col4:
        show_curve = st.radio("是否点开曲线图",("显示","不显示"),key = 7)
    if start_date_12 > end_date_12:
        st.error('Error: 开始日期必须在结束日期之前')
    #嵌入df
    pd21 = pd19.loc[(pd19['dt2'] >= start_date_12)  & (pd19['dt2']<= end_date_12)]
    if open_cnt == '排气电磁阀':
        st.subheader('预测排气电磁阀打开次数')
        #电磁阀耐久性能指标监控
        avg_predicted_total_susactuvlvblkexhsts = pd21['predicted_total_susactuvlvblkexhsts'].sum()/pd21['dt'].count()
        avg_predicted_total_susactuvlvblkexhsts_rounded = int(avg_predicted_total_susactuvlvblkexhsts)
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            y=pd21['predicted_total_susactuvlvblkexhsts'],
            x=pd21.dt,
            name='<b>预测排气电磁阀打开次数<b>',
            orientation='v',text= pd21['predicted_total_susactuvlvblkexhsts'],
            marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
         marker_line_width=1.5, opacity=0.6

        ))
        fig12.add_hline(y= avg_predicted_total_susactuvlvblkexhsts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均电磁阀预测耐久:%s"%(avg_predicted_total_susactuvlvblkexhsts_rounded))
        fig12.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
        fig12.update_layout(
                           height=500,width=800,
                           showlegend = False,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>"
                                         )
        fig12.show()
        st.plotly_chart(fig12,height=600,width=900,use_container_width=True)
        if show_curve == '显示':
            x1=0
            x2=180000
            x = np.arange(x1,x2)
            m, b = np.polyfit( pd22['total_daily_odometer'],pd22['total_susactuvlvblkexhsts'], 1)
            colx1= b/(0.3125-m)
            coly1= colx1 * 0.3125
            colx1_round = round(colx1,3)
            coly1_round = round(coly1,3)
            m_round = round(m,2)
            b_round = round(b,2)
            times = m * 160000 + b
            times_round = round(times, 2)
            difference = abs((times - 50000)/times)
            ratio = f"{difference:.2%}"
            if times <= 50000:
                high = '低'
            else:
                high = '高'
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=m*x+b,
                                      mode = 'lines',
                                      name= '实际值预测模型',
                                      line=dict(color='royalblue',width=3)))
            fig2.add_trace(go.Scatter(x=pd22['total_daily_odometer'],y=pd22['total_susactuvlvblkexhsts'],
                                      mode = 'markers',
                                      name = '实际值',
                                      line = dict(color='mediumvioletred',width=4)
                                      ))
            fig2.add_trace(go.Scatter(y=0.3125 * x,
                                      mode = 'lines',
                                      name= '设计值',
                                      line=dict(color='green',width=3, dash = 'dash')))
            fig2.add_hline(y= 50000, line_width=3, line_dash="dot", line_color="green")
            fig2.add_hline(y= times_round, line_width=3, line_dash="dot", line_color="green")
            fig2.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
            fig2.update_layout(xaxis_range=[0,pd22['total_daily_odometer'].max()+40],yaxis_range=[0,pd22['total_susactuvlvblkexhsts'].max()+20],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>里程<b>"
                                             )

            fig2.show()
            st.plotly_chart(fig2,height=500,width=800,use_container_width=True)
            st.success('根据全辆车的数据，当里程达到16万公里时，排气电磁阀使用为`%s`次，比标定制5万次`%s`了`%s`'%(times_round,high,ratio))




    if open_cnt == '左前电磁阀':
        st.subheader('预测左前电磁阀打开次数')
        #预测左前电磁阀打开次数
        avg_predicted_total_susactuvlvblkflsts = pd21['predicted_total_susactuvlvblkflsts'].sum()/pd21['dt'].count()
        predicted_total_susactuvlvblkflsts_rounded = int(avg_predicted_total_susactuvlvblkflsts)
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            y=pd21['predicted_total_susactuvlvblkflsts'],
            x=pd21.dt,
            name='<b>预测左前电磁阀打开次数<b>',
            orientation='v',text= pd21['predicted_total_susactuvlvblkflsts'],
            marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
         marker_line_width=1.5, opacity=0.6

        ))
        fig12.add_hline(y= avg_predicted_total_susactuvlvblkflsts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均电磁阀预测耐久:%s"%(predicted_total_susactuvlvblkflsts_rounded))
        fig12.update_yaxes(title_text = "<b>预测左前电磁阀打开次数<b>", title_standoff=5)
        fig12.update_layout(
                           height=500,width=800,
                           showlegend = False,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>"
                                         )
        fig12.show()
        st.plotly_chart(fig12,height=600,width=900,use_container_width=True)
        if show_curve == '显示':
            x1=0
            x2=180000
            x = np.arange(x1,x2)
            m, b = np.polyfit( pd22['total_daily_odometer'],pd22['total_susactuvlvblkflsts'], 1)
            colx1= b/(0.3125-m)
            coly1= colx1 * 0.3125
            colx1_round = round(colx1,3)
            coly1_round = round(coly1,3)
            m_round = round(m,2)
            b_round = round(b,2)
            times = m * 160000 + b
            times_round = round(times, 2)
            difference = abs((times - 50000)/times)
            ratio = f"{difference:.2%}"
            if times <= 50000:
                high = '低'
            else:
                high = '高'
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=m*x+b,
                                      mode = 'lines',
                                      name= '实际值预测模型',
                                      line=dict(color='royalblue',width=3)))
            fig2.add_trace(go.Scatter(x=pd22['total_daily_odometer'],y=pd22['total_susactuvlvblkflsts'],
                                      mode = 'markers',
                                      name = '实际值',
                                      line = dict(color='mediumvioletred',width=4)
                                      ))
            fig2.add_trace(go.Scatter(y=0.3125 * x,
                                      mode = 'lines',
                                      name= '设计值',
                                      line=dict(color='green',width=3, dash = 'dash')))
            fig2.add_hline(y= 50000, line_width=3, line_dash="dot", line_color="green")
            fig2.add_hline(y= times_round, line_width=3, line_dash="dot", line_color="green")
            fig2.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
            fig2.update_layout(xaxis_range=[0,pd22['total_daily_odometer'].max()+40],yaxis_range=[0,pd22['total_susactuvlvblkflsts'].max()+20],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>里程<b>"
                                             )

            fig2.show()
            st.plotly_chart(fig2,height=500,width=800,use_container_width=True)
            st.success('根据全辆车的数据，当里程达到16万公里时，排气电磁阀使用为`%s`次，比标定制5万次`%s`了`%s`'%(times_round,high,ratio))

    if open_cnt == '右前电磁阀':
        st.subheader('预测右前电磁阀打开次数')
        #预测左前电磁阀打开次数
        avg_predicted_total_susactuvlvblkfrsts = pd21['predicted_total_susactuvlvblkfrsts'].sum()/pd21['dt'].count()
        predicted_total_susactuvlvblkfrsts_rounded = int(avg_predicted_total_susactuvlvblkfrsts)
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            y=pd21['predicted_total_susactuvlvblkfrsts'],
            x=pd21.dt,
            name='<b>预测右前电磁阀打开次数<b>',
            orientation='v',text= pd21['predicted_total_susactuvlvblkfrsts'],
            marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
         marker_line_width=1.5, opacity=0.6

        ))
        fig12.add_hline(y= avg_predicted_total_susactuvlvblkfrsts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均电磁阀预测耐久:%s"%(predicted_total_susactuvlvblkfrsts_rounded))
        fig12.update_yaxes(title_text = "<b>预测右前电磁阀打开次数<b>", title_standoff=5)
        fig12.update_layout(
                           height=500,width=800,
                           showlegend = False,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>"
                                         )
        fig12.show()
        st.plotly_chart(fig12,height=600,width=900,use_container_width=True)
        if show_curve == '显示':
            x1=0
            x2=180000
            x = np.arange(x1,x2)
            m, b = np.polyfit( pd22['total_daily_odometer'],pd22['total_susactuvlvblkfrsts'], 1)
            colx1= b/(0.3125-m)
            coly1= colx1 * 0.3125
            colx1_round = round(colx1,3)
            coly1_round = round(coly1,3)
            m_round = round(m,2)
            b_round = round(b,2)
            times = m * 160000 + b
            times_round = round(times, 2)
            difference = abs((times - 50000)/times)
            ratio = f"{difference:.2%}"
            if times <= 50000:
                high = '低'
            else:
                high = '高'
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=m*x+b,
                                      mode = 'lines',
                                      name= '实际值预测模型',
                                      line=dict(color='royalblue',width=3)))
            fig2.add_trace(go.Scatter(x=pd22['total_daily_odometer'],y=pd22['total_susactuvlvblkfrsts'],
                                      mode = 'markers',
                                      name = '实际值',
                                      line = dict(color='mediumvioletred',width=4)
                                      ))
            fig2.add_trace(go.Scatter(y=0.3125 * x,
                                      mode = 'lines',
                                      name= '设计值',
                                      line=dict(color='green',width=3, dash = 'dash')))
            fig2.add_hline(y= 50000, line_width=3, line_dash="dot", line_color="green")
            fig2.add_hline(y= times_round, line_width=3, line_dash="dot", line_color="green")
            fig2.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
            fig2.update_layout(xaxis_range=[0,pd22['total_daily_odometer'].max()+40],yaxis_range=[0,pd22['total_susactuvlvblkfrsts'].max()+20],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>里程<b>"
                                             )

            fig2.show()
            st.plotly_chart(fig2,height=500,width=800,use_container_width=True)
            st.success('根据全辆车的数据，当里程达到16万公里时，排气电磁阀使用为`%s`次，比标定制5万次`%s`了`%s`'%(times_round,high,ratio))




    if open_cnt == '储气罐电磁阀':
        st.subheader('预测储气罐电磁阀打开次数')
        #预测左前电磁阀打开次数
        avg_predicted_total_susactuvlvblkrsvrsts = pd21['predicted_total_susactuvlvblkrsvrsts'].sum()/pd21['dt'].count()
        predicted_total_susactuvlvblkrsvrsts_rounded = int(avg_predicted_total_susactuvlvblkrsvrsts)
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            y=pd21['predicted_total_susactuvlvblkrsvrsts'],
            x=pd21.dt,
            name='<b>预测储气罐电磁阀打开次数<b>',
            orientation='v',text= pd21['predicted_total_susactuvlvblkrsvrsts'],
            marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
         marker_line_width=1.5, opacity=0.6

        ))
        fig12.add_hline(y= avg_predicted_total_susactuvlvblkrsvrsts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均电磁阀预测耐久:%s"%(predicted_total_susactuvlvblkrsvrsts_rounded))
        fig12.update_yaxes(title_text = "<b>预测储气罐电磁阀打开次数<b>", title_standoff=5)
        fig12.update_layout(
                           height=500,width=800,
                           showlegend = False,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>"
                                         )
        fig12.show()
        st.plotly_chart(fig12,height=600,width=900,use_container_width=True)
        if show_curve == '显示':
            x1=0
            x2=180000
            x = np.arange(x1,x2)
            m, b = np.polyfit( pd22['total_daily_odometer'],pd22['total_susactuvlvblkrsvrsts'], 1)
            colx1= b/(0.3125-m)
            coly1= colx1 * 0.3125
            colx1_round = round(colx1,3)
            coly1_round = round(coly1,3)
            m_round = round(m,2)
            b_round = round(b,2)
            times = m * 160000 + b
            times_round = round(times, 2)
            difference = abs((times - 50000)/times)
            ratio = f"{difference:.2%}"
            if times <= 50000:
                high = '低'
            else:
                high = '高'
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=m*x+b,
                                      mode = 'lines',
                                      name= '实际值预测模型',
                                      line=dict(color='royalblue',width=3)))
            fig2.add_trace(go.Scatter(x=pd22['total_daily_odometer'],y=pd22['total_susactuvlvblkrsvrsts'],
                                      mode = 'markers',
                                      name = '实际值',
                                      line = dict(color='mediumvioletred',width=4)
                                      ))
            fig2.add_trace(go.Scatter(y=0.3125 * x,
                                      mode = 'lines',
                                      name= '设计值',
                                      line=dict(color='green',width=3, dash = 'dash')))
            fig2.add_hline(y= 50000, line_width=3, line_dash="dot", line_color="green")
            fig2.add_hline(y= times_round, line_width=3, line_dash="dot", line_color="green")
            fig2.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
            fig2.update_layout(xaxis_range=[0,pd22['total_daily_odometer'].max()+40],yaxis_range=[0,pd22['total_susactuvlvblkrsvrsts'].max()+20],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>里程<b>"
                                             )

            fig2.show()
            st.plotly_chart(fig2,height=500,width=800,use_container_width=True)
            st.success('根据全辆车的数据，当里程达到16万公里时，排气电磁阀使用为`%s`次，比标定制5万次`%s`了`%s`'%(times_round,high,ratio))

    if open_cnt == '左后电磁阀':
        st.subheader('预测左后电磁阀打开次数')
        #预测左前电磁阀打开次数
        avg_predicted_total_susactuvlvblkrlsts = pd21['predicted_total_susactuvlvblkrlsts'].sum()/pd21['dt'].count()
        predicted_total_susactuvlvblkrlsts_rounded = int(avg_predicted_total_susactuvlvblkrlsts)
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            y=pd21['predicted_total_susactuvlvblkrlsts'],
            x=pd21.dt,
            name='<b>预测左后电磁阀打开次数<b>',
            orientation='v',text= pd21['predicted_total_susactuvlvblkrlsts'],
            marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
         marker_line_width=1.5, opacity=0.6

        ))
        fig12.add_hline(y= avg_predicted_total_susactuvlvblkrlsts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均电磁阀预测耐久:%s"%(predicted_total_susactuvlvblkrlsts_rounded))
        fig12.update_yaxes(title_text = "<b>预测左后电磁阀打开次数<b>", title_standoff=5)
        fig12.update_layout(
                           height=500,width=800,
                           showlegend = False,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>"
                                         )
        fig12.show()
        st.plotly_chart(fig12,height=600,width=900,use_container_width=True)
        if show_curve == '显示':
            x1=0
            x2=180000
            x = np.arange(x1,x2)
            m, b = np.polyfit( pd22['total_daily_odometer'],pd22['total_susactuvlvblkrlsts'], 1)
            colx1= b/(0.3125-m)
            coly1= colx1 * 0.3125
            colx1_round = round(colx1,3)
            coly1_round = round(coly1,3)
            m_round = round(m,2)
            b_round = round(b,2)
            times = m * 160000 + b
            times_round = round(times, 2)
            difference = abs((times - 50000)/times)
            ratio = f"{difference:.2%}"
            if times <= 50000:
                high = '低'
            else:
                high = '高'
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=m*x+b,
                                      mode = 'lines',
                                      name= '实际值预测模型',
                                      line=dict(color='royalblue',width=3)))
            fig2.add_trace(go.Scatter(x=pd22['total_daily_odometer'],y=pd22['total_susactuvlvblkrlsts'],
                                      mode = 'markers',
                                      name = '实际值',
                                      line = dict(color='mediumvioletred',width=4)
                                      ))
            fig2.add_trace(go.Scatter(y=0.3125 * x,
                                      mode = 'lines',
                                      name= '设计值',
                                      line=dict(color='green',width=3, dash = 'dash')))
            fig2.add_hline(y= 50000, line_width=3, line_dash="dot", line_color="green")
            fig2.add_hline(y= times_round, line_width=3, line_dash="dot", line_color="green")
            fig2.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
            fig2.update_layout(xaxis_range=[0,pd22['total_daily_odometer'].max()+40],yaxis_range=[0,pd22['total_susactuvlvblkrlsts'].max()+20],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>里程<b>"
                                             )

            fig2.show()
            st.plotly_chart(fig2,height=500,width=800,use_container_width=True)
            st.success('根据全辆车的数据，当里程达到16万公里时，排气电磁阀使用为`%s`次，比标定制5万次`%s`了`%s`'%(times_round,high,ratio))

    if open_cnt == '右后电磁阀':
        st.subheader('预测右后电磁阀打开次数')
        #预测左前电磁阀打开次数
        avg_predicted_total_susactuvlvblkrrsts = pd21['predicted_total_susactuvlvblkrrsts'].sum()/pd21['dt'].count()
        predicted_total_susactuvlvblkrrsts_rounded = int(avg_predicted_total_susactuvlvblkrrsts)
        fig12 = go.Figure()
        fig12.add_trace(go.Bar(
            y=pd21['predicted_total_susactuvlvblkrrsts'],
            x=pd21.dt,
            name='<b>预测右后电磁阀打开次数<b>',
            orientation='v',text= pd21['predicted_total_susactuvlvblkrrsts'],
            marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
         marker_line_width=1.5, opacity=0.6

        ))
        fig12.add_hline(y= avg_predicted_total_susactuvlvblkrrsts, line_width=3, line_dash="dash", line_color="green", annotation_text="以上几日平均电磁阀预测耐久:%s"%(predicted_total_susactuvlvblkrrsts_rounded))
        fig12.update_yaxes(title_text = "<b>预测右后电磁阀打开次数<b>", title_standoff=5)
        fig12.update_layout(
                           height=500,width=800,
                           showlegend = False,
                           margin=dict(l=0, r=200,b=40,t=20),
                           xaxis_title="<b>日期<b>"
                                         )
        fig12.show()
        st.plotly_chart(fig12,height=600,width=900,use_container_width=True)
        if show_curve == '显示':
            x1=0
            x2=180000
            x = np.arange(x1,x2)
            m, b = np.polyfit( pd22['total_daily_odometer'],pd22['total_susactuvlvblkrrsts'], 1)
            colx1= b/(0.3125-m)
            coly1= colx1 * 0.3125
            colx1_round = round(colx1,3)
            coly1_round = round(coly1,3)
            m_round = round(m,2)
            b_round = round(b,2)
            times = m * 160000 + b
            times_round = round(times, 2)
            difference = abs((times - 50000)/times)
            ratio = f"{difference:.2%}"
            if times <= 50000:
                high = '低'
            else:
                high = '高'
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=m*x+b,
                                      mode = 'lines',
                                      name= '实际值预测模型',
                                      line=dict(color='royalblue',width=3)))
            fig2.add_trace(go.Scatter(x=pd22['total_daily_odometer'],y=pd22['total_susactuvlvblkrrsts'],
                                      mode = 'markers',
                                      name = '实际值',
                                      line = dict(color='mediumvioletred',width=4)
                                      ))
            fig2.add_trace(go.Scatter(y=0.3125 * x,
                                      mode = 'lines',
                                      name= '设计值',
                                      line=dict(color='green',width=3, dash = 'dash')))
            fig2.add_hline(y= 50000, line_width=3, line_dash="dot", line_color="green")
            fig2.add_hline(y= times_round, line_width=3, line_dash="dot", line_color="green")
            fig2.update_yaxes(title_text = "<b>预测排气电磁阀打开次数<b>", title_standoff=5)
            fig2.update_layout(xaxis_range=[0,pd22['total_daily_odometer'].max()+40],yaxis_range=[0,pd22['total_susactuvlvblkrrsts'].max()+20],
                               height=500,width=800,
                               showlegend = True,legend=dict(
                                                  yanchor="top",
                                                  y=0.99,
                                                  xanchor="left",
                                                  x=0.01
                                              ),
                               margin=dict(l=0, r=200,b=40,t=20),
                               xaxis_title="<b>里程<b>"
                                             )

            fig2.show()
            st.plotly_chart(fig2,height=500,width=800,use_container_width=True)
            st.success('根据全辆车的数据，当里程达到16万公里时，排气电磁阀使用为`%s`次，比标定制5万次`%s`了`%s`'%(times_round,high,ratio))

