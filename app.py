import streamlit as st
from intro_markdown import detail_markdown_text
import fitbit
import pandas as pd
import altair as alt

st.set_page_config(page_title='Team Fitbit Challenge', 
                   page_icon=None, 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

st.title('Team Fitbit Challenge')
with st.expander('Click to see details'):
    st.markdown(detail_markdown_text)

NORM_STEPS = st.number_input(r'Enter Step Normalization $\sigma$', value=10_000, step=1,max_value=100_000)
NORM_ACTIVE = st.number_input(r'Enter Active Minutes Normalization $\alpha$', value=22, step=1,max_value=100)
CONST_COEFF = st.number_input(r'Enter Constant Coefficient For Score', value=500, step=1,max_value=10000)
with st.expander('Team Data'):
    st.subheader('To The Max Steps')
    updated_ttm_steps = st.experimental_data_editor(fitbit.df_ttm_steps, height=525, width=800)
    st.subheader('To The Max Active Minutes')
    updated_ttm_active = st.experimental_data_editor(fitbit.df_ttm_active, height=525, width=800)

    st.subheader('Walking Dead Steps')
    updated_wd_steps = st.experimental_data_editor(fitbit.df_wd_steps, height=525, width=800)
    st.subheader('Walking Dead Active Minutes')
    updated_wd_active = st.experimental_data_editor(fitbit.df_wd_active, height=525, width=800)
    cumulative_data = fitbit.get_cumulative_avg_daily_score_per_team(norm_steps=NORM_STEPS, 
                                                                        norm_active=NORM_ACTIVE,
                                                                        const_coefficient=CONST_COEFF,
                                                                        df_wd_steps=updated_wd_steps, 
                                                                        df_wd_active=updated_wd_active,
                                                                        df_ttm_steps=updated_ttm_steps,
                                                                        df_ttm_active=updated_ttm_active)
# chart = alt.Chart(cumulative_data).mark_line().encode(x='date',y='wd')
# st.altair_chart(chart, use_container_width=True)
st.subheader('Cumulative Average Daily Score Per Team')
st.line_chart(cumulative_data,x='date',use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.metric(label='To The Max Final Score', value=f'{cumulative_data["To The Max Score"][-1]:.0f}')
with col2:
    st.metric(label='Walking Dead Final Score', value=f'{cumulative_data["Walking Dead Score"][-1]:.0f}')